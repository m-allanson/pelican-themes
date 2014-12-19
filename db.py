import psycopg2
import psycopg2.extras

from api import APIGrabber


class PonyDB:
    """
    A little wrapper for accessing the database via psycopg2.
    """

    def __init__(self, app):
        """Open a new database connection."""
        self.app = app
        self.db = psycopg2.connect(app.config['DATABASE'])

    def query_db(self, query, args=(), one=False):
        """Execute a query on the db"""
        db = self.db
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        last_id = cur.fetchone()[0]
        rv = cur.fetchall()
        db.commit()
        cur.close()

        # Return results or id of last insert
        ret = (rv[0] if rv else None) if one else rv
        if len(ret) == 0:
            ret = last_id

        return ret

    def init_db(self):
        """
        Create database structure from schema file.  Scheme file can drop
        existing tables.
        """
        db = self.db
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        with self.app.open_resource('schema.sql', mode='r') as f:
            cur.execute(f.read())
        db.commit()

    def populate_db(self):
        """Populates the database with info from github."""
        self.init_db()
        a = APIGrabber(self.app.config['GITHUB_API_KEY'])
        data = a.process()
        theme_query = 'insert into themes (name, sha, user_name, repo, path, html_url) ' \
                      'values (%s, %s, %s, %s, %s, %s) RETURNING id'
        img_query = 'insert into screenshots (theme_id, url) values (%s, %s) RETURNING id'

        for d in data:
            row_id = self.query_db(
                theme_query,
                (d['name'], d['sha'], d['user'], d['repo'], d['path'], d['html_url'])
            )

            for image_url in d['image_urls']:
                self.query_db(
                    img_query,
                    (row_id, image_url)
                )

        print('Populated the database.')

    def get_image_themes(self):
        """
        Get all themes that have related images.  This should be the majority
        of themes.
        """
        q_with_images = """
        SELECT
            t.name, t.sha, t.user_name, t.repo, t.path, t.html_url,
            array_to_string(array_agg(s.url), ',') AS image_urls
        FROM themes t
        INNER JOIN screenshots s ON s.theme_id = t.id
        GROUP BY t.name, t.sha, t.user_name, t.repo, t.path, t.html_url
        ORDER BY name
        """
        return self.query_db(q_with_images)

    def get_no_image_themes(self):
        """
        Get all themes that don't have related images.  This should be a
        minority of themes.
        """
        q_no_image = """
        SELECT *
        FROM themes t
        WHERE NOT EXISTS (
          SELECT * FROM screenshots s WHERE s.theme_id = t.id
        )
        """
        return self.query_db(q_no_image)
