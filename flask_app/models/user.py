from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import current, past
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    db = "work_tracker"
    def __init__(self, data): 
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.current = []
        self.past = []


    @classmethod 
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod 
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])


    # @classmethod 
    # def get_current_jobs(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN current ON current.user_id = users.id WHERE users.id = %(id)s;"
    #     result =  connectToMySQL(cls.db).query_db(query, data)
    #     user = cls(result[0])
    #     for row in result:
    #         current_data = {
    #             "id": row['current.id'],
    #             "name": row['name'],
    #             "description": row['description'],
    #             "location": row['location'],
    #             "start_date": row['start_date'],
    #             "end_date": row['end_date'],
    #             "pay": row['pay'],
    #             "address": row['address'],
    #             "full_name": row['full_name'],
    #             "phone": row['phone'],
    #             "email_address": row['email_address'],
    #             "created_at": row['current.created_at'],
    #             "updated_at": row['current.updated_at']
    #         }
    #         user.current.append(current.Current(current_data))
    #     return user


    # @classmethod 
    # def get_past_jobs(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN past ON past.user_id = users.id WHERE users.id = %(id)s;"
    #     result =  connectToMySQL(cls.db).query_db(query, data)
    #     user = cls(result[0])
    #     for row in result:
    #         past_data = {
    #             "id": row['past.id'],
    #             "name": row['name'],
    #             "description": row['description'],
    #             "location": row['location'],
    #             "start_date": row['start_date'],
    #             "end_date": row['end_date'],
    #             "pay": row['pay'],
    #             "address": row['address'],
    #             "full_name": row['full_name'],
    #             "phone": row['phone'],
    #             "email_address": row['email_address'],
    #             "created_at": row['past.created_at'],
    #             "updated_at": row['past.updated_at']
    #         }
    #         user.past.append(past.Past(past_data))
    #     return user


    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters!", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("First name must be at least 3 characters!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!", "register")
            is_valid = False
        if user['confirm'] != user['password']:
            flash("Passwords don't match!", "register")
            is_valid = False
        return is_valid
