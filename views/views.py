import pymysql
from flask_restful import Resource
from flask import *

from functions import *
#  Add a member class
# member_signup and member_signin
class MemberSignup(Resource):
    def post(self):
        # Get the data from the client
        data = request.json
        surname = data["surname"]
        others = data["others"]
        gender= data["gender"]
        email = data["email"]
        phone = data["phone"]
        dob = data["dob"]
        status = data["status"]
        password = data["password"]
        location_id = data["location_id"]

        # check if password is valid
        response = password_validity(password)
        if response == True:
            # connectt to database
            connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
            cursor = connection.cursor()
            # insert into db
            sql = "INSERT INTO member(surname, others, gender, email, phone, dob, status, password, location_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (surname, others,gender,email,phone,dob,status,hash_password(password),location_id)
            try:
                cursor.execute(sql,data)
                connection.commit()
                send_sms(phone, "Registration successful")
                return ({"Message":"Post successful. Member saved"})
            except:
                connection.rollback()
                return jsonify({"Message":"Post failed. Member not saved"})
        else:
            return jsonify({"Message": response})
        
class MemberSignin(Resource):
    def post(self):
        # we want to get request from client
        data = request.json
        email = data["email"]
        password = data["password"]
        # connect to database
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        
        # check if email exists
        sql = "select * from member where email = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, email)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Email does not exist"})
        else:
            # check password
            member = cursor.fetchone()
            hashed_password = member["password"]
            is_match_password = hash_verify(password, hashed_password)
            if is_match_password == True:
                return jsonify({"Message": "Login successful"})
            elif is_match_password == False:
                return jsonify({"Message": "Login failed"})
            else:
                return jsonify({"Message": "Something went wrong"})
            
class MemberProfile(Resource):
    def post(self):
        data = request.json
        member_id = data["member_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from member where member_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Member does not exist"})
        else:
            member = cursor.fetchone()
            return jsonify({"message":member})
