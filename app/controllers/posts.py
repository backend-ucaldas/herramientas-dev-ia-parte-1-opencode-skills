from flask import Blueprint, current_app, jsonify, request

from app.dtos import PostCreateDTO, PostUpdateDTO
from app.services import PostService

blueprint = Blueprint("posts", __name__)


def service():
    return PostService(current_app.extensions["db_session"])


@blueprint.get("/posts")
def list_posts():
    return jsonify(service().list_posts())


@blueprint.post("/users/<int:user_id>/posts")
def create_post(user_id):
    post = service().create_post(user_id, PostCreateDTO.from_payload(request.get_json(silent=True)))
    return jsonify(post), 201


@blueprint.get("/posts/<int:post_id>")
def get_post(post_id):
    return jsonify(service().get_post(post_id))


@blueprint.put("/posts/<int:post_id>")
def update_post(post_id):
    post = service().update_post(post_id, PostUpdateDTO.from_payload(request.get_json(silent=True)))
    return jsonify(post)


@blueprint.delete("/posts/<int:post_id>")
def delete_post(post_id):
    service().delete_post(post_id)
    return "", 204
