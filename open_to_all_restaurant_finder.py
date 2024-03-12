from flask import Flask, render_template, request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

app = Flask(__name__)

API_KEY = "cEVxdVw6j15Ajur4bG2oqemztWqwAYQcrVY9Y3ppck_RYlW89rxExLXAkct-IVJnxJ3WEz-2aeNdnNN6sH2aDam69YM3BoDsXGY7B0HEQiCGBcfwfAi4Lk47TU3mZXYx"

def miles_to_meters(miles):
    # 1 mile is approximately equal to 1609.34 meters
    return int(float(miles) * 1609.34)

def get_restaurants(location, radius=None, open_now=False):
    url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=20&" + urlencode({"term": "restaurants", "location": location})
    if radius:
        radius_meters = miles_to_meters(radius)
        url += f"&radius={radius_meters}"
    if open_now:
        url += "&open_now=true"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    req = Request(url, headers=headers)
    with urlopen(req) as response:
        data = json.loads(response.read())
    return data["businesses"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurants', methods=['POST'])
def restaurants():
    location = request.form['location']
    radius = request.form.get('radius')
    open_to_all = 'open_to_all' in request.form
    restaurants = get_restaurants(location, radius, open_to_all)
    return render_template('restaurants.html', restaurants=restaurants)

if __name__ == '__main__':
    app.run(debug=True)