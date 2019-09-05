from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scraping():
    mars_info = mongo.db.mars_info

    #scrape_news()
    #scrape_image()
    #scrape_tweets()
    #scrape_facts()
    #scrape_hemispheres()

    news = scrape_mars.scrape_news()
    image = scrape_mars.scrape_image()
    tweets = scrape_mars.scrape_tweets()
    facts = scrape_mars.scrape_facts()
    hemispheres = scrape_mars.scrape_hemispheres()
    update_data ={'news':news,'image':image,'tweets':tweets,'facts':facts,'hemispheres':hemispheres}

    # listings.update({}, listings_data, upsert=True)
    mars_info.update({}, update_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
