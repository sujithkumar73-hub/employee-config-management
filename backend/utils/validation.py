from flask import abort


def validate_employee_data(payload: dict, update: bool = False):
    required_fields = ["name", "email", "department", "designation", "salary"]
    if not isinstance(payload, dict):
        abort(400, description="Invalid payload format")

    cleaned = {}
    for field in required_fields:
        value = payload.get(field)
        if not update and (value is None or str(value).strip() == ""):
            abort(400, description=f"{field} is required")
        if value is not None:
            cleaned[field] = value.strip() if isinstance(value, str) else value

    if "salary" in cleaned:
        try:
            cleaned["salary"] = float(cleaned["salary"])
        except (ValueError, TypeError):
            abort(400, description="Salary must be a valid number")

    if "email" in cleaned and "@" not in cleaned["email"]:
        abort(400, description="Email address is invalid")

    return cleaned
