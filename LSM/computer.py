import concurrent.futures

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

bp = Blueprint('computer', __name__)


@bp.route('/computer', methods=('POST', 'GET'))
@login_required
def index():
    if request.method == 'POST':
        c_id = request.form['computer_id']
        model = request.form['computer_model']
        mem = request.form['computer_memory']
        cpu = request.form['computer_cpu']
        gpu = request.form['computer_gpu']
        disk = request.form['computer_disk']
        disk_used = request.form['computer_disk_used']
        os1 = request.form['computer_os1']
        os2 = request.form['computer_os2']
        db, cur = get_db()
        cur.execute(" UPDATE computer"
                    f" set computer_model='{model}', computer_memory={mem}, computer_cpu='{cpu}',"
                    f" computer_gpu='{gpu}', computer_disk={disk}, computer_disk_used={disk_used}, "
                    f" computer_os1='{os1}', computer_os2='{os2}'"
                    f" WHERE computer_id={c_id}")
        db.commit()
        return redirect(url_for('computer.index'))
    db, cur = get_db()
    cur.execute("SELECT * FROM computer")
    computer_info = cur.fetchall()
    return render_template("computer/index.html", computer_info=computer_info)


@bp.route('/computer/delete', methods=('POST', ))
def delete():
    c_id = request.form['computer_id']
    db, cur = get_db()
    cur.execute(f"DELETE FROM computer WHERE computer_id={c_id}")
    db.commit()
    return redirect(url_for('computer.index'))


@bp.route('/computer/add', methods=('POST', 'GET'))
@login_required
def add():
    if request.method == 'POST':
        model = request.form['computer_model']
        mem = request.form['computer_memory']
        cpu = request.form['computer_cpu']
        gpu = request.form['computer_gpu']
        disk = request.form['computer_disk']
        disk_used = request.form['computer_disk_used']
        os1 = request.form['computer_os1']
        os2 = request.form['computer_os2']
        db, cur = get_db()
        cur.execute("INSERT INTO computer(computer_model, computer_memory, computer_cpu,"
                    " computer_gpu, computer_disk, computer_disk_used, computer_os1, computer_os2) "
                    f" VALUES ('{model}', '{mem}', '{cpu}', '{gpu}', {disk}, {disk_used}, '{os1}', '{os2}')")
        db.commit()
        return redirect(url_for('computer.index'))
    return render_template('computer/add.html')
