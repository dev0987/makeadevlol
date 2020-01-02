# makeadevlol

Simple Flask app hosted on Pythonanywhere.


1. Loads a .csv file of programming jokes and displays a random one at page refresh/makeadevlol endpoint. The .csv file was stripped of unicode characters that would require UCS-2 encoding so GSM-7 can be used when sending Twilio SMS messages to conserve space (153 GSM-7 chars vs 63 with UCS-2 for message body excluding Twilio message headers).
2. Verifies input mobile phone number and sends SMS joke msg via Twilio API using a limited Trial account handling potential errors. Form implements CSRF tokens. Keeps a .json log of send messages including ones with errors.
3. Implements an endpoint for use as a Twilio reply webhook that tests for a presence of a particular keyword and replies accordingly.
