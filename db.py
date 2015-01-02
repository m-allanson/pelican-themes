import psycopg2
import psycopg2.extras


class PonyDB:
    """
    A little wrapper for accessing the database via psycopg2.
    """

    def __init__(self, app):
        """Open a new database connection."""
        self.app = app
        self.db = psycopg2.connect(app.config['DATABASE'])

    def get_connection(self):
        """Returns the database connection"""
        return self.db

    def exec_sql(self, query, *args):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, *args)
        self.db.commit()
        return cur

    def insert(self, query, *args):
        cur = self.exec_sql(query, *args)
        last_id = cur.fetchone()[0]
        return last_id

    def update(self, query, *args):
        pass

    def select(self, query,  *args, **kwargs):
        # Return one result only?
        if 'one' not in kwargs:
            one = False
        else:
            one = True

        cur = self.exec_sql(query, *args)
        rv = cur.fetchall()

        # return row or rowset
        ret = (rv[0][0] if rv else None) if one else rv
        return ret


    def init_db(self):
        """
        Create database structure from schema file.  Schema file can drop
        existing tables.
        """
        db = self.db
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        with self.app.open_resource('schema.sql', mode='r') as f:
            cur.execute(f.read())
        db.commit()

    def populate_db(self, sha, data):
        """Populates the database with info from github."""
        self.init_db()
        theme_query = """
        insert into themes (name, sha, user_name, repo, path, html_url)
        values (%s, %s, %s, %s, %s, %s) RETURNING id
        """

        img_query = """
        insert into screenshots (theme_id, url) values (%s, %s) RETURNING id
        """

        self.exec_sql('truncate sha')
        self.insert('insert into sha (value) values (%s) RETURNING value', (sha,))

        for d in data:
            row_id = self.insert(
                theme_query,
                (d['name'], d['sha'], d['user'], d['repo'], d['path'], d['html_url'])
            )

            for image_url in d['image_urls']:
                self.insert(
                    img_query,
                    (row_id, image_url)
                )

        print('Populated the database.')

    def get_image_themes(self):
        """
        Get all themes that have related images.  This should be the majority
        of themes.
        """
        q = """
        SELECT
            t.name, t.sha, t.user_name, t.repo, t.path, t.html_url,
            array_to_string(array_agg(s.url), ',') AS image_urls
        FROM themes t
        INNER JOIN screenshots s ON s.theme_id = t.id
        GROUP BY t.name, t.sha, t.user_name, t.repo, t.path, t.html_url
        ORDER BY name
        """
        return self.select(q)

    def get_no_image_themes(self):
        """
        Get all themes that don't have related images.  This should be a
        minority of themes.
        """
        q = """
        SELECT *
        FROM themes t
        WHERE NOT EXISTS (
          SELECT * FROM screenshots s WHERE s.theme_id = t.id
        )
        """
        return self.select(q)

    def get_sha(self):
        """
        The pelican themes repo commit that this data was taken from
        """
        return self.select('SELECT * from sha LIMIT 1', one=True)

    def table_exists(self, name):
        """
        Check if a table name exists
        """
        q = """
        select exists(
          select * from information_schema.tables where table_name=%s
        )
        """
        return self.select(q, (name,), one=True)
