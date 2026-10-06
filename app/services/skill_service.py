from app.errors import ConflictError, NotFoundError
from app.mappers import skill_mapper
from app.repositories import SkillRepository


class SkillService:
    def __init__(self, session):
        self.skills = SkillRepository(session)

    def list_skills(self):
        return [skill_mapper.to_response(skill) for skill in self.skills.list()]

    def create_skill(self, dto):
        if self.skills.get_by_name(dto.name):
            raise ConflictError("Skill name already exists")
        return skill_mapper.to_response(self.skills.save(skill_mapper.to_model(dto)))

    def get_skill(self, skill_id):
        skill = self.skills.get(skill_id)
        if skill is None:
            raise NotFoundError("Skill not found")
        return skill_mapper.to_response(skill)
