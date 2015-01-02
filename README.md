# Requirements
Python 2.7
Postgres 9.4
See requirements.txt


# Getting started

The site requires four environment variables to get up and running.  You can
enable these in a shell like this:

```
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgres://<username>:<password>@<address>/<dbname>"
export SECRET_KEY="<your secret key here>"
export GITHUB_API_KEY="<your github api key here>"
```

If using virtualenv or similar, you can add the above lines to your `preactivate` script.

Now you're ready to install the requirements `pip install -r requirements.txt`.

Next you'll need to populate the app with data from github.  This may take a minute or two:

`flask --app=pthemes populatedb`

Now you can run the app:

`flask --app=pthemes --debug run`

To run via gunicorn:
`gunicorn -w 1 -b 127.0.0.1:5000 pthemes:app`

To run via foreman (using Procfile, a la heroku)
`foreman start web`

In each case, the site will be available on http://127.0.0.1:5000

Force push to heroku
`git push heroku dev:master --force`

# About
A web page that shows screenshots of Pelican themes.  The screenshots are sourced from <https://github.com/getpelican/pelican-themes> via the Github api.

Contribution is very welcome.  Thanks :)


# Screenshots
Theme screenshots are found from folders or submodules in the repo at <https://github.com/getpelican/pelican-themes>.


# Useful links
The getpelican/pelican-themes repo: <https://github.com/getpelican/pelican-themes>
An example theme: <https://api.github.com/repos/getpelican/pelican-themes/contents/bootstrap2>