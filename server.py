from flask import Flask, request, jsonify
import os
import uuid
from db import database

app = Flask(__name__)
db = database(os.path.abspath(os.getcwd()))


@app.route("/todo", methods=['GET'])
def get_entries():
    entries = list(db.read_file('entries'))
    return jsonify(entries), 200


@app.route("/todo/<int:entry_id>", methods=['GET'])
def get_entry(entry_id):
    entries = db.read_file('entries')

    for entry in entries:  # get event by id
        if entry['id'] == entry_id:
            return jsonify(entry)
    return jsonify("No Entry with ID " + str(entry_id)), 404


@app.route("/todo", methods=['POST'])
def post_entry():
    entries = list(db.read_file('entries'))
    event_id = int(str(uuid.uuid1().int)[:6])
    data = request.get_json()

    # description is required
    if data['description'] == '':
        return jsonify("'description' cannot be empty."), 400

    # set and fill data-structure
    data = {
        "id": event_id,
        "description": data['description'],
        "due-date": data['due-date'],
        "done": False,
        "priority": data['priority']
    }
    # append to existing list and write into file
    entries.append(data)
    db.write_file('entries', entries)
    return jsonify(entries), 201


@app.route("/todo/<int:entry_id>", methods=['PATCH'])
def patch_entry(entry_id):
    entries = db.read_file('entries')

    #  if entry with id exists: patch it and update .json file
    for entry in entries:
        if entry['id'] == entry_id:
            entry['done'] = True
            db.write_file('entries', entries)
            return jsonify(entry), 204
    return jsonify('No Entry with ID: ' + str(entry_id) + ' found.'), 404


@app.route("/todo/<int:entry_id>", methods=['DELETE'])
def delete_entry(entry_id):
    entries = db.read_file('entries')

    #  if entry with id exists: delete it and update .json file
    for i, entry in enumerate(entries):
        if entry['id'] == entry_id:
            del entries[i]
            db.write_file('entries', entries)
            return jsonify("Entry with ID: " + str(entry_id) + " has been deleted."), 204
    return jsonify('No Entry with ID: ' + str(entry_id) + ' found.'), 404


if __name__ == '__main__':
    app.run(use_reloader=False)
