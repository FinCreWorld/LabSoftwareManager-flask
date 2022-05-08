import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from LSM.auth import login_required
from LSM.db import get_db
from wtforms.fields import SelectField, StringField
from wtforms.validators import Length, NumberRange
from flask_wtf import Form

bp = Blueprint('teacher', __name__)


@bp.route('/teacher', methods=('GET', 'POST'))
@login_required
def index():
    db, cur = get_db()
    cur.execute("SELECT account.account_id, account_name, account_priviledge, teacher.teacher_id, "
                " teacher_name, teacher_phone"
                " FROM account RIGHT JOIN teacher ON account.teacher_id = teacher.teacher_id")
    teacher_info = cur.fetchall()
    return render_template("teacher/index.html", teacher_info=teacher_info)


@bp.route('/teacher/delete', methods=('POST', ))
@login_required
def delete():
    teacher_id = request.form['teacher_id']
    db, cur = get_db()
    cur.execute(f"DELETE FROM teacher WHERE teacher_id={teacher_id}")
    db.commit()
    return redirect(url_for('teacher.index'))


@bp.route('/teacher/add', methods=('POST', ))
@login_required
def add():
    teacher_name = request.form['teacher_name']
    teacher_phone = request.form['teacher_phone']
    db, cur = get_db()
    cur.execute(f"INSERT INTO teacher (teacher_name, teacher_phone) VALUES ('{teacher_name}', {teacher_phone})")
    db.commit()
    return redirect(url_for('teacher.index'))


@bp.route('/teacher/upload', methods=('POST', ))
def upload():
    file_obj = request.files.get('teachers')
    df = pd.read_csv(file_obj, encoding="utf-8")
    # 要求文件的格式必须为 教师名，教师号码 的csv文件
    n, m = df.shape
    db, cur = get_db()
    for i in range(n):
        cur.execute(f"INSERT INTO teacher(teacher_name, teacher_phone)"
                    f" VALUES ('{df.iloc[i, 0]}', {df.iloc[i, 1]})")
    db.commit()
    return redirect(url_for('teacher.index'))
