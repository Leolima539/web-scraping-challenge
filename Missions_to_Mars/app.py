from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template for initial scraping
@app.route("/")
def home():

    mars_data = mongo.db.collection.find()
    return render_template("index.html", data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update({},mars_info, upsert = True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)