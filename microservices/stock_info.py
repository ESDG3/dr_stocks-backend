from flask import Flask, request, jsonify
import finnhub
app = Flask(__name__)

#GET
@app.route("/stock_info/<string:stock_symbol>")
def get_stock_info(stock_symbol):
    finnhub_client = finnhub.Client(api_key="c8m5fkaad3i9hucp9870")
    return finnhub_client.quote(stock_symbol)
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)