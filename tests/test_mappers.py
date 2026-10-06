from app.dtos import UserCreateDTO
from app.mappers import user_mapper


def test_user_create_mapper_only_transforms_data():
    model = user_mapper.to_model(UserCreateDTO(name="Ada", email="ada@example.com"))

    assert model.name == "Ada"
    assert model.email == "ada@example.com"
    assert model.id is None
