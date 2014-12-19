import os
from flask import Flask, render_template, redirect, url_for
from db import PonyDB

# Config
# ---------------
app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS', None))
db = PonyDB(app)

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
    db.populate_db()
    return redirect(url_for('show_entries'))


if __name__ == "__main__":
    app.run()

