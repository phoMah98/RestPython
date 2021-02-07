from flask import Flask, jsonify, request
from json import dump, dumps
import pymongo

app = Flask(__name__)
app.config["DEBUG"] = True

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]

employees = [
    {"_id": 0,
     "name": "Ahmad",
     "age": "22",
     "salary": "1500"
     },
    {""
     "_id": 1,
     "name": "Baraa",
     "age": "23",
     "salary": "1600"
     },
    {"_id": 2,
     "name": "Omar",
     "age": "24",
     "salary": "1800"
     },
    {"_id": 3,
     "name": "Haitham",
     "age": "20",
     "salary": "1500"
     },
]
Employees = mydb["Employees"]


def get_all_employees():
    employees_list = list(Employees.find())
    return employees_list


@app.route('/api/v1/resources/employees/all', methods=["GET"])
def get_all():
    employees_list = get_all_employees()
    employees_json_list = dumps(employees_list)
    return employees_json_list


@app.route('/api/v1/resources/employees/', methods=["GET"])
def get_employee():
    employees_list = get_all_employees()
    if 'id' in request.args:
        id = int(request.args['id'])
        exists = False
        for employee in employees_list:
            if id == employee["_id"]:
                exists = True
                break
        if not exists:
            return f"There is no employee with this id: {id}"
    else:
        return "Error: No id field provided. Please specify an id."

    return Employees.find_one({"_id": id})


@app.route('/api/v1/resources/employees/get_highest_salary_employee', methods=["GET"])
def get_highest_salary_employee():
    employees_list = get_all_employees()
    max_salary = 0
    highest_employee = None
    for employee in employees_list:
        if int(employee["salary"]) > int(max_salary):
            max_salary = employee["salary"]
            highest_employee = employee

    return highest_employee


@app.route('/api/v1/resources/employees/', methods=["POST"])
def add_employee():
    employees_list = get_all_employees()
    employee_details = request.get_json()

    try:
        id = int(employee_details["_id"])
        name = (employee_details["name"])
        age = int(employee_details["age"])
        salary = int(employee_details["salary"])
    except KeyError:
        return "You must specify '_id', 'Name', 'Age' and 'Salary' Fields!"

    except ValueError:
        return "'_id',Age and Salary must be Numeric value"

    for employee in employees_list:
        if id == employee["_id"]:
            return f"Employee with this id: {id}, Already Exists!"
    else:
        emp = {"_id": id,
               "name": name,
               "age": age,
               "salary": salary
               }
        Employees.insert_one(emp)

    return f"Employee with id: {id}, is Added Successfully!\n" + str(employee_details)


@app.route('/api/v1/resources/employees/', methods=["PUT"])
def update_employee():
    employees_list = get_all_employees()
    employee_details = request.get_json()

    if 'id' in request.args:
        id = int(request.args['id'])
        exists = False
        for employee in employees_list:
            if id == employee["_id"]:
                exists = True
                break
        if not exists:
            return f"There is no employee with this id: {id}"
    else:
        return "Error: No id field provided. Please specify an id."

    try:

        name = (employee_details["name"])
        age = int(employee_details["age"])
        salary = int(employee_details["salary"])
    except KeyError:
        return "You must specify '_id', 'Name', 'Age' and 'Salary' Fields!"

    except ValueError:
        return "'_id',Age and Salary must be Numeric value"

    else:
        emp = {"_id": id}
        new_values = {"$set": {"name": name,
                               "age": str(age),
                               "salary": str(salary)
                               }
                      }

        Employees.update_one(emp, new_values)

    return f"Employee with id: {id}, is Updated Successfully!\n"


@app.route('/api/v1/resources/employees/', methods=["DELETE"])
def delete_employee():
    employees_list = get_all_employees()
    if 'id' in request.args:
        id = int(request.args['id'])
        exists = False
        for employee in employees_list:
            if id == employee["_id"]:
                exists = True
                break
        if not exists:
            return f"There is no employee with this id: {id}"
    else:
        return "Error: No id field provided. Please specify an id."

    emp = {"_id": id}
    Employees.delete_one(emp)
    return f"Employee with id: {id}, is Deleted Successfully!\n"


app.run()
