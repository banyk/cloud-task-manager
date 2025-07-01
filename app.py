from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import time
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.json.ensure_ascii = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    done = db.Column(db.Boolean, default = False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }


@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        return make_response(jsonify([task.to_dict() for task in tasks]), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Error retrieving tasks'}), 500)


@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.json
        title = data.get('title', '').strip()

        if not title:
            return jsonify({'error': 'Title cannot be empty'}), 400
        new_task = Task(
            title = title,
            done = False
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    except Exception as e:
        return jsonify({'error': 'Error creating task'}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.json
        task = Task.query.get(task_id)

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        task.title = data.get('title', task.title)
        task.done = data.get('done', task.done)

        db.session.commit()
        return jsonify(task.to_dict()), 200
    except Exception as e:
        return jsonify({'error': 'Error updating task'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200
    except Exception as e:
        return jsonify({'error': 'Error deleting task'}), 500


@app.route('/')
def home():
    return "Hello, Banyk!"

def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                host="db", database="cloud_task_db", user="postgres", password="password"
            )
            conn.close()
            print("Postgres is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for Postgres...")
            time.sleep(1)

wait_for_postgres()


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")



