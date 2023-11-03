
from flask import Flask, render_template, request
import pandas as pd
from app import app
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
# from app import app as app_parent



app = Flask(__name__)
# app.register_blueprint(app_parent)
# Load the data from data.csv
data = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Flipkart_Update.csv')

def get_price_ranges():
    # Determine price ranges based on your data
    # You can customize this based on your data
    price_ranges = [
        "0-10,000",
        "10,000-20,000",
        "20,000-30,000",
        "30,000-40,000",
        "40,000-50,000",
        "50,000-60,000",
        "60,000-70,000",
        "70,000-80,000",
        "80,000-90,000",
        "90,000-1,00,000",
        "1,00,000-1,20,000",
        "1,20,000-1,30,000",
        "1,30,000-1,50,000",
        "1,50,000-2,00,000",
    ]
    return price_ranges

def get_rating_ranges():
    # Determine rating ranges based on your data
    # Customize this based on your data
    rating_ranges = [
        "1-2",
        "2-3",
        "3-4",
        "4-5",
    ]
    return rating_ranges

 
@app.route('/', methods=['GET', 'POST'])
# @app.route('/feature_wise_selection', methods=['GET', 'POST'])
# @app.route('/new_index', methods=['GET', 'POST'])
# @app.route('/new_feature_wise_selection', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mobile_name = request.form['company_name']
        price_range = request.form['price_range']
        camera = request.form['camera']
        display_size = request.form['display']
        rating_range = request.form['rating_range']

        # Determine the price range limits
        if price_range:
            price_range_parts = price_range.split('-')
            min_price = float(price_range_parts[0].replace(',', '').replace('₹', '').strip())
            max_price = float(price_range_parts[1].replace(',', '').replace('₹', '').strip())

        if rating_range:
            rating_range_parts = rating_range.split('-')
            min_rating = float(rating_range_parts[0])
            max_rating = float(rating_range_parts[1])

        # Filter the data based on user input
        filtered_data = filter_data(mobile_name, min_price, max_price, camera, display_size, min_rating, max_rating)

        return render_template('result.html', data=filtered_data.to_html(classes='table table-striped'))

    sorted_display = sorted(data['Display inch'].unique())

    return render_template('new.html', company_names=get_unique_companyname_names(), price_ranges=get_price_ranges(),
                           cameras=get_unique_cam(), displays=sorted_display, rating_ranges=get_rating_ranges())


def filter_data(mobile_name, min_price, max_price, camera, display_size, min_rating, max_rating):
    filtered_data = data.copy()

    if mobile_name:
        filtered_data = filtered_data[filtered_data['Company Name'] == mobile_name]

    if min_price is not None and max_price is not None:
        filtered_data = filtered_data[(filtered_data['Price'].str.replace(',', '').str.replace('₹', '').astype(float) >= min_price) &
                                      (filtered_data['Price'].str.replace(',', '').str.replace('₹', '').astype(float) <= max_price)]

    if camera:
        camera_values = filtered_data['Primary Camera'].str.split('+').str[0].str.strip()
        filtered_data = filtered_data[camera_values.str.contains(camera, case=False)]

    if display_size:
        display_size = float((display_size))
        filtered_data = filtered_data[filtered_data['Display inch'] <= display_size]

    if min_rating is not None and max_rating is not None:
        filtered_data = filtered_data[(filtered_data['Rating'] >= min_rating) & (filtered_data['Rating'] <= max_rating)]

    return filtered_data


def get_unique_companyname_names():
    # Get unique mobile names from the data
    return data['Company Name'].unique()

def get_unique_colors():
    # Get unique colors from the data
    return data['Color'].unique()

def get_unique_price():
    # Get unique prices from the data
    return data['Price'].unique()

# def get_unique_cam():
#     # Get unique colors from the data

#     return data['Primary Camera'].unique()
def get_unique_cam():
    # Get unique camera values from the data

    # Split the camera values and extract the first part
    camera_values = data['Primary Camera'].str.split('+').str[0].str.strip()
    
    return camera_values.unique()


def get_unique_disp():
    # Get unique colors from the data
    return data['Display inch'].unique()

if __name__ == '__main__':
    app.run(debug=True)
