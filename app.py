from flask import *
from flask_restful import Api
app = Flask(__name__)

api = Api(app)

from datetime import timedelta
from flask_jwt_extended import JWTManager

# set up JWT
app.secret_key = "d37f705c269"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# endpoints / routes
from views.views import MemberSignup, MemberSignin, MemberProfile, AddDependant, ViewDependants, Laboratories, LabTest
api.add_resource(MemberSignup, '/api/member_signup')
api.add_resource(MemberSignin, '/api/member_signin')
api.add_resource(MemberProfile, '/api/member_profile')
api.add_resource(AddDependant, '/api/add_dependant')
api.add_resource(ViewDependants, '/api/view_dependant')
api.add_resource(Laboratories, '/api/laboratories')
api.add_resource(LabTest,'/api/lab_test')
if __name__  == "__main__":
 
    app.run(debug=True)