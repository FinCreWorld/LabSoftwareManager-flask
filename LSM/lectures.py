from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from LSM.auth import login_required
from LSM.db import get_db
from wtforms.fields import SelectField, StringField
from wtforms.validators import Length, NumberRange
from flask_wtf import Form
import pandas as pd


bp = Blueprint('lectures', __name__)


@bp.route('/lectures', methods=('GET', 'POST'))
@login_required
def view():
    if request.method == 'POST':
        lec_id = request.form['lectures_id']
        name = request.form['lectures_name']
        hours = request.form['lectures_hours']
        total_num = request.form['lectures_total_num']
        class_num = request.form['lectures_class_num']
        semester = request.form['lectures_semester']
        notes = request.form['lectures_notes']
        software = request.form['lectures_software']
        teacher = request.form['lectures_teachers']

        db, cur = get_db()
        cur.execute("UPDATE lectures SET "
                    f" lectures_name='{name}', "
                    f" lectures_hours={hours}, "
                    f" lectures_total_num={total_num}, "
                    f" lectures_class_num={class_num}, "
                    f" lectures_semester='{semester}', "
                    f" lectures_notes='{notes}', "
                    f" lectures_software='{software}', "
                    f" lectures_teachers='{teacher}' "
                    f" WHERE lectures_id={lec_id}")
        db.commit()
        redirect('lectures.view')
    db, cur = get_db()
    cur.execute("SELECT * FROM lectures_view")
    v = cur.fetchall()
    return render_template("lectures/view.html", v=v)


@bp.route('/lectures/upload', methods=('POST', ))
@login_required
def upload():
    file_obj = request.files.get('lectures')
    # if file_obj.content_length:
    df = pd.read_csv(file_obj, encoding="utf-8")
    # 要求文件的格式必须为 课程名,学时,课程总人数,班级人数,课程学期,课程教师,学院 的csv文件
    n, m = df.shape
    db, cur = get_db()
    for i in range(n):
        cur.execute(f"SELECT department_id FROM department WHERE department_name='{df.iloc[i, -1]}'")
        if cur.rownumber == 0:
            cur.execute(f"INSERT INTO department(department_name) "
                        f" VALUES ('{df.iloc[i, -1]}')")
            db.commit()
        cur.execute(f"SELECT department_id FROM department WHERE department_name='{df.iloc[i, -1]}'")
        name = df.iloc[i, 0]
        hours = df.iloc[i, 1]
        total = df.iloc[i, 2]
        classnum = df.iloc[i, 3]
        semester = df.iloc[i, 4]
        teacher = df.iloc[i, 5]
        d_id = cur.fetchone()['department_id']
        cur.execute(f"INSERT INTO lectures(lectures_name, lectures_hours, lectures_total_num, "
                    f" lectures_class_num, lectures_semester, lectures_teachers, department_id) "
                    f" VALUES ('{name}', {hours}, {total}, {classnum}, '{semester}', '{teacher}', {d_id})")
    db.commit()
    return redirect(url_for('lectures.view'))
