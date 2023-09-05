from main import get_travel_time #local import
from personal_info import desktop_path, maps_directions_url #local import

from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

CLIENT_SECRET_FILE = desktop_path + '/client_secret.json' #OAuth 2.0 Client ID json file path
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/'] #authorization scope (full permission to use Gmail account)

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) #create gmail api service instance

travel_time, int_travel_time = get_travel_time()
sleep_time = 60-int_travel_time
FIVE_MINS_IN_SECS = 5*60

def create_raw_string(str):
	if str == "wake up":
		emailMsg = f"Hello,\n\nYou are currently scheduled to start travling at: 6:{sleep_time} AM. Estimated travel time is: {travel_time}. Click this link to open Google Maps directions: {maps_directions_url}\n\nHave a safe trip!" #message body
	elif str == "5 min":
		emailMsg = f"Hello,\n\nThis is your five minute reminder. You are currently scheduled to start travling at: 6:{sleep_time} AM. Estimated travel time is: {travel_time}. Click this link to open Google Maps directions: {maps_directions_url}\n\nHave a safe trip!" #message body
	elif str == "leave":
		emailMsg = f"Hello,\n\nThis is your final reminder. Estimated travel time is: {travel_time}. Click this link to open Google Maps directions: {maps_directions_url}\n\nHave a safe trip!" #message body
	
	mimeMessage = MIMEMultipart() #Initialize MIMEMultipart (Multipurpose Internet Mail Extensions) instance
	mimeMessage['to'] = '...@gmail.com' #set email reciever
	mimeMessage['subject'] = 'Grocery Trip Reminder' #set email subject
	mimeMessage.attach(MIMEText(emailMsg, 'plain')) #add message body to MIME
	raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode() #Gmail api needs raw string

	return raw_string

def send_email(str):
	message = service.users().messages().send(userId='me', body={'raw': create_raw_string(str)}).execute() #me references the authenticated user
	print(message)
	return

if __name__ == "__main__":
	send_email("wake up")
	time.sleep(sleep_time*60-FIVE_MINS_IN_SECS)
	send_email("5 min")
	time.sleep(sleep_time*60)
	send_email("leave")
