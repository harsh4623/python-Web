from flask import Flask, render_template, request
import pandas as pd
from app import app


app = Flask(__name__)

# Load the dataset
data = pd.read_csv('/Users/harshpatel/Desktop/Website/test/data/Final_Final.csv')

# @app.route('/compare_two_mobile', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
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
            diff_data['Images'] = diff_data['Images'].apply(lambda x: f'<a href="{x}" target="_blank">View Image</a>')

            diff_data_dict_list = diff_data[columns_to_display].to_dict(orient='records')
            # sorted_mobile_names = sorted(data['Mobile Name'].unique())

            return render_template('result2.html', diff_data_dict_list=diff_data_dict_list, mobile1=mobile1, mobile2=mobile2)

    return render_template('index2.html', mobile_names=get_unique_mobile_names())

def get_unique_mobile_names():
    # Get unique mobile names from the data
    return sorted(data['Mobile Name'].unique())
if __name__ == '__main__':
    app.run(debug=True)
