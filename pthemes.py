import os
import logging
from flask import Flask, render_template, redirect, url_for, flash
from pq import PQ

from api import APIGrabber
from db import PonyDB

logging.basicConfig()

# Config
# ---------------
# App config
app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', None))
db = PonyDB(app)
pq = PQ(db.get_connection())   # Postgres work queue
if db.table_exists('queue') is False:
    pq.create()
queue = pq['themes']

# App decorators
# ---------------
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.init_db()

@app.cli.command('populatedb')
def populatedb_command():
    db.populate_db()


# Routes
# ---------------
@app.route('/')
def show_entries():
    image_themes = db.get_image_themes()
    no_image_themes = db.get_no_image_themes()
    sha = db.get_sha()

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
                           counts=counts,
                           sha=sha)


@app.route('/refresh_hook', methods=['GET'])
def add_entry():
    queue.put('Refresh themes')
    flash('Added theme refresh job to queue')
    return redirect(url_for('show_entries'))


@app.cli.command('worker')
def queue_worker():

    for task in queue:
        if task is not None:
            a = APIGrabber(app.config['GITHUB_API_KEY'])
            sha, data = a.process()
            db.populate_db(sha, data)

if __name__ == "__main__":
    app.run()

