import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, render_template, flash, redirect, url_for
from api import APIGrabber
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pthemes.db'),
    DEBUG=True,
    SECRET_KEY='mysupersecretsecretwahahhr'
))
app.config.from_envvar('PTHEMES_SETTINGS', silent=True)


def make_dicts(cursor, row):
    """Row factory that converts tuples to dicts"""
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = make_dicts
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def query_db(query, args=(), one=False):
    """Execute a query on the db"""
    db = get_db()
    cur = db.execute(query, args)
    last_id = cur.lastrowid
    rv = cur.fetchall()
    db.commit()
    cur.close()

    ret = (rv[0] if rv else None) if one else rv
    if len(ret) == 0:
        ret = last_id

    return ret


@app.cli.command('populatedb')
def populatedb_command():
    """Populates the database with info from github."""
    a = APIGrabber()
    data = a.fetch()
    theme_query = 'insert into themes (name, sha, user, repo, path, html_url) ' \
                  'values (?, ?, ?, ?, ?, ?)'
    img_query = 'insert into screenshots (theme_id, url) values (?, ?)'

    for d in data:
        row_id = query_db(
            theme_query,
            (d['name'], d['sha'], d['user'], d['repo'], d['path'], d['html_url'])
        )

        for image_url in d['image_urls']:
            query_db(
                img_query,
                (row_id, image_url)
            )

    print('Populated the database.')


@app.route('/')
def show_entries():
    q = """
    SELECT
        *,
        GROUP_CONCAT(s.url) AS 'image_urls'
    FROM themes t
        INNER JOIN screenshots s ON s.theme_id = t.id
    GROUP BY t.name
    ORDER BY name
    """
    themes = query_db(q)

    for t in themes:
        if t['image_urls'] is not None:
            t['image_urls'] = t['image_urls'].split(',')

    return render_template('list.html', themes=themes)


@app.route('/add', methods=['GET'])
def add_entry():
    db = get_db()
    db.execute('insert into themes (title, text) values (?, ?)',
               ['Test', 'and test'])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.run()

# count amount of results with images
#
# SELECT
#     count(DISTINCT t.id)
# FROM themes t
#     INNER JOIN screenshots s ON s.theme_id = t.id