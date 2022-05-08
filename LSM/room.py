from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from LSM.auth import login_required
from LSM.db import get_db
from wtforms.fields import SelectField, StringField
from wtforms.validators import Length, NumberRange
from flask_wtf import Form

bp = Blueprint('room', __name__)


@bp.route('/room/delete', methods=('POST',))
@login_required
def delete():
    room_id = request.form['room_id']
    db, cur = get_db()
    cur.execute(f"DELETE FROM room WHERE room_id = {room_id}")
    db.commit()
    return redirect(url_for('room.update'))


class CreateForm(Form):
    room_name = StringField('房间名', validators=[Length(min=1, max=19)])
    room_location = StringField('房间位置', validators=[Length(min=1, max=19)])
    room_capacity = StringField('房间容量', validators=[NumberRange(min=0, max=2000)])
    computers = SelectField("电脑型号", choices=[])

    def add_computers(self, cur):
        cur.execute("SELECT computer_id, computer_model FROM computer")
        for item in cur.fetchall():
            self.computers.choices.append((item['computer_id'], item['computer_model']))


@bp.route('/room/create', methods=('POST', 'GET'))
@login_required
def create():
    if request.method == 'POST':
        room_name = request.form['room_name']
        computer_id = request.form['computers']
        account_id = g.user
        room_location = request.form['room_location']
        room_capacity = request.form['room_capacity']

        error = None
        if not (room_name and computer_id and account_id and room_location
                and room_capacity):
            error = 'Please input all the room information.\n'
        if error is not None:
            flash(error)
        else:
            db, cur = get_db()
            cur.execute(
                "INSERT INTO room (computer_id, account_id, room_name, room_location, room_capacity) "
                f"VALUES ({computer_id}, {account_id}, '{room_name}', '{room_location}', {room_capacity})"
            )
            db.commit()
        return redirect(url_for('room.view'))

    db, cur = get_db()
    cur.execute("SELECT computer_id, computer_model FROM computer")
    create_form = CreateForm()
    create_form.add_computers(cur)
    return render_template('room/create.html', form=create_form)


@bp.route('/room', methods=('POST', 'GET'))
@login_required
def update():
    if request.method == 'POST':
        room_name = request.form['room_name']
        account_id = g.user
        room_location = request.form['room_location']
        room_capacity = request.form['room_capacity']
        room_id = request.form['room_id']
        room_notes = request.form['room_notes']

        error = None
        if not (room_name and account_id and room_location
                and room_capacity):
            error = 'Please input all the room information.\n'
        if error is not None:
            flash(error)
        else:
            db, cur = get_db()
            cur.execute(
                "UPDATE room "
                f" set "
                f" room_name='{room_name}',"
                f" room_location='{room_location}',"
                f" room_capacity={room_capacity},"
                f" room_notes='{room_notes}' "
                f" WHERE room_id = {room_id}"
            )
            db.commit()
        return redirect(url_for('room.update'))
    db, cur = get_db()
    cur.execute("SELECT *"
                " FROM room, computer, account, teacher"
                " WHERE room.account_id=computer.computer_id"
                " AND room.account_id=account.account_id"
                " AND account.teacher_id=teacher.teacher_id")
    room_info = cur.fetchall()
    return render_template('room/index.html', room_info=room_info)


@bp.route('/room/view', methods=('GET', ))
@login_required
def view():
    db, cur = get_db()
    cur.execute("SELECT * FROM room_view")
    v = cur.fetchall()
    return render_template('room/view.html', v=v)
