from flask_restful import Api
from app import app
from .UserAPI import User
from .UserAPIbyID import UserAPIbyID

restServerInstance = Api(app)

restServerInstance.add_resource(User,"/api/v1.0/user")
restServerInstance.add_resource(UserAPIbyID,"/api/v1.0/user/id/<id>")