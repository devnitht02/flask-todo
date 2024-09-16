from datetime import datetime
from sqlalchemy import Boolean, Column
from sqlalchemy.orm import Mapped, mapped_column
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jvrvuirbboirneb'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskly.db"
db.init_app(app)


# class User(db.Model, UserMixin):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(80), nullable=False)
#     tasks: Mapped[list['Task']] = relationship('Task', back_populates='user')
#
#     def __repr__(self):
#         return f'<User {self.username}>'


class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    time: Mapped[str] = mapped_column(String(80), nullable=False)
    date: Mapped[str] = mapped_column(String(80), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    # user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    # user: Mapped['User'] = relationship('User', back_populates='tasks')

    def __repr__(self):
        return f'<Task {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        title = request.form.get('title')

        new_task = Task(title=title, date=date, time=time)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully")
        return redirect(url_for('index'))

    all_tasks = Task.query.all()

    return render_template('index.html', all_tasks=all_tasks)


@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully")
    return render_template("index.html", task=task)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
