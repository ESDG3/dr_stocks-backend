from flask import Flask, request, jsonify
import sendgrid, base64
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

#POST
@app.route("/email_noti/send", methods=['POST'])
def get_stock_info():
    senddata = request.get_json()
    text = "U0cuN1ZPa0lCamhROHFFUDdweDdvNkFRUS53OFhmYVJ2QUYxcDZxSHBxclF6dWI5WUFteHZweUtuTm1WZkl5bVFvMXRR"
    msg = base64.b64decode(text)
    key = msg.decode('ascii')
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
    return jsonify(
        {
            "code":str(response.status_code),
            "data":res
        }
    )





if __name__ == '__main__':
    app.run(port=5000, debug=True)