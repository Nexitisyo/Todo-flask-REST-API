from flask import Flask, request, render_template
import os
import uuid
from db import database

app = Flask(__name__)
db = database(os.path.abspath(os.getcwd()))

desc_err = "Description cannot be empty."
entry_add = "Entry has been added."
status_class = ['badge badge-success', 'badge badge-danger']


@app.route("/todo", methods=['GET', 'POST', 'DELETE', 'PATCH'])
def todo():
    entries = list(db.read_file('entries'))

    if request.method == 'GET':
        return render_template("index.html", entries=entries, status="")  # show all entries

    if request.method == 'POST':
        id = int(str(uuid.uuid1().int)[:6])

        # description is required
        if request.form["description"] == '':
            return render_template("index.html", entries=entries, status=desc_err, status_class=status_class[1])

        # set and fill data-structure
        data = {
            "id": id,
            "description": request.form["description"],
            "due_date": request.form["due_date"],
            "done": False,
            "priority": request.form["priority"]
        }
        # append to existing list and write into file
        entries.append(data)
        db.write_file('entries', entries)
        return render_template("index.html", entries=entries, status=entry_add, status_class=status_class[0])

    if request.method == 'PATCH':
        for entry in entries:
            if entry["id"] == request.form["id"]:
                entry["done"] = True

    if request.method == 'DELETE':
        for entry in entries:
            if entry["id"] == request.form["id"]:
                del entry


@app.route("/todo/<int:entry_id>", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def todo_single(entry_id):
    entries = db.read_file('entries')
    if request.method == 'GET':
        for entry in entries:
            if entry["id"] == entry_id:
                return render_template("single_view.html", entry=entry)
        return "No Entry with ID " + str(entry_id)


if __name__ == '__main__':
    app.run(use_reloader=False)
