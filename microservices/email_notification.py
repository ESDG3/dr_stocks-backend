from flask import Flask, request, jsonify
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

#POST
@app.route("/email_noti/send", methods=['POST'])
def get_stock_info():
    senddata = request.get_json()
    sg = sendgrid.SendGridAPIClient(api_key="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")
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