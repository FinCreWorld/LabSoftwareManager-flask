from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from LSM.db import get_db

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = user_id
    if user_id is not None:
        db, cur = get_db()
        cur.execute(f"SELECT account_priviledge FROM account WHERE account_id={user_id}")
        a = cur.fetchone()
        if a is not None:
            g.pri = a['account_priviledge']


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # return "hello"
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        username = request.form['username']
        password = request.form['password']
        db, cur = get_db()
        error = None

        if not username:
            error = "user name is required."
        elif not password:
            error = "password is required."
        elif cur.execute(f"SELECT * FROM account WHERE teacher_id='{teacher_id}'"):
            error = "the teacher_id has been registered"
        elif cur.execute(f"SELECT * FROM account WHERE account_name='{username}'"):
            error = f"user '{username}' is already existed."

        if error is None:
            cur.execute("SELECT * FROM account")
            # 如果是第一个注册的话，默认是管理员账户
            if cur.rowcount == 0:
                cur.execute(f"INSERT INTO account(account_name, account_password, teacher_id, account_priviledge) "
                            f"VALUES ('{username}', '{generate_password_hash(password)}', '{teacher_id}', 1)")
            else:
                cur.execute(f"INSERT INTO account(account_name, account_password, teacher_id) "
                            f"VALUES ('{username}', '{generate_password_hash(password)}', '{teacher_id}')")
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
    # return "hello world\n"


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        db, cur = get_db()
        error = None
        cur.execute(f"SELECT * FROM account WHERE account_name='{username}';")
        user = cur.fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user['account_password'], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session['user_id'] = user['account_id']
            return redirect(url_for('room.view'))

        flash(error)

    session.clear()
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapper_view
