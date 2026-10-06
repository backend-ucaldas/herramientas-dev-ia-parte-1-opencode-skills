from dataclasses import dataclass

from app.errors import ValidationError


def _object(payload):
    if not isinstance(payload, dict):
        raise ValidationError("JSON object body is required")
    return payload


def _text(payload, field, required=True):
    value = payload.get(field)
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"'{field}' must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class UserCreateDTO:
    name: str
    email: str

    @classmethod
    def from_payload(cls, payload):
        payload = _object(payload)
        return cls(_text(payload, "name"), _text(payload, "email"))


@dataclass(frozen=True)
class UserUpdateDTO:
    name: str | None
    email: str | None

    @classmethod
    def from_payload(cls, payload):
        payload = _object(payload)
        value = cls(_text(payload, "name", False), _text(payload, "email", False))
        if value.name is None and value.email is None:
            raise ValidationError("At least one updatable field is required")
        return value


@dataclass(frozen=True)
class ProfileUpsertDTO:
    bio: str

    @classmethod
    def from_payload(cls, payload):
        return cls(_text(_object(payload), "bio"))


@dataclass(frozen=True)
class PostCreateDTO:
    title: str
    content: str

    @classmethod
    def from_payload(cls, payload):
        payload = _object(payload)
        return cls(_text(payload, "title"), _text(payload, "content"))


@dataclass(frozen=True)
class PostUpdateDTO:
    title: str | None
    content: str | None

    @classmethod
    def from_payload(cls, payload):
        payload = _object(payload)
        value = cls(_text(payload, "title", False), _text(payload, "content", False))
        if value.title is None and value.content is None:
            raise ValidationError("At least one updatable field is required")
        return value


@dataclass(frozen=True)
class SkillCreateDTO:
    name: str

    @classmethod
    def from_payload(cls, payload):
        return cls(_text(_object(payload), "name"))
