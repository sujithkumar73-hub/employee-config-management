from flask import abort
from backend.database.db import db
from backend.models.employee import Employee
from backend.utils.validation import validate_employee_data


def create_employee(payload: dict):
    data = validate_employee_data(payload)
    if Employee.query.filter_by(email=data["email"]).first():
        abort(400, description="Employee with this email already exists")

    employee = Employee(**data)
    db.session.add(employee)
    db.session.commit()
    return employee


def get_all_employees():
    return [employee.to_dict() for employee in Employee.query.order_by(Employee.created_at.desc()).all()]


def get_employee_by_id(employee_id: int):
    employee = Employee.query.get(employee_id)
    if not employee:
        abort(404, description="Employee not found")
    return employee


def update_employee(employee_id: int, payload: dict):
    employee = get_employee_by_id(employee_id)
    data = validate_employee_data(payload, update=True)
    for key, value in data.items():
        setattr(employee, key, value)
    db.session.commit()
    return employee


def delete_employee(employee_id: int):
    employee = get_employee_by_id(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return True
