#!/usr/bin/env python3

import json
import os

import amqp_setup

import sendgrid, base64
from sendgrid.helpers.mail import Mail, Email, To, Content

def receiveEmailNotification():
    amqp_setup.check_setup()

    queue_name = 'Email_Notification'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    print("\nReceived an email notification log by " + __file__)
    get_stock_info(json.loads(body))
    print() # print a new line feed

def get_stock_info(senddata):
    text = "U0cuN1ZPa0lCamhROHFFUDdweDdvNkFRUS53OFhmYVJ2QUYxcDZxSHBxclF6dWI5WUFteHZweUtuTm1WZkl5bVFvMXRR"
    msg = base64.b64decode(text)
    key = str(msg.decode('ascii'))
    sg = sendgrid.SendGridAPIClient(api_key=key)
    from_email = Email("dr.stocks.pte.ltd@gmail.com")  # Change to your verified sender
    to_email = To(senddata["Email"])  # Change to your recipient
    subject = senddata["Subject"]
    content = Content("text/plain", senddata["Content"])
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    res = str(response.headers).split("\n")
    print(
        {
            "code":str(response.status_code),
            "data":res
        }
    )


if __name__ == '__main__':
    app.run(port=5003, debug=True)
