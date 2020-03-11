# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_data = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Delete existing documents from MongoDB first so we can store freshly scraped data 
    mongo.db.collection.delete_many({})

    # Run Mars scrape function
    mars_scraped_data = scrape_mars.scrape()

    # Insert the Mars scraped data into MongoDB
    mongo.db.collection.insert_one(mars_scraped_data)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
