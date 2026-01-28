from app.auth.repository import (
    get_user_by_provider,
    create_user,
    create_local_user,
    get_user_by_username,
    count_users
)
from werkzeug.security import generate_password_hash, check_password_hash


def get_or_create_user(profile, provider):
    provider_id = profile["id"]
    email = profile["email"]
    username = email.split("@")[0]

    user = get_user_by_provider(provider, provider_id)
    if user:
        return user

    return create_user({
        "username": username,
        "email": email,
        "provider": provider,
        "provider_id": provider_id
    })


def generate_username(full_name: str) -> str:
    parts = full_name.strip().lower().split()
    return f"{parts[0]}.{parts[-1]}"

def register_user(form):
    if form["password"] != form["password_confirm"]:
        raise ValueError("As senhas não conferem")

    username = generate_username(form["full_name"])

    password_hash = generate_password_hash(form["password"])

    is_first_user = count_users() == 0

    return create_local_user({
        "username": username,
        "email": form["email"],
        "full_name": form["full_name"],
        "matricula": form["matricula"],
        "setor": form["setor"],
        "password_hash": password_hash,
        "is_active": is_first_user,
        "is_admin": is_first_user
    })



def authenticate_local(username, password):
    user = get_user_by_username(username)
    if not user:
        return None
    if not user["is_active"]:
        return "PENDING"
    if not check_password_hash(user["password_hash"], password):
        return None
    return user
