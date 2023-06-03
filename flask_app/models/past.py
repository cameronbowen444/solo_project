from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, current
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Past: 
    db = "work_tracker"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.pay = data['pay']
        self.address = data['address']
        self.full_name = data['full_name']
        self.phone = data['phone']
        self.email_address = data['email_address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None


    @classmethod 
    def save_past(cls, data):
        query = "INSERT INTO past (name, description, location, start_date, end_date, pay, address, full_name, phone, email_address, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(location)s, %(start_date)s, %(end_date)s, %(pay)s, %(address)s, %(full_name)s, %(phone)s, %(email_address)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_past_job(cls, data):
        query = "SELECT * FROM past WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod 
    def update_past(cls, data):
        query = "UPDATE past SET name=%(name)s, description=%(description)s, location=%(location)s, start_date=%(start_date)s, end_date=%(end_date)s, pay=%(pay)s, full_name=%(full_name)s, phone=%(phone)s, email_address=%(email_address)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def delete_past(cls, data):
        query = "DELETE FROM past WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod 
    def get_past_jobs(cls):
        query = "SELECT * FROM past JOIN users ON past.user_id = users.id;"
        result =  connectToMySQL(cls.db).query_db(query)
        if len(result) == 0:
            return []
        else:
            pasts = []
            for row in result:
                past = cls(row)
                user_info = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }
                author = user.User(user_info)
                past.user_id = author
                pasts.append(past)
            return pasts

    @staticmethod
    def validate_past(past):
        is_valid = True
        if len(past['name']) < 3:
            flash("Job name must be at least 3 characters!", "past")
            is_valid = False
        if len(past['description']) < 3:
            flash("Job description must be at least 3 characters!", "past")
            is_valid = False
        if past['start_date'] == "":
            flash("Start date is required!", "past")
            is_valid = False
        if past['end_date'] == "":
            flash("End date is required!", "past")
            is_valid = False
        if past['pay'] == "":
            flash("Pay is required!", "past")
            is_valid = False
        return is_valid 