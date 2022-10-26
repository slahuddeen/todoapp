from distutils.log import error
import json
from types import MethodDescriptorType
from wsgiref.util import request_uri
from flask import Flask, render_template, redirect, jsonify, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc
import sys

from traitlets import default

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:abc@localhost:5432/todoapp'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)
    
    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    checked = db.Column(db.Boolean, nullable=True, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)
    
    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.checked}>'

with app.app_context():
    db.create_all()

@app.route('/todos/create', methods=['GET','POST'])
def create_todo():
    body = {}
    error= False
    try:
        #description = request.form.get('description', '')
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description)
        active_list = TodoList.query.get(list_id)
        todo.list = active_list
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    if not error:
        return jsonify(body)


@app.route('/todos/<todo_id>/set-checked', methods=['GET', 'POST'])
def set_checked(todo_id):
    try:
        completed = request.get_json()['checked']
        todo = Todo.query.get(todo_id)
        todo.checked = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))
    
@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
      lists=TodoList.query.all(),
      active_list=TodoList.query.get(list_id),
      todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    )

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

if __name__ == '__main__':
    app.app_context()
    app.debug = True
    app.run(debug=True)
    app.run(host="0.0.0.0", port=3000)