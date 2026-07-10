from flask import Flask, render_template, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor(dictionary=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    return jsonify(cursor.fetchall())


@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.json

    sql = """
    INSERT INTO tasks
    (title,description,priority,status,due_date)
    VALUES(%s,%s,%s,%s,%s)
    """

    values = (
        data["title"],
        data["description"],
        data["priority"],
        "pending",
        data["dueDate"]
    )

    cursor.execute(sql, values)
    db.commit()

    return jsonify({"success": True})


@app.route("/tasks/<int:id>", methods=["PUT"])
def complete_task(id):

    cursor.execute(
        "UPDATE tasks SET status='completed' WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({"success": True})


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (id,)
    )

    db.commit()

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)