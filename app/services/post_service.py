from app.errors import NotFoundError
from app.mappers import post_mapper
from app.repositories import PostRepository, UserRepository


class PostService:
    def __init__(self, session):
        self.posts = PostRepository(session)
        self.users = UserRepository(session)

    def list_posts(self):
        return [post_mapper.to_response(post) for post in self.posts.list()]

    def get_post(self, post_id):
        return post_mapper.to_response(self._post_or_404(post_id))

    def create_post(self, user_id, dto):
        if self.users.get(user_id) is None:
            raise NotFoundError("User not found")
        return post_mapper.to_response(self.posts.save(post_mapper.to_model(dto, user_id)))

    def update_post(self, post_id, dto):
        return post_mapper.to_response(self.posts.save(post_mapper.apply_update(self._post_or_404(post_id), dto)))

    def delete_post(self, post_id):
        self.posts.delete(self._post_or_404(post_id))

    def _post_or_404(self, post_id):
        post = self.posts.get(post_id)
        if post is None:
            raise NotFoundError("Post not found")
        return post
