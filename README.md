# makeadevlol

Simple Flask app hosted on Pythonanywhere.


1. Loads a .csv file of programming jokes and displays a random one at page refresh.
2. Verifies input mobile phone number and sends SMS jokes via Twilio API using a limited Trial account handling potential errors. Form implements CSRF tokens.
3. Implements an endpoint for use as a Twilio reply webhook that tests for a presence of a particular keyword and replies accordingly.
