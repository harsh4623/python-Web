from flask import Flask, render_template, request
import pandas as pd
from app import app
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configure Matplotlib to use the Agg backend
matplotlib.use('Agg')

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Flipkart_Update.csv')

# Extract the Mobile Name and Star Wise Rating columns
mobile_names = df['Mobile Name']
star_wise_ratings = df['Star Wise Rating']

# Function to create a chart for a given mobile name
def create_chart(mobile_name):
    selected_mobile = df[df['Mobile Name'] == mobile_name]
    if not selected_mobile.empty:
        star_wise_rating_str = selected_mobile.iloc[0]['Star Wise Rating']
        
        # Remove commas from the string and convert it to a list of integers
        star_wise_ratings = [int(rating.replace(',', '')) for rating in eval(star_wise_rating_str)]

        # Corresponding star labels
        star_labels = [ '5 Stars','4 Stars','3 Stars','2 Stars','1 Stars']

        # Create a bar chart
        plt.figure(figsize=(8, 6))
        plt.bar(star_labels, star_wise_ratings, color='skyblue')
        plt.xlabel('Star Rating')
        plt.ylabel('Count')
        plt.title(f'Star-wise Rating Count for {mobile_name}')
        
        # Save the chart to a BytesIO object
        chart_buffer = BytesIO()
        plt.savefig(chart_buffer, format="png")
        chart_buffer.seek(0)
        
        # Encode the chart as base64
        chart_base64 = base64.b64encode(chart_buffer.read()).decode("utf-8")
        
        return f"<img src='data:image/png;base64,{chart_base64}'/>"
    else:
        return None

# @app.route('/chart', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    chart_base64 = None

    if request.method == 'POST':
        mobile_name = request.form.get('mobile_name')

        if mobile_name:
            chart_base64 = create_chart(mobile_name)

    sorted_mobile_names = sorted(df['Mobile Name'].unique())

    return render_template('chart.html', chart_base64=chart_base64, sorted_mobile_names=sorted_mobile_names)

if __name__ == '__main__':
    app.run(debug=True)



