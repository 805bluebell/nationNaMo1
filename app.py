from flask import Flask, render_template, request


# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
# from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def login():
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
	"""
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=8080)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	

	return creds
	



"""Send an email message from the user's account.
"""

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	message: Message to be sent.

  Returns:
	Sent Message.
  """
  message = (service.users().messages().send(userId=user_id, body=message)
			   .execute())
  print(f"Message Id: {message['id']}")
  return message
  # try:
  #   message = (service.users().messages().send(userId=user_id, body=message)
  #              .execute())
  #   print(f"Message Id: {message['id']}")
  #   return message
  # except:
  #   print("An error occurred")


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
	sender: Email address of the sender.
	to: Email address of the receiver.
	subject: The subject of the email message.
	message_text: The text of the email message.

  Returns:
	An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  # return message
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw': raw}
  # return {'raw': base64.urlsafe_b64encode(bytes(message.as_string(), 'utf-8'))}
  # return b64_string
  # b64_string = b64_bytes.decode()
  # body = {'raw': message.as_string()}
  # return body


def startSending(creds, to, subject, msg):
	service = build('gmail', 'v1', credentials=creds)
	msg = CreateMessage("me", to, subject, msg)
	SendMessage(service, "me", msg)





app = Flask(__name__)

@app.route('/start')
def hello_world():
	creds = login()
	return render_template('compose.html')

	startSending(creds)
	return 'Hello, World!'

@app.route('/sendform')
def sendfrom():
	return render_template('compose.html')

@app.route('/send')
def sendit():
	to = request.args.get('to')
	subject = request.args.get('subject')
	msg = request.args.get('msg')
	
	creds = login()
	startSending(creds, to, subject, msg)
	return "Success, Email sent :)"

