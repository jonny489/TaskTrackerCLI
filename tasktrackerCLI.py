# Task Tracker CLI
import json
import argparse
from datetime import datetime
from typing import List

now = datetime.now().isoformat()
TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, title, description="", status="Not Done", updatedAt=now, createdAt=now):
        self.title = title
        self.description = description
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    def to_dict(self): #convert to dictionary
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    @staticmethod
    def from_dict(data): #convert from dictionary
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status"),
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt")
        )
    

def load_tasks() -> List[Task]: #get tasks out from the json file and put it into a list of task objects
    try:
        with open(TASKS_FILE, "r") as f:
            return [Task.from_dict(t) for t in json.load(f)]
    except FileNotFoundError:
        return []

def save_tasks(tasks: List[Task]): #convert tasks to dictionaries for easy input into the json file
    with open(TASKS_FILE, "w") as f:
        json.dump([t.to_dict() for t in tasks], f, indent=2)

def add_task(args): #add task
    tasks = load_tasks()
    task = Task(args.title, args.description)
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{args.title}' added.")

def list_all(args): #list all tasks
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return

    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task.title} - {task.description} (Status: {task.status})")

def list_done(args): #list finished tasks
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    done_tasks = [t for t in tasks if t.status == "Done"]
    if not done_tasks:
        print("No finished tasks yet!")
        return
    
    for task in tasks:
        if task.status == "Done":
            print(f"{task.title} - {task.description} (Status: {task.status})")

def list_inprogress(args): #list in progress tasks
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    done_tasks = [t for t in tasks if t.status == "Done"]
    if not done_tasks:
        print("No finished tasks yet!")
        return
    
    for task in tasks:
        if task.status == "In Progress":
            print(f"{task.title} - {task.description} (Status: {task.status})")

def list_notdone(args): #list in not done tasks
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet!")
        return
    done_tasks = [t for t in tasks if t.status == "Done"]
    if not done_tasks:
        print("No finished tasks yet!")
        return
    
    for task in tasks:
        if task.status == "Not Done":
            print(f"{task.title} - {task.description} (Status: {task.status})")


def delete_task(args): #delete a task
    tasks = load_tasks()
    index = args.index - 1  #convert to 0-based index

    if index < 0 or index >= len(tasks):
        print("Not a valid index!")
        return
    
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Task '{removed.title}' successfully deleted.")

def to_inprogress(args):
    tasks = load_tasks()
    index = args.index - 1

    if index < 0 or index >= len(tasks):
        print("Not a valid index!")
        return
    
    for i, task in enumerate(tasks):
        if i == index:
            task.status = "In Progress"
            task.updatedAt = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"Successfully set {task.title} to in progress! Keep it up!")

def complete_task(args):
    tasks = load_tasks()
    index = args.index - 1

    if index < 0 or index >= len(tasks):
        print("Not a valid index!")
        return
    
    for i, task in enumerate(tasks):
        if i == index:
            task.status = "Done"
            task.updatedAt = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"Successfully completed {task.title}! Nice Job!")
    


parser = argparse.ArgumentParser(description="Task Tracker CLI")
subparsers = parser.add_subparsers()

# Add command
parser_add = subparsers.add_parser("add")
parser_add.add_argument("title")
parser_add.add_argument("--description", default="")
parser_add.set_defaults(func=add_task)

# Set to in progress command
parser_inprogress = subparsers.add_parser("setinprogress")
parser_inprogress.add_argument("index", type=int)
parser_inprogress.set_defaults(func=to_inprogress)

# Complete command
parser_complete = subparsers.add_parser("complete")
parser_complete.add_argument("index", type=int)
parser_complete.set_defaults(func=complete_task)

# Delete command
parser_delete = subparsers.add_parser("delete")
parser_delete.add_argument("index", type=int)
parser_delete.set_defaults(func=delete_task)


# List all command
parser_list = subparsers.add_parser("listall")
parser_list.set_defaults(func=list_all)

# List done command
parser_list = subparsers.add_parser("listdone")
parser_list.set_defaults(func=list_done)

# List in progress command
parser_list = subparsers.add_parser("listinprogress")
parser_list.set_defaults(func=list_inprogress)

# List not done command
parser_list = subparsers.add_parser("listnotdone")
parser_list.set_defaults(func=list_notdone)

# Run
args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()