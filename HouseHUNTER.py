from flask import Flask
import os
import requests
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Initialise the Flask application
app = Flask(__name__)

# URL for fetching property listings data from Rightmove - generic London property search change to required area
url = "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E87490&insId=1&radius=3.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="

# Retrieve the SendGrid API Key from environment variables
sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
# Variable to store the count of listings from the last check
previous_count = 0

def send_email(from_email, to_email, subject, body):
    """Send an email using the SendGrid API."""
    print("Preparing to send email...")
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email successfully sent from {from_email} to {to_email}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def fetch_data(url):
    """Fetch data from the specified URL using the requests library."""
    print("Fetching data from URL...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Data successfully fetched.")
            return response
        else:
            print(f"Error occurred while fetching data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while fetching data: {e}")
    return None

def check_new_listings():
    """Check for new property listings and send an email if there are new listings."""
    global previous_count
    print("Checking for new listings...")
    response = fetch_data(url)
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract the number of listings from the page content
        result_count_span = soup.select_one('.searchHeader-resultCount')
        if result_count_span:
            count = int(result_count_span.text.replace(',', ''))  # Remove commas for conversion to int
            print(f"Current listing count: {count}")
            if count != previous_count:
                print("Change in listing count detected, sending email...")
                send_email("ben.allott@gmail.com", "ben.allott@gmail.com", "Property Listings Update", f"The number of listings has changed. There are now {count} listings available. Check it out here: " + url)
                previous_count = count
            else:
                print("No change in the no. of listenings.")
        else:
            print("Failed to find the listing count on the page.")
    else:
        print("Failed to fetch/parse listing data.")

@app.route("/")
def index():
    """Define the root URL route for the Flask application."""
    check_new_listings()
    return "Checking for new listings. Please check the console for more details."

if __name__ == "__main__":
    # Specify the port to run the Flask app
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)  # Run the Flask app with debug mode enabled
