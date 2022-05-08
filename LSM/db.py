from flask import current_app, g
from flask.cli import with_appcontext
import click
import pymysql


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(**(current_app.config['DATABASE']))
        g.cur = g.db.cursor(pymysql.cursors.DictCursor)
    return g.db, g.cur


def close_db(e=None):
    db = g.pop('db', None)
    cur = g.pop('cur', None)

    if cur is not None:
        cur.close()

    if db is not None:
        db.close()


def init_db():
    db, cur = get_db()

    with current_app.open_resource('sql/lsm.sql') as f:
        sqls = f.read().decode('utf8').split(';')
        for sql in sqls[0:-1]:
            cur.execute(sql)
    with current_app.open_resource('sql/trigger1.sql') as f:
        cur.execute(f.read().decode('utf8'))
    with current_app.open_resource('sql/trigger2.sql') as f:
        cur.execute(f.read().decode('utf8'))
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
