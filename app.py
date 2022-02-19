from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    language = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    # show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    phone = request.form.get("phone")
    language = request.form.get("language")
    #date_added = request.form.get("date_added")
    new_todo = Todo(title=title, phone=phone, language=language, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))  #redirect to index/homepage

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # updates item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))  #redirect to index/homepage

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # deletes item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))  #redirect to index/homepage


# launches server when 'python app.py' is entered 
if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=80)