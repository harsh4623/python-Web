from flask import Flask, render_template, request
import pandas as pd
from app import app


app = Flask(__name__)

# Load the dataset (Update the path to your CSV file)
data = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Final.csv')

@app.route('/', methods=['GET', 'POST'])
# @app.route('/mobile_review', methods=['GET', 'POST'])
def index():
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

if __name__ == '__main__':
    app.run(debug=True)
