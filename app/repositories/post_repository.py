from sqlalchemy import select

from app.models import Post


class PostRepository:
    def __init__(self, session):
        self.session = session

    def list(self):
        return self.session.scalars(select(Post).order_by(Post.id)).all()

    def get(self, post_id):
        return self.session.get(Post, post_id)

    def save(self, post):
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete(self, post):
        self.session.delete(post)
        self.session.commit()
