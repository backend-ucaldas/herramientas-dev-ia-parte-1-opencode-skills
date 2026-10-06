from sqlalchemy import select

from app.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def list(self):
        return self.session.scalars(select(User).order_by(User.id)).all()

    def get(self, user_id):
        return self.session.get(User, user_id)

    def get_by_email(self, email):
        return self.session.scalar(select(User).where(User.email == email))

    def save(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user):
        self.session.delete(user)
        self.session.commit()
