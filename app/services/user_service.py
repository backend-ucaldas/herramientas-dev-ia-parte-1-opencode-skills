from app.errors import ConflictError, NotFoundError
from app.mappers import profile_mapper, user_mapper
from app.repositories import ProfileRepository, SkillRepository, UserRepository


class UserService:
    def __init__(self, session):
        self.users = UserRepository(session)
        self.profiles = ProfileRepository(session)
        self.skills = SkillRepository(session)

    def list_users(self):
        return [user_mapper.to_response(user) for user in self.users.list()]

    def get_user(self, user_id):
        return user_mapper.to_response(self._user_or_404(user_id))

    def create_user(self, dto):
        if self.users.get_by_email(dto.email):
            raise ConflictError("Email is already registered")
        return user_mapper.to_response(self.users.save(user_mapper.to_model(dto)))

    def update_user(self, user_id, dto):
        user = self._user_or_404(user_id)
        if dto.email is not None and dto.email != user.email and self.users.get_by_email(dto.email):
            raise ConflictError("Email is already registered")
        return user_mapper.to_response(self.users.save(user_mapper.apply_update(user, dto)))

    def delete_user(self, user_id):
        self.users.delete(self._user_or_404(user_id))

    def upsert_profile(self, user_id, dto):
        self._user_or_404(user_id)
        profile = self.profiles.get_by_user_id(user_id)
        if profile is None:
            profile = profile_mapper.to_model(dto, user_id)
        else:
            profile_mapper.apply_update(profile, dto)
        return profile_mapper.to_response(self.profiles.save(profile))

    def assign_skill(self, user_id, skill_id):
        user = self._user_or_404(user_id)
        skill = self.skills.get(skill_id)
        if skill is None:
            raise NotFoundError("Skill not found")
        if skill in user.skills:
            raise ConflictError("Skill is already assigned to user")
        user.skills.append(skill)
        return user_mapper.to_response(self.users.save(user))

    def remove_skill(self, user_id, skill_id):
        user = self._user_or_404(user_id)
        skill = self.skills.get(skill_id)
        if skill is None or skill not in user.skills:
            raise NotFoundError("Skill assignment not found")
        user.skills.remove(skill)
        self.users.save(user)

    def _user_or_404(self, user_id):
        user = self.users.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user
