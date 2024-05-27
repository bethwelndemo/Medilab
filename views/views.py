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
            data = (surname, others,gender,email,phone,dob,status,password,location_id)
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