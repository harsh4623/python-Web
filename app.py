from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for, request
# import new_app
from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import os

app = Flask(__name__)

matplotlib.use('Agg')

rel_path = 'data/Final_Final.csv'
rel_path2= 'data/Final_updated_Flipkart.csv'

abs_file_path = os.path.abspath(os.path.join(os.getcwd(), rel_path))
abs_file_path2 = os.path.abspath(os.path.join(os.getcwd(), rel_path2))

# data = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Final.csv')
data=pd.read_csv(abs_file_path)
data1=pd.read_csv(abs_file_path2)

# data1 = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_updated_Flipkart.csv')

# Route for the homepage
@app.route('/')
def homepage():
    return render_template('layout1.html')

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

def display_ranges():
    display=['4.5-5',"5-5.5",'5.5-6',"6-6.5",'6.5-7']

    return display

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

 
# @app.route('/', methods=['GET', 'POST'])
@app.route('/feature_wise_selection', methods=['GET', 'POST'])
# @app.route('/new_index', methods=['GET', 'POST'])
# @app.route('/new_feature_wise_selection', methods=['GET', 'POST'])
def feature_wise_selection():
    if request.method == 'POST':
        mobile_name = request.form['company_name']
        price_range = request.form['price_range']
        camera = request.form['camera']
        display_size = request.form['display']
        rating_range = request.form['rating_range']

        if display_size:

            min_display, max_display = display_size.split('-')

    # Convert min_display and max_display to float values
            min_display = float(min_display)
            max_display = float(max_display)
        else:
            min_display=None
            max_display=None


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
        filtered_data = filter_data(mobile_name, min_price, max_price, camera, display_size, min_rating, max_rating,min_display,max_display)

        return render_template('result.html', data=filtered_data.to_html(classes='table table-striped'))

    sorted_display = sorted(data1['Display inch'].unique())

    return render_template('new.html', company_names=get_unique_companyname_names(), price_ranges=get_price_ranges(),
                           cameras=get_unique_cam(), displays=display_ranges(), rating_ranges=get_rating_ranges())


def filter_data(mobile_name, min_price, max_price, camera, display_size, min_rating, max_rating,min_display,max_display):
    filtered_data = data1.copy()

    if mobile_name:
        filtered_data = filtered_data[filtered_data['Company Name'] == mobile_name]

    if min_price is not None and max_price is not None:
        filtered_data = filtered_data[(filtered_data['Price'].str.replace(',', '').str.replace('₹', '').astype(float) >= min_price) &
                                      (filtered_data['Price'].str.replace(',', '').str.replace('₹', '').astype(float) <= max_price)]

    if camera:
        camera_values = filtered_data['Primary Camera'].str.split('+').str[0].str.strip()
        filtered_data = filtered_data[camera_values.str.contains(camera, case=False)]

    # if display_size:
    #     display_size = float((display_size))
    #     filtered_data = filtered_data[filtered_data['Display inch'] <= display_size]

    if display_size:
        filtered_data = filtered_data[
            (filtered_data['Display inch'] >= min_display) &
            (filtered_data['Display inch'] <= max_display)
        ]

    if min_rating is not None and max_rating is not None:
        filtered_data = filtered_data[(filtered_data['Rating'] >= min_rating) & (filtered_data['Rating'] <= max_rating)]

    return filtered_data


def get_unique_companyname_names():
    # Get unique mobile names from the data
    return data1['Company Name'].unique()

def get_unique_colors():
    # Get unique colors from the data
    return data1['Color'].unique()

def get_unique_price():
    # Get unique prices from the data
    return data1['Price'].unique()

# def get_unique_cam():
#     # Get unique colors from the data

#     return data['Primary Camera'].unique()
def get_unique_cam():
    # Get unique camera values from the data

    # Split the camera values and extract the first part
    camera_values = data1['Primary Camera'].str.split('+').str[0].str.strip()
    
    return camera_values.unique()


def get_unique_disp():
    # Get unique colors from the data
    return data1['Display inch'].unique()

@app.route('/compare_two_mobile', methods=['GET', 'POST'])
def compare_two_mobile():
    if request.method == 'POST':
        mobile1 = request.form.get('mobile1')
        mobile2 = request.form.get('mobile2')

        if mobile1 and mobile2:
            # Filter the dataset for the selected mobiles
            mobile1_data = data[data['Mobile Name'] == mobile1]
            mobile2_data = data[data['Mobile Name'] == mobile2]

            # Create a DataFrame for the differences
            diff_data = pd.concat([mobile1_data, mobile2_data]).drop_duplicates(keep=False)

            # Select specific columns for display
            columns_to_display = ['Mobile Name', 'Price', 'In The Box', 'Color', 'Display Size', 'Operating System', 'Rating', 'REVIEW BODY', 'DL Sentiment Pred', 'ML Sentiment Pred']

            # Modify the 'Images' column to include image links
            # diff_data['Images'] = diff_data['Images'].apply(lambda x: f'<a href="{x}" target="_blank">View Image</a>')

            diff_data_dict_list = diff_data[columns_to_display].to_dict(orient='records')
            # sorted_mobile_names = sorted(data['Mobile Name'].unique())

            return render_template('result2.html', diff_data_dict_list=diff_data_dict_list, mobile1=mobile1, mobile2=mobile2)

    return render_template('index2.html', mobile_names=get_unique_mobile_names())

def get_unique_mobile_names():
    # Get unique mobile names from the data
    return sorted(data['Mobile Name'].unique())

