from sqlalchemy import select

from app.models import Skill


class SkillRepository:
    def __init__(self, session):
        self.session = session

    def list(self):
        return self.session.scalars(select(Skill).order_by(Skill.id)).all()

    def get(self, skill_id):
        return self.session.get(Skill, skill_id)

    def get_by_name(self, name):
        return self.session.scalar(select(Skill).where(Skill.name == name))

    def save(self, skill):
        self.session.add(skill)
        self.session.commit()
        self.session.refresh(skill)
        return skill
