from flask import Flask , request , jsonify , make_response
from datetime import timedelta
from flask_cors import CORS
import database #
import traceback
import secrets

from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
    supports_credentials=True,
) # this cors code by chatgpt

app.secret_key = secrets.token_hex(32)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SAMESITE"] = "Lax" # code by chatgpt
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

# for test api is working?
@app.route('/')
def hello_world():
    """
    Test API is working
    Returns:
        str: API Is Working
    """
    return 'Api Is Working'

# example of get_data method
@app.route('/data' , methods=['GET'])
def data():
    """
    Get all data from user table in database
    Returns:
        json: All data from user table
    Raises:
        Exception: If there is an error in database
    """
    try:
        jsonData = database.get_data()
        return jsonify(jsonData)
    except Exception as err:
        traceback.print_exc()
        return jsonify({"error": str(err)}), 500

# register api use function register_db from ./database.py (finished)
@app.route('/register' , methods=["POST"])
def register():
    """
    Register new user
    Returns:
        json: Message if register successfull or error message
    Raises:
        Exception: If there is an error in database
    Parameters:
        username (str): Username of new user
        password (str): Password of new user
        email (str): Email of new user
    """
    try:
        data = request.get_json() # get data from header (json file)
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        result = database.register_db(username,password,email)
        return result
    except Exception as err:
        traceback.print_exc()
        return jsonify({"error": str(err)}), 500

# login method use fuction login_db from ./database.py (not finished)
@app.route('/login' , methods=["POST"])
def login():
    """
    Login user
    Returns:
        json: Message if login successfull or error message
    Raises:
        Exception: If there is an error in database
    Parameters:
        email (str): Email of user
        password (str): Password of user
    """
    try:
        data = request.get_json() # get data from header (json file)
        email = data.get("email").strip().lower()
        password = data.get("password")
        result = database.login_db(email,password)
        if result[1] == 200:
            user_email = result[0]
            access_token = create_access_token(identity=user_email)
            resp = jsonify({"success": "login successful", "expires_in_sec": 3600})
            set_access_cookies(resp, access_token)
            return resp, 200
        return result
    except Exception as err:
        traceback.print_exc()
        return jsonify({"error": str(err)}), 500

# this function code by chatgpt
@app.route("/auth", methods=["GET"])
@jwt_required()
def auth():
    try:
        email = get_jwt_identity()
        user = database.get_from_email(email)
        if not user:
            return jsonify({"authenticated": False}),200
        return jsonify({"authenticated": True, "user": user}), 200
    except Exception as err:
        traceback.print_exc()
        return jsonify({"error": str(err)}), 500

# logout method
@app.route("/logout", methods=["GET"])
def logout():
    """
    Logout user
    Returns:
        json: Message if logout successfull
    """
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# protected method for use auth you login (this function code by chatgpt)
@app.route("/protected")
@jwt_required()
def protected():
    """
    A protected endpoint which can only be accessed if a valid JWT is provided.

    Returns:
        json: A simple JSON response with a message indicating that the request was successful
    """
    return jsonify(foo="bar")

# running file
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
