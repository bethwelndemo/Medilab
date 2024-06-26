import pymysql
from flask_restful import Resource
from flask import *
# import JWT packages
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required


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
                access_token = create_access_token(identity=member, fresh=True)
                return jsonify({"access_token":access_token,'member':member})
            elif is_match_password == False:
                return jsonify({"Message": "Login failed"})
            else:
                return jsonify({"Message": "Something went wrong"})
            
class MemberProfile(Resource):
    @jwt_required(fresh=True)
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

class AddDependant (Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        member_id = data["member_id"]
        surname = data["surname"]
        others = data["others"]
        dob  = data["dob"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        cursor = connection.cursor()
        sql = "insert into dependants (member_id, surname, others, dob) values (%s, %s, %s, %s)"
        data = (member_id, surname, others,dob)
        try:
            cursor.execute(sql, data)
            connection.commit()
            return jsonify({"Message":"POST SUCCESSFUL. Dependant saved"})

        except:
            connection.rollback
            return jsonify({"Message":"POST FAILED. Dependant not saved"})

class ViewDependants(Resource):
    @jwt_required(fresh=True)
    def post(self):
        data = request.json
        member_id = data["member_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from dependants where member_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Member does not exist"})
        else:
            member = cursor.fetchall()
            return jsonify({"message":member})

class Laboratories(Resource):
    def get(self):
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from laboratories"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return jsonify({"Message":"No laboratories"})
        else:
            labs = cursor.fetchall()
            return jsonify(labs)

class LabTest(Resource):
    def post(self):
        data = request.json
        lab_id = data["lab_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from lab_tests where lab_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, lab_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "No lab test found"})
        else:
            lab = cursor.fetchall()
            return jsonify({"message":lab})

class MakeBooking(Resource):
    def post(self):
        data = request.json
        member_id = data["member_id"]
        booked_for = data["booked_for"]
        dependant_id = data["dependant_id"]
        test_id = data["test_id"]
        appointment_date = data["appointment_date"]
        appointment_time = data["appointment_time"]
        where_taken = data["where_taken"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        status = data["status"]
        lab_id = data["lab_id"]
        invoice_no = data["invoice_no"]
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        cursor = connection.cursor()
        sql = "insert into bookings(member_id, booked_for, dependant_id, test_id, appointment_date, appointment_time, where_taken, latitude, longitude, status, lab_id, invoice_no) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (member_id, booked_for, dependant_id, test_id, appointment_date, appointment_time, where_taken, latitude, longitude, status, lab_id, invoice_no)

        try:
            cursor.execute(sql, data)
            connection.commit()
            return jsonify({"message":"Booking Verified"})
        
        except:
            connection.rollback()
            return jsonify({"message":"Booking Failed"})

class mybooking(Resource):
    def get(self):
        data = request.json
        member_id = data["member_id"]
        connection = pymysql.connect(host='localhost', user='root', password='', database='Medilab')
        sql = "select * from bookings where member_id = %s"
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, member_id)
        if cursor.rowcount == 0:
            return jsonify({"Message": "Booking does not exist"})
        else:
            bookings = cursor.fetchall()
            # date and time was not convertible to json
            # hence we use json.dumps and json.loads
            import json
            # we want to pass our bookings to json.dumps
            ourbookings = json.dumps(bookings, indent=1, sort_keys=True, default=str)
            return json.loads(ourbookings)

class payment(Resource):
    def post(self):
        data = request.json
        invoice_no = data["invoice_no"]
        amount = data["amount"]
        phone = data["phone"]
        mpesa_payment(amount, phone, invoice_no)
        return jsonify({"message":"Payment Successful"})