@app.route('/mobile_review', methods=['GET', 'POST'])
def mobile_review():
    mobile_features = None

    if request.method == 'POST':
        mobile_name = request.form.get('mobile_name')

        if mobile_name:
            mobile_data = data[data['Mobile Name'] == mobile_name]

            if not mobile_data.empty:
                # Select specific columns for display
                columns_to_display = ['Mobile Name', 'Model Number','Price','Internal Storage','RAM','In The Box', 'Color', 'Display Size', 'Operating System','Primary Camera','Battery Capacity','Star Wise Rating','Total_Ratings','Total_Reviews','REVIEW BODY', 'Rating', 'REVIEW BODY', 'DL Sentiment Pred', 'ML Sentiment Pred']

                # Modify the 'Images' column to include image links
                # mobile_data['Images'] = mobile_data['Images'].apply(lambda x: f'<a href="{x}" target="_blank">View Image</a>')

                mobile_features = mobile_data[columns_to_display].to_dict(orient='records')

    # Get unique mobile names from the data and sort them
    sorted_mobile_names = sorted(data['Mobile Name'].unique())

    return render_template('index.html', sorted_mobile_names=sorted_mobile_names, mobile_features=mobile_features)

@app.route('/chart')
def chart():
    chart_base64 =ratings_chart()
    chart_base64_1=prices_chart()
    chart_base64_2=battery_chart()
    chart_base64_3=sentiment_chart()
    return render_template('ana.html',chart_base64=chart_base64,chart_base64_1=chart_base64_1,chart_base64_2=chart_base64_2,chart_base64_3=chart_base64_3)

@app.route('/ratings_chart')
def ratings_chart():
    # Calculate the average rating for each company
    average_ratings = data.groupby('Company Name')['Rating'].mean().sort_values(ascending=False)

    # Set up the figure and axis for the bar plot
    plt.figure(figsize=(10, 6))
    ax = average_ratings.plot(kind='bar', color='skyblue')

    # Customize the plot
    plt.title('Average Rating by Company')
    plt.xlabel('Company Name')
    plt.ylabel('Average Rating')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=90)

    # Save the plot to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format="png")
    chart_buffer.seek(0)

    # Encode the plot as base64
    chart_base64 = base64.b64encode(chart_buffer.read()).decode("utf-8")

    return f"<img src='data:image/png;base64,{chart_base64}'/>"

@app.route('/prices_chart')
def prices_chart():
    if data['Price'].dtype == 'float64':
        # If the symbol is already removed, check if the column is numeric
        if data['Price'].dtype != 'float64':
            data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
    else:
        # Remove any non-numeric characters and convert the 'Price' column to numeric
        data['Price'] = data['Price'].str.replace('₹', '').str.replace(',', '')
        data['Price'] = pd.to_numeric(data['Price'], errors='coerce')


    
    # Remove any non-numeric characters and convert the 'Price' column to numeric
    # data['Price'] = data['Price'].str.replace('₹', '').str.replace(',', '')
    # data['Price'] = pd.to_numeric(data['Price'], errors='coerce')

    # Calculate the average price for each company
    average_prices = data.groupby('Company Name')['Price'].mean().sort_values(ascending=False)

    # Set up the figure and axis for the bar plot
    plt.figure(figsize=(10, 6))
    ax = average_prices.plot(kind='bar', color='skyblue')

    # Customize the plot
    plt.title('Average Prices by Company')
    plt.xlabel('Company Name')
    plt.ylabel('Average Price')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=90)

    # Save the plot to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format="png")
    chart_buffer.seek(0)

    # Encode the plot as base64
    chart_base64 = base64.b64encode(chart_buffer.read()).decode("utf-8")

    return f"<img src='data:image/png;base64,{chart_base64}'/>"

@app.route('/battery_chart')
def battery_chart():
    # Remove any non-numeric characters and convert the 'Battery Capacity' column to numeric
    data['Battery Capacity'] = data['Battery Capacity'].str.replace('[^\d.]', '', regex=True)
    data['Battery Capacity'] = pd.to_numeric(data['Battery Capacity'], errors='coerce')

    # Calculate the average 'Battery Capacity' for each company
    average_battery_capacity = data.groupby('Company Name')['Battery Capacity'].mean().sort_values(ascending=False)

    # Set up the figure and axis for the bar plot
    plt.figure(figsize=(12, 6))
    average_battery_capacity.plot(kind='bar', color='skyblue')
    plt.xlabel('Company Name')
    plt.ylabel('Average Battery Capacity (mAh)')
    plt.title('Average Battery Capacity by Company')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format="png")
    chart_buffer.seek(0)

    # Encode the plot as base64
    chart_base64 = base64.b64encode(chart_buffer.read()).decode("utf-8")

    return f"<img src='data:image/png;base64,{chart_base64}'/>"

@app.route('/sentiment_chart')
def sentiment_chart():
    # Preprocess the 'DL Sentiment Pred' column to ensure it contains the sentiment categories
    data['DL Sentiment Pred'] = data['DL Sentiment Pred'].str.lower()

    # Group the data by 'Company Name' and count the occurrences of each sentiment category
    sentiment_counts = data.groupby(['Company Name', 'DL Sentiment Pred']).size().unstack(fill_value=0)

    # Create a stacked bar graph
    ax = sentiment_counts.plot(kind='bar', stacked=True, colormap='coolwarm', figsize=(12, 6))
    plt.xlabel('Company Name')
    plt.ylabel('Sentiment Count')
    plt.title('Sentiment Distribution by Company')
    plt.xticks(rotation=90)
    plt.legend(title='Sentiment')

    # Save the plot to a BytesIO object
    chart_buffer = BytesIO()
    plt.savefig(chart_buffer, format="png")
    chart_buffer.seek(0)

    # Encode the plot as base64
    chart_base64 = base64.b64encode(chart_buffer.read()).decode("utf-8")

    return f"<img src='data:image/png;base64,{chart_base64}'/>"

if __name__ == '__main__':
    app.run(debug=True)
