import os
from sqlite3 import dbapi2 as sqlite3

from flask import Flask, g, render_template, flash, redirect, url_for

from api import APIGrabber


print "ENVIRON:"
external_settings = getattr(os.environ, 'PTHEMES_SETTINGS', None)
print external_settings

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pthemes.db'),
    DEBUG=True,
    SECRET_KEY='mysupersecretsecretwahahhr'
))
if external_settings:
    app.config.from_object(external_settings)


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


def populatedb():
    """Populates the database with info from github."""
    print "populating db"
    init_db()
    a = APIGrabber()
    data = a.process()
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


@app.cli.command('populatedb')
def populatedb_command():
    populatedb()

@app.route('/')
def show_entries():
    q_with_images = """
    SELECT
        *,
        GROUP_CONCAT(s.url) AS 'image_urls'
    FROM themes t
        INNER JOIN screenshots s ON s.theme_id = t.id
    GROUP BY t.name
    ORDER BY name
    """
    image_themes = query_db(q_with_images)

    q_no_image = """
    SELECT *
    FROM themes t
    WHERE NOT EXISTS (
      SELECT * FROM screenshots s WHERE s.theme_id = t.id
    )
    """
    no_image_themes = query_db(q_no_image)

    counts = {}
    counts['image_themes'] = len(image_themes)
    counts['no_image_themes'] = len(no_image_themes)
    counts['total'] = counts['image_themes'] + counts['no_image_themes']

    for t in image_themes:
        if t['image_urls'] is not None:
            t['image_urls'] = t['image_urls'].split(',')

    return render_template('list.html',
                           image_themes=image_themes,
                           no_image_themes=no_image_themes,
                           counts=counts)

@app.route('/refresh_hook', methods=['GET'])
def add_entry():
    populatedb()
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.run()

