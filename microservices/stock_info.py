from flask import Flask, request, jsonify
import finnhub, base64
app = Flask(__name__)

#GET
@app.route("/stock_info/<string:stock_symbol>")
def get_stock_info(stock_symbol):
    text = "YzhtNWZrYWFkM2k5aHVjcDk4NzA="
    msg = base64.b64decode(text)
    key = str(msg.decode('ascii'))
    finnhub_client = finnhub.Client(api_key=key)
    return finnhub_client.quote(stock_symbol)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)