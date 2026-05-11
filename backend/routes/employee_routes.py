from flask import Blueprint, request, jsonify
from backend.controllers.employee_controller import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
)
from backend.middleware.auth_middleware import jwt_required_api

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/", methods=["GET"])
@jwt_required_api
def list_employees():
    employees = get_all_employees()
    return jsonify({"status": "success", "data": employees}), 200


@employee_bp.route("/", methods=["POST"])
@jwt_required_api
def add_employee():
    payload = request.get_json(force=True)
    employee = create_employee(payload)
    return jsonify({"status": "success", "data": employee.to_dict()}), 201


@employee_bp.route("/<int:employee_id>", methods=["GET"])
@jwt_required_api
def get_employee(employee_id):
    employee = get_employee_by_id(employee_id)
    return jsonify({"status": "success", "data": employee.to_dict()}), 200


@employee_bp.route("/<int:employee_id>", methods=["PUT"])
@jwt_required_api
def modify_employee(employee_id):
    payload = request.get_json(force=True)
    employee = update_employee(employee_id, payload)
    return jsonify({"status": "success", "data": employee.to_dict()}), 200


@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
@jwt_required_api
def remove_employee(employee_id):
    delete_employee(employee_id)
    return jsonify({"status": "success", "message": "Employee removed"}), 200
