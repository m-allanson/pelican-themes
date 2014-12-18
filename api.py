import pprint
import re
import requests

from github import Github, UnknownObjectException


CREDENTIALS_FILE = 'GITHUB_API_KEY.dat'

class APIGrabber():
    def __init__(self):
        self.gh = ''
        self.token = ''
        self.user = 'getpelican'
        self.repo_name = 'pelican-themes'
        self.main_repo = None

    def process(self):
        """Extracts a list of dicts from the Pelican Themes repo.  Each dict
        provides basic info about a Pelican theme."""
        with open(CREDENTIALS_FILE, 'r') as fd:
            token = fd.readline().strip()  # Can't hurt to be paranoid
        self.gh = Github(token)

        theme_list = self.fetch_content()
        theme_list = self.fetch_related_images(theme_list)

        return theme_list

    def fetch_content(self):
        """
        Gets the list of themes from the pelican themes repo, then gets
        possible images from each theme.
        """

        self.main_repo = self.gh.get_repo('{}/{}'.format(self.user, self.repo_name))
        contents = self.main_repo.get_contents('/').raw_data

        theme_list = []
        # Get theme location, whether directory or submodule
        for theme in contents:
            push = False
            if theme['type'] == 'dir':
                push = True
            elif theme['type'] == 'file' and theme['size'] == 0:
                push = True

            if push:
                theme_list.append(self.info_from_content(theme))

        return theme_list

    def fetch_related_images(self, theme_list):
        """ Given info about a repo/path on github, get any .jpg or .png files
        listed in that location."""
        failures = []

        for t in theme_list:
            contents = []

            this_repo = self.get_repo(t['user'], t['repo'])
            if this_repo is not None:
                contents = this_repo.get_contents(t['path']).raw_data

            # Find image files for this repo / path
            for c in contents:
                m = re.search('.png|.jpg$', c['name'], re.IGNORECASE)
                if m:
                    t['image_urls'].append(c['download_url'])

            if len(t['image_urls']) == 0:
                print 'could NO GET IMAGE for {}/{}'.format(t['user'], t['repo'])
            # else:
                # print 'found {} images'.format(len(t['image_urls']))

        # print "Successfully got images for {} themes:".format(len(theme_list))
        # print pprint.pformat(theme_list)
        #
        # print "Failed on {} themes: ===================".format(len(failures))
        # print pprint.pformat(failures)

        return theme_list

    def info_from_content(self, content):
        """Converts data returned from api into info needed to extract
        screenshots from a dir or submodule."""
        c = content

        # dirs have path, submodules are assumed to be /
        if c['type'] == 'dir':
            path = c['path']
        else:
            path = ''

        # Extract user and repo from url
        user, repo_name = self.github_url_to_user_repo(c['html_url'])

        return {
            'user': user,
            'repo': repo_name,
            'path': path,
            'sha': c['sha'],
            'name': c['name'],
            'html_url': c['html_url'],
            'image_urls': []
        }

    def get_repo(self, user, repo_name):
        """
        Get a repo based on user name and repo name
        """
        this_repo = None
        if user == self.user and repo_name == self.repo_name:
            this_repo = self.main_repo
        else:  # It's a submodule, so look up correct repo
            try:
                this_repo = self.gh.get_repo('{}/{}'.format(user, repo_name))
            except UnknownObjectException:
                # print 'FAILED on: {}/{}'.format(user, repo_name)
                user, repo_name = self.get_repo_via_web(user, repo_name)
                # print 'update user and repo name: {}/{}'.format(user, repo_name)

                # try again
                try:
                    this_repo = self.gh.get_repo('{}/{}'.format(user, repo_name))
                except:
                    print 'STILL FAILED=================='
                    return None

        return this_repo

    def get_repo_via_web(self, user, repo_name):
        """
        Github API doesn't redirect on user/repo renames or transfers.
        The workaround is to make a request to github.com for the repo, then
        see where you're redirected to to get the actual location.
        """
        url = 'https://github.com/{}/{}/'.format(user, repo_name)
        r = requests.get(url, allow_redirects=False)
        new_url = r.headers['location']
        user, repo_name = self.github_url_to_user_repo(new_url)

        return user, repo_name

    def github_url_to_user_repo(self, url):
        """
        Get the username and repo name from a github url like:
        https://github.com/user/repo/
        """
        repo_info = url.replace('https://github.com/', '').split('/')

        return repo_info[0], repo_info[1]