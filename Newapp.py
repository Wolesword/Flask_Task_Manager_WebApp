from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

Newapp = Flask(__name__)
Newapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TaskManager.db'

db = SQLAlchemy(Newapp)


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@Newapp.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Work(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding the task'

    else:
        tasks = Work.query.order_by(Work.date_created).all()
        return render_template('index.html', tasks=tasks)


@Newapp.route('/delete/<int:id>')
def Del_Task(id):
    task_to_delete = Work.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'there was a problem deleting the task'


@Newapp.route('/update/<int:id>', methods=['GET', 'POST'])
def task_update(id):
    task = Work.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating the task'

    else:
        return render_template('update.html', tasks=task)


if __name__ == "__main__":
    Newapp.run(debug=True)
