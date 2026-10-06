from app.models import Skill


def to_model(dto):
    return Skill(name=dto.name)


def to_response(skill):
    return {"id": skill.id, "name": skill.name}
