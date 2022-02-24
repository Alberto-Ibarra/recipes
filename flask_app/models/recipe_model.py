from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from .user_model import User


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.instruction = data['instruction']
        self.description = data['description']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for row in results:
            print("*************************")
            print(row)
            recipe = cls(row)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        print(results)
        if results:
            return cls(results[0])

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id= users.id WHERE recipes.id = %(id)s;"

        results = connectToMySQL('recipes_schema').query_db(query, data)
        recipe = cls(results[0])
        print(results)
        data = {
            **results[0],
            'id': results[0]['users.id'],
            'created_at': results[0]['users.created_at']
        }
        recipe.user = User(data)
        return recipe

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes ( name, under30, instruction, description, created_at, user_id ) VALUES ( %(name)s, %(under30)s, %(instruction)s, %(description)s, %(created_at)s, %(user_id)s);"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name =%(name)s, instruction = %(instruction)s, description = %(description)s WHERE id = %(id)s;"

        return connectToMySQL('recipes_schema').query_db( query,data )


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("name must be at least 3 characters!")
            is_valid = False
        if len(recipe['instruction']) < 3:
            flash("instructions must be at least 3 characters!")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("description must be at least 3 characters!")
            is_valid = False
        return is_valid