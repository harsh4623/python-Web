from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

matplotlib.use('Agg')

# Load your dataset
data = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Final.csv')  # Replace 'your_data.csv' with your actual file path

@app.route('/')
def index():
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
    # Remove any non-numeric characters and convert the 'Price' column to numeric
    data['Price'] = data['Price'].str.replace('₹', '').str.replace(',', '')
    data['Price'] = pd.to_numeric(data['Price'], errors='coerce')

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