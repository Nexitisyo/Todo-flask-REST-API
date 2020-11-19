import requests
import sys
import argparse
import datetime

URL = "http://localhost:5000/todo"

parser = argparse.ArgumentParser(description="Todo App")
exclusive = parser.add_mutually_exclusive_group()
exclusive.add_argument('-a', '--get_all', action="store_true", help="Returns every entry")
exclusive.add_argument('-e', '--entry', help="Returns entry by ID")
exclusive.add_argument('-n', '--new', action="store", nargs=3, required=False, help="Returns every entry")  # -new description due-date priority
exclusive.add_argument('-c', '--check', help="Sets entry to done")
exclusive.add_argument('-d', '--delete', help="Deletes an entry by ID")
args = parser.parse_args()

# 126078


def main():
    if args.get_all:
        get_entries()
    if args.entry:
        get_entry(args.entry)
    if args.check:
        patch_entry(args.check)
    if args.delete:
        delete_entry(args.delete)
    if args.new:
        print(args.new)
        post_entry(args.new[0], args.new[1], args.new[2])


def get_entries():
    r = requests.get(url=URL)
    data = r.json()
    print(data)


def get_entry(entry_id):
    r = requests.get(url=URL + "/" + entry_id)
    data = r.json()
    print(data, r)


def post_entry(description, due_date=None, priority=None):
    data = {
        "description": description,
        "due-date": str(datetime.datetime.strptime(due_date, '%d.%m.%Y/%H:%M').astimezone().isoformat()),
        "priority": priority
    }
    r = requests.post(url=URL, json=data)
    print("Entry has been added.", r)


def patch_entry(entry_id):
    r = requests.patch(url=URL + "/" + entry_id)
    print("Entry " + entry_id + " set to done.", r)


def delete_entry(entry_id):
    r = requests.delete(url=URL + "/" + entry_id)
    print("Entry " + entry_id + " deleted.", r)


if __name__ == '__main__':
    main()
