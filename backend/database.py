# database management zone
from flask import jsonify
import mysql.connector
import bcrypt

# db connector
def ConnectorMysql():
    """
    Connects to the MySQL database and returns a connection object.

    Raises:
        RuntimeError: if there is an error connecting to the database.
    """
    try:
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="automoney",
        )
        return db
    except Exception as err:
        raise RuntimeError(f"Database error: {err}")

# method for fetch all data from database
def get_data():
    """
    Fetches all data from the user table in the database.

    Returns:
        list: A list of dictionaries containing the user data. Each dictionary contains the user's id, username, password, and email.

    Raises:
        RuntimeError: if there is an error connecting to the database or fetching the data.
    """
    try:
        db = ConnectorMysql()
        cursor = db.cursor()
        stmt = "SELECT * FROM user"
        cursor.execute(stmt)
        result = cursor.fetchall()
        if len(result) > 0:
            data = []
            for x in result:
                arr = {
                    "user_id" : x[0],
                    "username" : x[1],
                    "password" : x[2],
                    "email" : x[3]
                }
                data.append(arr)
        return data
    except Exception as err:
        raise RuntimeError(f"Database error: {err}")

# method register with username , password (encrypt with bcrypt function) and email
def register_db(username , password , email):
    """
    Registers a new user with a username, password, and email.

    Parameters:
        username (str): The username of the new user.
        password (str): The password of the new user.
        email (str): The email of the new user.

    Returns:
        tuple: A tuple containing a JSON response and a status code. The JSON response contains a success message and the status code is 200.

    Raises:
        RuntimeError: if there is an error connecting to the database or registering the user.
    """
    try:
        db = ConnectorMysql()
        cursor = db.cursor()
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) # encrypt password code
        stmt = "INSERT INTO user (username , password , email) VALUES (%s, %s, %s)"
        payload = (username , hashed , email)
        cursor.execute(stmt,payload)
        db.commit()
        return jsonify({"success": "Registered successfull"}), 200
    except Exception as err:
        raise RuntimeError(f"Database error: {err}")

# method get user from email
def get_from_email(email):
    try:
        db = ConnectorMysql()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, email FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as err:
        raise RuntimeError(f"Database error: {err}")

# method login with email and password
def login_db(email , password):
    """
    Logs in a user with their email and password.

    Parameters:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        tuple: A tuple containing a JSON response and a status code. The JSON response contains a success message and the status code is 200.

    Raises:
        RuntimeError: if there is an error connecting to the database or logging in the user.
    """
    try:
        db = ConnectorMysql()
        cursor = db.cursor()
        stmt = "SELECT * FROM user WHERE email=%s"
        cursor.execute(stmt, [email])
        result = cursor.fetchall()
        if len(result) > 0:
            for x in result:
                arr = {
                    "user_id" : x[0],
                    "username" : x[1],
                    "password" : x[2],
                    "email" : x[3]
                }
            if bcrypt.checkpw(password.encode("utf-8") , arr['password'].encode("utf-8")):
                return arr['email'], 200
            return jsonify({"error": "Wrong password!"}), 401
        return jsonify({"error": "Email doesn't exist!"}), 401
    except Exception as err:
        raise RuntimeError(f"Database error: {err}")
