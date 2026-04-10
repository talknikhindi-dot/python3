from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Setup
db_path = os.path.join(os.path.dirname(__file__), 'talknik_database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class UserTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)

# Auto-Create Database
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = UserTask.query.all()
    return jsonify({"all_tasks": [{"id": t.id, "task": t.task_name} for t in tasks]})

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()
    if data and "task" in data:
        new_entry = UserTask(task_name=data["task"])
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data Saved Permanently!"}), 201
    return jsonify({"message": "Error"}), 400

if __name__ == "__main__":
    print("Talknik IT Server Starting at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
