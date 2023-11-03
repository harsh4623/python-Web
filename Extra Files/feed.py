from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuration for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Change to your email provider's SMTP port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'harshpatel46399@gmail.com'
app.config['MAIL_PASSWORD'] = 'harshp463@'
# app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input
        email = request.form['email']
        feedback = request.form['feedback']

        # Send email
        msg = Message('Feedback for Your Website', sender='your_email@example.com', recipients=[email])
        msg.body = feedback
        mail.send(msg)

        return "Feedback sent! Thank you."

    return render_template('feed.html')

if __name__ == '__main__':
    app.run(debug=True)
