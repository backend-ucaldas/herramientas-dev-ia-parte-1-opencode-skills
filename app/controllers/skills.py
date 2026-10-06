from flask import Blueprint, current_app, jsonify, request

from app.dtos import SkillCreateDTO
from app.services import SkillService

blueprint = Blueprint("skills", __name__, url_prefix="/skills")


def service():
    return SkillService(current_app.extensions["db_session"])


@blueprint.get("")
def list_skills():
    return jsonify(service().list_skills())


@blueprint.post("")
def create_skill():
    skill = service().create_skill(SkillCreateDTO.from_payload(request.get_json(silent=True)))
    return jsonify(skill), 201


@blueprint.get("/<int:skill_id>")
def get_skill(skill_id):
    return jsonify(service().get_skill(skill_id))
