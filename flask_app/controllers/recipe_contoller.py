from flask import render_template, redirect,request,session
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User


# retreive
@app.route('/all_recipes')
def all_recipes():
    recipes = Recipe.get_all()
    return render_template('/dashboard.html', recipes=recipes)

@app.route('/show/<int:id>/recipe')
def show_recipe(id):
    data = {
        "id": id
    }
    data2 ={
        'id': session['user_id']
    }
    return render_template('show.html', recipe=Recipe.get_one_with_user(data), user=User.get_by_id(data2))

# create
@app.route('/new/recipe')
def new_recipe():
    return render_template('new_recipe.html')

@app.route('/create/recipe', methods=['post'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "under30": request.form["under30"],
        "instruction": request.form["instruction"],
        "description": request.form["description"],
        "created_at": request.form["created_at"],
        "user_id": session["user_id"]
        }
    print(data)
    Recipe.save(data)
    return redirect('/dashboard')

# delete
@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

# update
@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    data ={
        "id":id
    }
    return render_template("edit.html",recipe=Recipe.get_one(data))

@app.route('/recipe/<int:id>/update', methods=['post'])
def recipe_update(id):
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/{id}/edit')
    data = {
        **request.form,
        "id":id
    }
    Recipe.update(data)
    return redirect('/dashboard')