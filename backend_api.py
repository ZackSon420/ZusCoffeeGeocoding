from flask import Flask, jsonify
from flask_cors import CORS 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load outlet data from CSV
outlets_data = pd.read_csv('Zus_coffee_scrape_cleaned.csv')

@app.route('/api/outlets')
def get_outlets():
    return jsonify(outlets_data.to_dict(orient='records'))

@app.route('/api/outlets/<outlet_id>')
def get_outlet(outlet_id):
    outlet = outlets_data.loc[outlets_data['Index'] == int(outlet_id)]
    if outlet.empty:
        return jsonify({'error': 'Outlet not found'}), 404
    return jsonify(outlet.to_dict(orient='records'))

def calculate_catchment_area(outlet_lat, outlet_lon):
    outlet_point = Point(outlet_lon, outlet_lat)
    catchment_polygon = outlet_point.buffer(0.045)  # Set to 5km catchment radius
    return catchment_polygon

if __name__ == '__main__':
    app.run(debug=True)
