[![Code Climate](https://codeclimate.com/github/m-allanson/pelican-themes.png)](https://codeclimate.com/github/m-allanson/pelican-themes)

# Requirements
Vagrant ~1.6

# Getting started
* Install vagrant
* install vagrant librarian-chef plugin with the following command: `vagrant plugin install vagrant-librarian-chef`
* Edit the file `/provisioning/GITHUB_API_KEY.dat` to contain your github api key
* Run `vagrant up`
* Wait
* Keep waiting
* Browse to http://localhost:3000

# About
A quick and dirty NodeJS website that shows screenshots of Pelican themes.  The screenshots are sourced from <https://github.com/getpelican/pelican-themes> via the Github api.

The Github data is cached in Redis.

You'll need to set an env var called GITHUB_API_KEY to fetch the theme data from github.  This can be done by editing the file `/provisioning/GITHUB_API_KEY.dat` to contain your API key.

The Vagrant VM automatically starts node using forever.  Logs can be found in `/logs/`.

To run the node app manually, login to the VM with `vagrant ssh`, from there, run `forever stopall`, then `node --harmony /vagrant/server.js`

Contribution is very welcome.  Thanks :)

# Screenshots
Theme screenshots are found from folders or submodules in the repo at <https://github.com/getpelican/pelican-themes>.  The script repoService.js searches of each theme for `jpg` or `png` files with the words `screenshot` or `preview` in their filename.  The following file names would be matched:

* theme-screenshot.png
* my-preview.jpg
* screenshot.jpg
* screenshot.png
* preview.png

It doesn't check in a `screenshots` folder, but probably should.
It doesn't check in a `document` folder, but maybe should? See https://github.com/if1live/pelican-sora
It won't find `screenshot1.png` or `preview1.jpg` but probably should.
It won't find `index.png` but maybe should?

# Useful links
The getpelican/pelican-themes repo: <https://github.com/getpelican/pelican-themes>
An example theme: <https://api.github.com/repos/getpelican/pelican-themes/contents/bootstrap2>

# Todo
periodically check for updates (or use hooks?)

# Notes
`sudo npm install -g redis-commander`, followed by `redis-commander -p 3001` will let you view the redis store in a browser from the host machine.  <http://localhost:3001>