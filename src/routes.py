from flask import Blueprint

from src.controllers.staff_controller import staffs
from src.controllers.user_controller import users
from src.controllers.admin_controller import admin
from src.controllers.category_management_controller import category

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(users, url_prefix="/users")
api.register_blueprint(staffs, url_prefix="/staff")
api.register_blueprint(admin, url_prefix="/admin")
api.register_blueprint(category, url_prefix="/category")
