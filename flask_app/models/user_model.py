from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data=['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes_schema').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if results:
            return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if results:
            return cls(results[0])

    @staticmethod
    def validate_register(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!", "register")
            is_valid=False
        elif User.get_by_email(data):
            flash("email already taken.", "register")
            is_valid=False
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid= False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid= False
        if len(data['password']) < 8:
            flash("password must be at least 8 characters", "register")
            is_valid= False
        elif data['password'] != data['confirm']:
            flash("Password dont match", "register")
            is_valid=False
        return is_valid
