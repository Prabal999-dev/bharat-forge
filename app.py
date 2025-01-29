import asyncio
import logging
from flask import Flask, render_template, request, jsonify
from chatbot import SupplierAssistant

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
assistant = SupplierAssistant()

# Mock data for suppliers
suppliers = [
    {
        "id": 1,
        "name": "Industrial Metals Co.",
        "rating": 4.8,
        "products": [
            {"name": "Steel Sheets", "price": "₹45,000/ton", "stock": 500},
            {"name": "Aluminum Blocks", "price": "₹32,000/ton", "stock": 300},
        ],
        "location": "Mumbai, Maharashtra"
    },
    {
        "id": 2,
        "name": "Tech Components Ltd.",
        "rating": 4.5,
        "products": [
            {"name": "Circuit Boards", "price": "₹2,500/unit", "stock": 1000},
            {"name": "Sensors", "price": "₹800/unit", "stock": 2500},
        ],
        "location": "Pune, Maharashtra"
    },
    {
        "id": 3,
        "name": "Raw Materials Plus",
        "rating": 4.9,
        "products": [
            {"name": "Carbon Fiber", "price": "₹75,000/kg", "stock": 100},
            {"name": "Industrial Plastics", "price": "₹15,000/ton", "stock": 800},
        ],
        "location": "Bangalore, Karnataka"
    }
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()

    if not user_message:
        logging.warning("Received empty chat message.")
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = asyncio.run(assistant.get_response(user_message))  # Proper async handling
        logging.info(f"User: {user_message} | Chatbot: {response['response']}")
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in chatbot response: {str(e)}")
        return jsonify({'error': 'Chatbot service unavailable'}), 500

@app.route('/suppliers')
def supplier_page():
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/product')
def product_page():
    return render_template('product.html')

@app.route('/raw')
def raw():
    return render_template('raw.html')

@app.route('/trends')
def trends():
    return render_template('trends.html')

if __name__ == '__main__':
    app.run(debug=True)
