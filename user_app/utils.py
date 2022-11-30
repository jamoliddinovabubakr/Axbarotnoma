import re

from user_app.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

USERNAME_MIN_LENGTH = 5


def validate_username(username):
    if User.objects.filter(username=username).exists():
        return {
            "success": False,
            "reason": "Username already exists",
        }

    if len(username.replace("/", "")) < USERNAME_MIN_LENGTH:
        return {
            "success": False,
            "reason": f"Username character less {USERNAME_MIN_LENGTH}",
        }

    if not username.isalnum():

        return {
            "success": False,
            "reason": "Matriculation number should be alphanumeric",
        }

    return {
        "success": True,
    }


def validate_email(email):
    if User.objects.filter(email=email).exists():
        return {"success": False, "reason": "Email Address already exists"}
    if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email):
        return {"success": False, "reason": "Invalid Email Address"}
    if email is None:
        return {"success": False, "reason": "Email is required."}
    return {"success": True}