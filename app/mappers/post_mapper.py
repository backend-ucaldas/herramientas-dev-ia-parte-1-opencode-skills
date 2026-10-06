from app.models import Post


def to_model(dto, user_id):
    return Post(title=dto.title, content=dto.content, user_id=user_id)


def apply_update(post, dto):
    if dto.title is not None:
        post.title = dto.title
    if dto.content is not None:
        post.content = dto.content
    return post


def to_response(post):
    return {"id": post.id, "title": post.title, "content": post.content, "user_id": post.user_id}
