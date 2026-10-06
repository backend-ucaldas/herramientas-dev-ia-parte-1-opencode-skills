from flask import Blueprint, current_app, jsonify, request

from app.dtos import ProfileUpsertDTO, UserCreateDTO, UserUpdateDTO
from app.services import UserService

blueprint = Blueprint("users", __name__, url_prefix="/users")


def service():
    return UserService(current_app.extensions["db_session"])


@blueprint.get("")
def list_users():
    return jsonify(service().list_users())


@blueprint.post("")
def create_user():
    user = service().create_user(UserCreateDTO.from_payload(request.get_json(silent=True)))
    return jsonify(user), 201


@blueprint.get("/<int:user_id>")
def get_user(user_id):
    return jsonify(service().get_user(user_id))


@blueprint.put("/<int:user_id>")
def update_user(user_id):
    user = service().update_user(user_id, UserUpdateDTO.from_payload(request.get_json(silent=True)))
    return jsonify(user)


@blueprint.delete("/<int:user_id>")
def delete_user(user_id):
    service().delete_user(user_id)
    return "", 204


@blueprint.put("/<int:user_id>/profile")
def upsert_profile(user_id):
    profile = service().upsert_profile(user_id, ProfileUpsertDTO.from_payload(request.get_json(silent=True)))
    return jsonify(profile)


@blueprint.post("/<int:user_id>/skills/<int:skill_id>")
def assign_skill(user_id, skill_id):
    return jsonify(service().assign_skill(user_id, skill_id))


@blueprint.delete("/<int:user_id>/skills/<int:skill_id>")
def remove_skill(user_id, skill_id):
    service().remove_skill(user_id, skill_id)
    return "", 204
