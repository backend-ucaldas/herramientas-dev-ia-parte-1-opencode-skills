from app.models import Profile


def to_model(dto, user_id):
    return Profile(bio=dto.bio, user_id=user_id)


def apply_update(profile, dto):
    profile.bio = dto.bio
    return profile


def to_response(profile):
    return {"id": profile.id, "bio": profile.bio, "user_id": profile.user_id}
