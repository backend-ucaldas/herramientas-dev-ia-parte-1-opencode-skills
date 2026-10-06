from app.models import User


def to_model(dto):
    return User(name=dto.name, email=dto.email)


def apply_update(user, dto):
    if dto.name is not None:
        user.name = dto.name
    if dto.email is not None:
        user.email = dto.email
    return user


def to_response(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "profile": None if user.profile is None else {"id": user.profile.id, "bio": user.profile.bio},
        "skills": [{"id": skill.id, "name": skill.name} for skill in user.skills],
    }
