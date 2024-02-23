# HouseHUNTER
Python code - utilising SendGrid API to email you for faster property notification than via RightMoves email notifications

This Python Flask application monitors Rightmove for new property listings and sends email notifications using SendGrid when new listings are detected. It's designed to run locally and check for new listings upon accessing the root URL of the Flask server.

Features
Fetches current property listings from Rightmove.
Compares the listing count to detect new listings.
Sends an email notification via SendGrid when new listings are found.
Requirements
Python 3.x
Flask
Requests
BeautifulSoup4
SendGrid Python Library
Setup Instructions
1. Clone the Repository
Clone the project repository to your local machine.

bash
Copy code
git clone <repository-url>
cd <repository-directory>
2. Install Dependencies
Ensure you have Python installed, then install the required Python packages:

bash
Copy code
pip install Flask requests beautifulsoup4 sendgrid
3. SendGrid Setup
To use SendGrid for sending emails, follow these steps:

a. Create a SendGrid Account
If you don't already have a SendGrid account, sign up at SendGrid's website.

b. Verify Your Email Address
Verify your email address with SendGrid to ensure you can send emails from it.

c. Create a SendGrid API Key
Log in to your SendGrid dashboard.
Navigate to Settings > API Keys.
Click on Create API Key.
Give your API key a name, assign full access or restricted access with email sending capabilities, and then click Create & View.
Copy your API key to a secure place.
d. Set the SendGrid API Key in Your Environment
To avoid hardcoding your API key in your application, set it as an environment variable:

bash
Copy code
echo "export SENDGRID_API_KEY='YOUR_SENDGRID_API_KEY'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
source ./sendgrid.env
Replace YOUR_SENDGRID_API_KEY with the actual API key you obtained from SendGrid.

Important: Adding sendgrid.env to .gitignore prevents your API key from being tracked in version control.

4. Running the Application
With all setup complete, you can start the Flask application:

bash
Copy code
python app.py
5. Accessing the Application
Open a web browser and navigate to http://localhost:8080/. The Flask application will fetch the current listings from Rightmove, compare them to the previous check, and send an email notification if new listings are detected.

Additional Information
The application uses the SENDGRID_API_KEY environment variable for authentication with the SendGrid API.
Modify the from_email and to_emails parameters in the send_email function to match your verified sender and recipient email addresses.
