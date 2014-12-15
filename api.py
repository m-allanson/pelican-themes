import pprint
import re
from github import Github

CREDENTIALS_FILE = 'GITHUB_API_KEY.dat'

class APIGrabber():
    def __init__(self):
        self.token = ''
        self.user = 'getpelican'
        self.repo_name = 'pelican-themes'
        self.main_repo = None


    def info_from_content(self, content):
        """Get data needed to extract screenshots from a dir or submodule."""
        c = content

        # dirs have path, submodules are assumed to be /
        if c['type'] == 'dir':
            path = c['path']
        else:
            path = ''

        # Extract user and repo from url
        repo_info = c['html_url'].replace('https://github.com/', '')\
                                 .split('/')

        return {
            'user': repo_info[0],
            'repo': repo_info[1],
            'path': path,
            'sha': c['sha'],
            'name': c['name'],
            'html_url': c['html_url'],
            'image_urls': []
        }

    def fetch(self):
        """
        Gets the list of themes from the pelican themes repo, then gets
        possible images from each theme.
        """
        with open(CREDENTIALS_FILE, 'r') as fd:
            token = fd.readline().strip()  # Can't hurt to be paranoid

        gh = Github(token)
        self.main_repo = gh.get_repo('{}/{}'.format(self.user, self.repo_name))
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

        # Get theme images
        for t in theme_list:
            print '---- Checking theme: {}'.format(t['name'])
            # It's a subdir in the main repo
            if t['user'] == self.user and t['repo'] == self.repo_name:
                this_repo = self.main_repo
            # It's a submodule in a different repo
            else:
                try:
                    this_repo = gh.get_repo('{}/{}'.format(t['user'], t['repo']))
                except:
                    print 'FAILED on: {}/{}'.format(t['user'], t['repo'])

            contents = []
            contents = this_repo.get_contents(t['path']).raw_data

            # Find image files for this repo / path
            for c in contents:
                m = re.search('.png|.jpg$', c['name'], re.IGNORECASE)
                if m:
                    t['image_urls'].append(c['download_url'])

            print 'found {} images'.format(len(t['image_urls']))

        print pprint.pformat(theme_list)
        return theme_list