**2024 update**: In 2023 I transferred the pelicanthemes.com domain to @justinmayer, who has created a new (and better!) site. It looks like the new site is generated from the `build-theme-previews.py` script in [getpelican/pelican-themes](https://github.com/getpelican/pelican-themes).

**2018 update**: _This project is live at pelicanthemes.com but is essentially unmaintained.  I'm happy to provide commit access to anyone who'd like to continue running it._

------

# About
A web page that shows screenshots of Pelican themes.  The screenshots are sourced from <https://github.com/getpelican/pelican-themes> via the Github api.

The site consists of two parts.  The frontend which lists out the themes, and a separate worker which will update themes in the background.

A live version can be seen at http://www.pelicanthemes.com

# Requirements
Python 2.7
Postgres 9.4
See requirements.txt


# Getting started

The site requires four environment variables to get up and running.  They look like this:

```
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgres://<username>:<password>@<address>/<dbname>"
export SECRET_KEY="<your secret key here>"
export GITHUB_API_KEY="<your github api key here>"
```

If using virtualenv or similar, you can add the above lines to your `preactivate` script.

Now you're ready to install the requirements `pip install -r requirements.txt`.

Now you can run the app:

`flask --app=pthemes --debug run`

And start the worker:

`flask --app=pthemes worker`

The site will now be available on http://127.0.0.1:5000.  You can trigger the worker to update the themes by visiting http://127.0.0.1:5000/git-update

# Other info

To run via gunicorn:

`gunicorn -w 1 -b 127.0.0.1:5000 pthemes:app`

To run the frontend (without worker) via foreman (using Procfile, a la heroku)

`foreman start web`

Force push to heroku

`git push heroku dev:master --force`

Push to heroku live site

`git push heroku-prod dev:master --force`

Manually run the worker on Heroku

`heroku run 'flask --app=pthemes worker'`


# Screenshots
Theme screenshots are found from folders or submodules in the repo at <https://github.com/getpelican/pelican-themes>.


# Useful links
The getpelican/pelican-themes repo: <https://github.com/getpelican/pelican-themes>
An example theme: <https://api.github.com/repos/getpelican/pelican-themes/contents/bootstrap2>
