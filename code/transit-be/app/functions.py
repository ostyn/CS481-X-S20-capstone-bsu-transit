from flask import jsonify, abort
from sqlalchemy import or_
from datetime import datetime, timedelta
from flask import current_app as app
import csv


from .models import *


#   Transit Service Functions

# --Employer CRUD Operations--
#   Return All Employers
def get_employers():
    try:
        employers = Employer.query.all()
        output = employer_schema.dump(employers, many=True)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not retrieve employers")


#   Add New Employer
def create_employer(json):
    try:
        name = json['name']
        email = json['email']
        rider_cap = json['rider_cap']
        employer = Employer(name,
                            email,
                            rider_cap)
        db.session.add(employer)
        db.session.commit()
        output = employer_schema.dump(employer)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(400, "Could not create new employer")
    #   Get Specified Employer


def get_employer(id):
    try:
        employer = Employer.query.get(id)
        output = employer_schema.dump(employer)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not retrieve employer")


#   Update Specified Employer
def update_employer(id, json):
    try:
        employer = Employer.query.get(id)
        employer.name = json['name']
        employer.email = json['email']
        employer.rider_cap = json['rider_cap']
        db.session.add(employer)
        db.session.commit()
        output = employer_schema.dump(employer)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not update employer")
    #   Delete Specified Employer


def delete_employer(id):
    try:
        employer = Employer.query.get(id)
        db.session.delete(employer)
        db.session.commit()
        return jsonify({'message': 'Employer deleted'})
    except Exception as e:
        print(e)
        abort(404, "Could not delete employer")

def _get_employer_id(employer_name):
    """
    This is a private helper method that will get the employer id
    from the table based on the employer name associated
    with that account.
    Parameters:
        employer_name: Name of the employer.
    Returns:
        employer_id: The id of the employer
    """
    try:
        employer_id = db.session.query(Employer.id).filter(employer_name == Employer.employer_name)

        return employer_id
    except Exception as e:
        print(e)
        abort(404, 'employer not found')

#-- Employee CRUD Operations

# -- Employee CRUD Operations

# -- VERIFICATION NOTES
# To test run python wsgi.py
# Send requests to the routes defined
# in routes.py that call the functions
# in this file
# Ensure that the databse is updated
# after accessing each end point if it
# should have updated the database

#   Add New Employee
def create_employee(json):
    try:
        name = json['name']
        email = json['email']
        employer_id = json['employer_id']
        success = json['success']
        employee = Employee(name,
                            email,
                            employer_id,
                            success)
        db.session.add(employee)
        db.session.commit()
        output = employee_schema.dump(employee)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(400, "Could not create new employee")

    #   Return All Employees


def get_employees():
    try:
        employees = Employee.query.all()
        output = employee_schema.dump(employees, many=True)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not retrieve employees")

    #   Get Specified Employee


def get_employee(id):
    try:
        employee = Employee.query.get(id)
        output = employee_schema.dump(employee)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not retrieve employee")


#   Get Employers Employees
def get_employer_employees(id):
    try:
        employees = Employee.query.filter_by(employer_id=id).all()
        output = employee_schema.dump(employees, many=True)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not get employer's employees")


#   Update Specified Employee
def update_employee(id, json):
    try:
        employee = Employee.query.get(id)
        employee.name = json['name']
        employee.email = json['email']
        employee.employer_id = json['employer_id']
        success = json['success']
        db.session.add(employee)
        db.session.commit()
        output = employee_schema.dump(employee)
        return jsonify(output)
    except Exception as e:
        print(e)
        abort(404, "Could not update employee")

    #   Delete Specified Employee


def delete_employee(id):
    try:
        employee = Employee.query.get(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted'})
    except Exception as e:
        print(e)
        abort(404, "Could not delete employee")


def issue_tickets(employer_id):
    try:
        # TODO: A masabi call to issue tickets to the employee
        # we should probably use the issue_date that is returned from the masabi API call(s) that would happen, but for right now I'm using this one datetime
        issue_date = datetime.utcnow()

        employees = Employee.query.filter(Employee.employer_id == employer_id).all()
        for employee in employees:
            if not employee.success:
                # single masabi calls would occur here, if successful then create issued table entry + update employee
                issue = Issued(issue_date, employee.id, employer_id)
                db.session.add(issue)
                if issue:
                    employee.success = True

        db.session.commit()
        return jsonify(employee_schema.dump(employees, many=True))
    except Exception as e:
        print(e)
        abort(500, "how did we get here")


def get_tickets(employer_id):
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=31)
        issued_tickets = Issued.query.filter(Issued.issue_date > cutoff_date).all()

        return jsonify(issued_schema.dump(issued_tickets))
    except Exception as e:
        print(e)
        abort(500, "an exception here is shameful")



def get_reissue_list():
    """
    This is a method to get a list of all the employees that
    have either been unsuccessful or their issued ticket is
    passed 31 days.
    """
    try:
        reissue_date = datetime.utcnow() - timedelta(days=31)
        reissue_list = db.session.query(Employee).join(Issued,
                                                       Employee.id == Issued.employee_id).filter(or_(
            Employee.success == False, Issued.issue_date < reissue_date))
        return reissue_list
    except Exception as e:
        print(e)
        # TODO: this needs to be added to a log


def push_nightly_tickets(need_issued_list):
    """
    Pushes the nightly tickets
    """
    for employee in need_issued_list:
        try:
            pass
            #TODO: this is where all the code for the api will go.
        except Exception as e:
            print(e)
            insert_error(employee.id, e)
        # going to have to catch specific exceptions coming from masabi at later dates


def insert_error(employee_id, error_message):
    """
    This method will insert an error into the database for logging.
    If the employee exists in the table currently, then that persons
    error message will be over written keeping the most recent record only.
    """
    error = db.session.query(Error).get(employee_id)
    if error:
        error.error_message = error_message
        db.session.commit()
    else:
        new_error = Error(error_message, employee_id)
        db.session.add(new_error)
        db.session.commit()

def parse_new_csv(csv_file, employer_name):
    """
    A method to parse the new csv file input by the admin or the employer.
    The csv file should have two columns, name and email.
    Parameters:
        csv_file: CSV file to be parsed.
        employer_name: Name of the employer that is inputting the data in order to get the id.
    """
    employer_id = _get_employer_id(employer_name)
    with open(csv_file, newline='') as file:
        csv_dict = csv.DictReader(f=file, fieldnames=['name', 'email'])
        for row in csv_dict:
            try:
                employee = Employee(row['name'], row['email'], employer_id, False)
                db.session.add(employee)
                db.session.commit()
            except Exception as e:
                print(e)
                #TODO: this needs to be logged for an error inputting a user.


