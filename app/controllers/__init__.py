from app.controllers.posts import blueprint as posts_blueprint
from app.controllers.skills import blueprint as skills_blueprint
from app.controllers.users import blueprint as users_blueprint


def register_blueprints(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(skills_blueprint)
