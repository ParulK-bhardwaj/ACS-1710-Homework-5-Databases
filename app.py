from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/plantsDatabase"
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def plants_list():
    """Display the plants list page."""

    # TODO: Replace the following line with a database call to retrieve *all*
    # plants from the Mongo database's `plants` collection.
    plants_data = mongo.db.plants.find()

    context = {
        'plants': plants_data,
    }
    return render_template('plants_list.html', **context)

@app.route('/about')
def about():
    """Display the about page."""
    return render_template('about.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Display the plant creation page & process data from the creation form."""
    if request.method == 'POST':
        # TODO: Get the new plant's name, variety, photo, & date planted, and 
        # store them in the object below.
        name = request.form['plant_name']
        variety = request.form['variety']
        photo = request.form['photo']
        date_planted = request.form['date_planted']
        new_plant = {
            'name': name,
            'variety': variety,
            'photo': photo,
            'date_planted': date_planted
        }
        # TODO: Make an `insert_one` database call to insert the object into the
        # database's `plants` collection, and get its inserted id. Pass the 
        # inserted id into the redirect call below.
        new_plant_id = mongo.db.plants.insert_one(new_plant).inserted_id
        return redirect(url_for('detail', plant_id=new_plant_id))

    else:
        return render_template('create.html')

@app.route('/plant/<plant_id>')
def detail(plant_id):
    """Display the plant detail page & process data from the harvest form."""

    # TODO: Replace the following line with a database call to retrieve *one*
    # plant from the database, whose id matches the id passed in via the URL.
    plant_to_show = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    # plant_to_show = mongo.db.plants.find_one(plantID=plant_id)

    # TODO: Use the `find` database operation to find all harvests for the
    # plant's id.
    # HINT: This query should be on the `harvests` collection, not the `plants`
    # collection.
    harvests = mongo.db.harvests.find()

    context = {
        'plant' : plant_to_show,
        'harvests': harvests,
    }
    return render_template('detail.html', **context)

@app.route('/harvest/<plant_id>', methods=['POST'])
def harvest(plant_id):
    """
    Accepts a POST request with data for 1 harvest and inserts into database.
    """

    # TODO: Create a new harvest object by passing in the form data from the
    # detail page form.
    quantity = request.form['harvested_amount']
    date = request.form['date_planted']
    new_harvest = {
        'quantity': quantity, # e.g. '3 tomatoes'
        'date': date,
        'plant_id': plant_id
    }

    # TODO: Make an `insert_one` database call to insert the object into the 
    # `harvests` collection of the database.
    mongo.db.harvests.insert_one(new_harvest)
    # return redirect(url_for('detail', plant_id=new_harvest['_id']))
    return redirect(url_for('detail', plant_id=plant_id))

@app.route('/edit/<plant_id>', methods=['GET', 'POST'])
def edit(plant_id):
    """Shows the edit page and accepts a POST request with edited data."""
    if request.method == 'POST':
        # TODO: Make an `update_one` database call to update the plant with the
        # given id. Make sure to put the updated fields in the `$set` object.
        name = request.form['plant_name']
        variety = request.form['variety']
        photo = request.form['photo']
        date_planted = request.form['date_planted']
        edit_plant = {
            'name': name,
            'variety': variety,
            'photo': photo,
            'date_planted': date_planted,
        }

        searchParam = {'_id': ObjectId(plant_id)}
        changeParam = {'$set' : edit_plant}
        edit_plant = mongo.db.plants.update_one(searchParam, changeParam)
        return redirect(url_for('detail', plant_id=plant_id))
    else:
        plant_to_show = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})

        context = {
            'plant': plant_to_show
        }

        return render_template('edit.html', **context)

@app.route('/delete/<plant_id>', methods=['POST'])
def delete(plant_id):

        searchParam = {'_id': ObjectId(plant_id)}
        mongo.db.plants.delete_one(searchParam)
        mongo.db.harvests.delete_many({"plant_id": plant_id})
        return redirect(url_for('plants_list'))     

if __name__ == '__main__':
    app.run(debug=True)