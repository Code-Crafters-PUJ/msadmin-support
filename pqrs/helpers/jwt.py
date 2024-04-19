from typing import Any

import jwt

from config.settings import SECRET_KEY


def validate_role(token: str, role: str) -> bool:
    payload: dict[str, Any]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(payload)
    except jwt.InvalidTokenError:
        return False

    if payload["role"] != role:
        return False
    return True


def validate_admin_role(token: str) -> bool:
    return validate_role(token, "ADMIN")


def validate_soporte_role(token: str) -> bool:
    return validate_role(token, "SOPORTE")
