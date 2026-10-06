from app.models import Profile


class ProfileRepository:
    def __init__(self, session):
        self.session = session

    def get_by_user_id(self, user_id):
        return self.session.query(Profile).filter_by(user_id=user_id).one_or_none()

    def save(self, profile):
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile
