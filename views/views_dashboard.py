# import required modules
import pymysql
from flask_restful import *
from flask import *
from functions import *
import pymysql.cursors

# jwt packages
from flask_jwt_extended import create_access_token,create_refresh_token, jwt_required
# lab signup resource
class LabSignup(Resource):
    def post(self):
        data = request.json
        lab_name = data["lab_name"]
        email = data["email"]
        phone = data["phone"]
        permit_id = data["permit_id"]
        password = data["password"]

        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        cursor = connection.cursor()

        response = password_validity(password)
        if response:
            if check_phone(phone):
                # phone is correct
                sql = "INSERT INTO laboratories(lab_name,email,phone,permit_id,password) VALUES(%s,%s,%s,%s,%s)"
                data = (lab_name,email,encypt(phone),permit_id,hash_password(password))

                try:
                    cursor.execute(sql,data)
                    connection.commit()
                    code = gen_random()
                    send_sms(phone, '''Thankyou for joining medilab.
                             Your secret No: {}. Do not share. '''. format(code))
                    return jsonify({"message":"Lab signup successfull"})
                except:
                    connection.rollback()
                    return jsonify({"message":"lab signup failed"})

            else:
                # phone is not in correct format
                return jsonify({"message":"Invalid phone enter +254.."})    

        else:
           return jsonify({"message":response})