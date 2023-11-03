# import pandas as pd
# import spacy
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# from flask import Flask, render_template, request

# # Load the CSV file
# df = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Final.csv')  # Update with the path to your CSV file

# # Load spaCy's English tokenizer
# nlp = spacy.load('en_core_web_sm')

# # Initialize VADER sentiment analyzer
# analyzer = SentimentIntensityAnalyzer()

# # Initialize Flask app
# app = Flask(__name__)

# # Create a new column for sentiment
# df['Sentiment'] = ""

# # Analyze sentiment and collect words
# for index, row in df.iterrows():
#     review = row['REVIEW BODY']
#     if isinstance(review, str):
#         analysis = analyzer.polarity_scores(review)
#         sentiment = 'positive' if analysis['compound'] >= 0.05 else 'negative' if analysis['compound'] <= -0.05 else 'neutral'
#         df.at[index, 'Sentiment'] = sentiment

# # Calculate sentiment percentages
# sentiment_counts = df['Sentiment'].value_counts()
# total_reviews = len(df)
# sentiment_percentages = {
#     'positive': sentiment_counts.get('positive', 0) / total_reviews * 100,
#     'negative': sentiment_counts.get('negative', 0) / total_reviews * 100,
#     'neutral': sentiment_counts.get('neutral', 0) / total_reviews * 100,
# }

# # Function to generate the word clouds
# def generate_word_cloud(sentiment, words):
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
#     wordcloud.to_file(f'/Users/harshpatel/Desktop/Final_Project/website/static/{sentiment}_wordcloud.png')

# # Generate word clouds for positive and negative sentiments
# generate_word_cloud('positive', df[df['Sentiment'] == 'positive']['REVIEW BODY'])
# generate_word_cloud('negative', df[df['Sentiment'] == 'negative']['REVIEW BODY'])

# # Function to generate the sentiment pie chart
# def generate_sentiment_pie_chart(sentiment_percentages):
#     labels = list(sentiment_percentages.keys())
#     sizes = list(sentiment_percentages.values())
#     colors = ['gold', 'lightcoral', 'lightskyblue']
#     explode = (0.1, 0, 0)

#     plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
#     plt.axis('equal')
#     plt.savefig('/Users/harshpatel/Desktop/Final_Project/website/static/sentiment_pie_chart.png', bbox_inches='tight')
#     plt.close()

# generate_sentiment_pie_chart(sentiment_percentages)

# # Route to the home page
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         user_review = request.form['review_text']
#         if user_review:
#             analysis = analyzer.polarity_scores(user_review)
#             sentiment = 'positive' if analysis['compound'] >= 0.05 else 'negative' if analysis['compound'] <= -0.05 else 'neutral'
#             return render_template('wr.html', review=user_review, sentiment=sentiment, sentiment_percentages=sentiment_percentages)
#     return render_template('word.html')

# if __name__ == '__main__':
#     app.run(debug=True)


import pandas as pd
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from flask import Flask, render_template, request

# Load the CSV file
df = pd.read_csv('/Users/harshpatel/Desktop/Final_Project/website/data/Final_Final.csv')  # Update with the path to your CSV file

# Load spaCy's English tokenizer
nlp = spacy.load('en_core_web_sm')

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize Flask app
app = Flask(__name__)

# Create a new column for sentiment
df['Sentiment'] = ""

# Calculate sentiment percentages
def calculate_sentiment_percentages(df):
    sentiment_counts = df['Sentiment'].value_counts()
    total_reviews = len(df)
    return {
        'positive': sentiment_counts.get('positive', 0) / total_reviews * 100,
        'negative': sentiment_counts.get('negative', 0) / total_reviews * 100,
        'neutral': sentiment_counts.get('neutral', 0) / total_reviews * 100,
    }

# Function to generate the word clouds
def generate_word_cloud(sentiment, text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    wordcloud.to_file(f'/Users/harshpatel/Desktop/Final_Project/website/static/{sentiment}_wordcloud.png')

# Function to generate the sentiment pie chart
def generate_sentiment_pie_chart(sentiment_percentages):
    labels = list(sentiment_percentages.keys())
    sizes = list(sentiment_percentages.values())
    colors = ['gold', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('/Users/harshpatel/Desktop/Final_Project/website/static/sentiment_pie_chart.png', bbox_inches='tight')
    plt.close()

# Route to the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_review = request.form['review_text']
        if user_review:
            analysis = analyzer.polarity_scores(user_review)
            sentiment = 'positive' if analysis['compound'] >= 0.05 else 'negative' if analysis['compound'] <= -0.05 else 'neutral'
            return render_template('wr.html', review=user_review, sentiment=sentiment, sentiment_percentages={}, user_input=True)
    return render_template('word.html')

# Route to display sentiment analysis, word clouds, and pie chart
@app.route('/analyze', methods=['POST'])
def analyze():
    user_review = request.form['user_input']
    analysis = analyzer.polarity_scores(user_review)
    sentiment = 'positive' if analysis['compound'] >= 0.05 else 'negative' if analysis['compound'] <= -0.05 else 'neutral'
    
    # Clear the existing 'Sentiment' column
    df['Sentiment'] = ""
    
    # Update the 'Sentiment' column for the user's input
    df.loc[df['REVIEW BODY'] == user_review, 'Sentiment'] = sentiment

    # Calculate sentiment percentages based on the user's input
    sentiment_percentages = calculate_sentiment_percentages(df)

    # Generate word clouds for positive and negative sentiments based on the user's input
    positive_reviews = ' '.join(df[df['Sentiment'] == 'positive']['REVIEW BODY'])
    negative_reviews = ' '.join(df[df['Sentiment'] == 'negative']['REVIEW BODY'])
    generate_word_cloud('positive', positive_reviews)
    generate_word_cloud('negative', negative_reviews)

    # Generate the sentiment pie chart
    generate_sentiment_pie_chart(sentiment_percentages)

    return render_template('wr.html', review=user_review, sentiment=sentiment, sentiment_percentages=sentiment_percentages, user_input=False)

if __name__ == '__main__':
    app.run(debug=True)
