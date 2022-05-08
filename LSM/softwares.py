from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from LSM.auth import login_required
from LSM.db import get_db
from wtforms.fields import SelectField, StringField, SelectMultipleField
from wtforms.validators import Length, NumberRange
from flask_wtf import Form

bp = Blueprint('softwares', __name__)


@bp.route('/softwares', methods=('GET', ))
@login_required
def view():
    db, cur = get_db()
    cur.execute("SELECT * FROM software_view")
    v = cur.fetchall()
    return render_template("softwares/view.html", v=v)


@bp.route('/softwares/<int:s_id>/delete', methods=('GET', ))
@login_required
def delete(s_id):
    db, cur = get_db()
    cur.execute(f"DELETE FROM software_room WHERE software_id={s_id}")
    cur.execute(f"DELETE FROM software WHERE software_id={s_id}")
    db.commit()
    return redirect(url_for('softwares.view'))


class Add(Form):
    category = SelectField("类型", choices=[])
    name = StringField("软件名称", validators=[Length(min=1, max=19)])
    conf = StringField("配置要求", validators=[Length(min=0, max=99)])
    des = StringField("软件描述", validators=[Length(min=0, max=99)])

    def add_category(self, cur):
        cur.execute("SELECT * FROM category")
        for item in cur.fetchall():
            self.category.choices.append((item['category_id'], item['category_name']))


@bp.route('/softwares/add', methods=('POST', 'GET'))
@login_required
def add():
    if request.method == 'POST':
        form = request.form
        c_id = form['category']
        name = form['name']
        conf = form['conf']
        des = form['des']
        db, cur = get_db()
        cur.execute(f"INSERT INTO software(category_id, software_name, software_configuration,"
                    f" software_description) VALUES "
                    f" ({c_id}, '{name}', '{conf}', '{des}')")
        db.commit()
        return redirect(url_for('softwares.view'))
    form = Add()
    db, cur = get_db()
    form.add_category(cur)
    return render_template('/softwares/add.html', form=form)


@bp.route('/softwares/<int:_id>/add_room', methods=('POST', 'GET'))
@login_required
def add_room(_id):
    """
    本来需要使用 js 做一个弹窗功能的，时间有限，并且不了解js，故只能写成界面了
    """
    if request.method == 'POST':
        db, cur = get_db()
        room_ids = request.form.keys()
        for room_id in room_ids:
            cur.execute(f"SELECT * FROM software_room WHERE software_id={_id} AND room_id={int(room_id)}")
            if cur.rowcount == 0:
                cur.execute(f"INSERT INTO software_room(software_id, room_id) VALUES ({_id}, {room_id})")
        db.commit()
        return redirect(url_for('softwares.view'))
    db, cur = get_db()
    cur.execute("SELECT * FROM room")
    room = cur.fetchall()
    return render_template("softwares/add_room.html", room=room, id=_id)
