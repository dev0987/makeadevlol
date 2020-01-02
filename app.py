from flask import Flask, session, redirect, url_for, render_template, request
from config import Config
from forms import PhoneForm
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from twilio.base.exceptions import TwilioRestException
import pandas
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

dir_path = os.path.dirname(os.path.realpath(__file__))

jokes = pandas.read_csv(dir_path + "/prog_dad_jokes_.csv", header=None, names=['id', 'joke'], index_col=0)
#print(jokes.sample(replace = True).joke.tolist()[0])

def _get_joke():
    joke_msg = jokes.sample(replace = True).joke.tolist()[0]
    return joke_msg

#Getting around pythonanywhere proxy issue with twilio
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}


def _sendsms(number):
    error = None
    message = None
    error_code = None
    msg_body=_get_joke()
    error_uri = None
    try:
        client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTHTOKEN'], http_client=proxy_client )
        message = client.messages.create(from_= app.config['NUMBER'],\
                                         body= msg_body,\
                                         to= number)
    except TwilioRestException as e:
        error = e.msg
        error_code = e.code
        error_uri = e.uri

    return message, error, error_code, error_uri, msg_body

@app.route("/")
@app.route("/makeadevlol")
def Lol():
    return render_template('lol.html', text=_get_joke().split('\n'))

@app.route('/send_sms', methods=['GET', 'POST'])
def send_sms():
    form = PhoneForm()
    if form.validate_on_submit():
        session['phone'] = form.phone.data
        msg_sent, msg_error, error_code, error_uri, error_msg_body =_sendsms(session['phone'])
        if msg_error == None:
            with open(dir_path + "/logs/send_sms_log.json", "a+") as f:
                f.write(json.dumps(msg_sent._properties, indent=4, sort_keys=True, default=str))
            session['body'] = msg_sent.body
            session['date_sent'] = msg_sent.date_created
            session['to'] = msg_sent.to
            session['from'] = msg_sent.from_
            session['error_message'] = msg_sent.error_message
        else:
            error_log = {"body": error_msg_body, "date_created": datetime.now().isoformat(' ', 'seconds'),\
                         "date_sent": None, "date_updated": datetime.now().isoformat(' ', 'seconds'),\
                         "direction": "outbound-api", "error_code": error_code, "error_message": msg_error, "from_": app.config['NUMBER'],\
                         "messaging_service_sid": None, "num_media": "0", "num_segments": "1", "price": None, "price_unit": "USD",\
                         "sid": None, "status": "failed", "subresource_uris": None, "to": "+61421123456", "uri": error_uri}
            with open(dir_path + "/logs/send_sms_log.json", "a+") as f:
                f.write(json.dumps(error_log, indent=4, sort_keys=True, default=str))
            session['body'] = error_log["body"]
            session['date_sent'] = error_log["date_created"]
            session['to'] = error_log["to"]
            session['from'] = error_log["from_"]
            session['error_message'] = error_log["error_message"]
        return redirect(url_for('sms_receipt'))
    return render_template('phoneform.html', form=form)

#used for testing form functionality
@app.route('/show_phone')
def show_phone():
    return render_template('show_phone.html', phone=session['phone'])

@app.route('/sms_receipt')
def sms_receipt():
    return render_template('sms_receipt.html', to=session['to'], \
                            from_=session['from'], body=session['body'], \
                            date_sent=session['date_sent'], \
                            error_message=session['error_message'])

#To be used as Twilio webhook
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    if 'lol' in incoming_msg:
        # return a joke
        msg.body(_get_joke())
    else:
        msg.body("NoSenseOfHumourException raised!")
    return str(resp)



