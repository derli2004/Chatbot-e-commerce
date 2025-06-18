
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db
from database.models import Product
from database.mock_data import add_mock_data
from logic import get_book_suggestions



def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow frontend to talk to backend easily
    init_db(app)

    # Ensure mock data is added only if not already present
    with app.app_context():
        add_mock_data()

    return app

app = create_app()

dummy_orders = {
    "ORD123": {"status": "Shipped", "delivery_days": 3},
    "ORD456": {"status": "Shipped", "delivery_days": 5},
    "ORD789": {"status": "Processing", "delivery_days": 7},
    "ORD101": {"status": "Delivered", "delivery_days": 0},
    "ORD202": {"status": "Pending", "delivery_days": 10},
}
import re
user_states = {}
def extract_order_id(message):
    match = re.search(r'ORD\d{3}', message)
    if match:
        return match.group(0)
    return None

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    user_id = request.remote_addr  # you can use IP for now to track users
    order_id = extract_order_id(user_message)
    
    

    # List of predefined options
    options_list = [
        "Search Products",
        "Return Products",
        "Track Order",
        "Refund Request",
        "Connect to Customer Care"
    ]

    # List of return reasons
    return_reasons = [
        "Wrong item delivered",
        "Product damaged",
        "Item not as described",
        "Changed my mind",
        "Other"
    ]
    

    # Smart extraction of product name using regex
    def extract_product_name(message):
        match = re.search(r'\b(?:need|search|find|buy|looking for|get|want|search products for)\b\s+(?:a|an|the)?\s*(\w+)', message.lower())
        if match:
            return match.group(1)
        return message.strip()

    # Handle if user is in a special state (waiting for order ID or refund ID)
    if user_id in user_states:
        state = user_states[user_id]

        # Handle return flow (check first)
        if state == 'awaiting_return_order_id':
            order_id = user_message.strip().upper()
            if order_id in dummy_orders:
                user_states[user_id] = 'awaiting_return_reason' # Transition to waiting for return reason 
                bot_message = f"Got it. Please select a return reason for Order ID: {order_id}."
                return jsonify({"message": bot_message, "options": return_reasons})
            else:
                bot_message = f"Sorry, I couldn't find the order with ID {order_id}. Please check and try again."
            return jsonify({"message": bot_message,"options": options_list})

        if state == 'awaiting_return_reason':
            if user_message in return_reasons:
                user_states.pop(user_id)  # Clear the user state
                bot_message = f"Return initiated for your Order ID. Our team will contact you shortly!"
                return jsonify({"message": bot_message,"options":options_list})
            else:
                bot_message = "Please select a valid return reason."
                return jsonify({"message": bot_message, "options": return_reasons})

        # Handle other special states like 'Track Order', 'Refund Request', etc.
        if state == 'awaiting_track_order_id':
            order_id = user_message.strip().upper()
            user_states.pop(user_id)
            if order_id in dummy_orders:
                order = dummy_orders[order_id]
                bot_message = f"Order {order_id} is currently '{order['status']}'. Expected delivery in {order['delivery_days']} days."
                return jsonify({"message": bot_message, "options": options_list})
            else:
                bot_message = f"Sorry, I couldn't find the order with ID {order_id}. Please check and try again."
            return jsonify({"message": bot_message,"options": options_list})
        
        if state == 'awaiting_refund_request_id':
            order_id = user_message.strip().upper()
            user_states.pop(user_id)
            if order_id in dummy_orders:
                bot_message = f"Refund process started for Order ID: {order_id}. You will get your refund within 5-7 working days."
                return jsonify({"message": bot_message,"options": options_list})
                
            
            else:
                bot_message = f"Sorry, I couldn't find the order with ID {order_id}. Please check and try again."
            return jsonify({"message": bot_message,"options": options_list})


    # If it's the first interaction, show the welcome message and options
    if user_message.lower() == "start" or not user_message:
        bot_response = {
            "message": "Welcome to our store! How can I assist you today?",
            "options": options_list
        }

    elif "suggest" in user_message.lower():
        # Calling the suggestion function from logic.py (modify based on your requirements)
        suggestion = get_book_suggestions(user_message)
        
        bot_response = {
            "message": f"Here is a suggestion: {suggestion}",
            "options": options_list
        }
    elif user_message.lower() in ["hello", "hi", "hey", "good morning", "good evening"]:
        bot_response = {
        "message": "Hello! How can I assist you today?",
        "options": options_list
    }
    elif user_message.lower() in ["thank you", "thanks", "thankyou"]:
       bot_response = {
        "message": "You're most welcome! Anything else I can help you with?",
        "options": options_list
    }
    # Handle "Return Products" option first, ensure priority
    elif user_message.lower() in ["return","return products","return items"]:
        user_states[user_id] = 'awaiting_return_order_id'
        bot_response = {
            "message": "Please provide your Order ID to initiate the return process."
        }
    
    elif user_message.lower() in ["welcome", "you're welcome", "you are welcome"]:
        bot_response = {
        "message": "Glad to be of help! Let me know if you need anything else.",
        "options": options_list
    }
        
    elif user_message.lower() in ["how are you", "how are you doing"]:
        bot_response = {
        "message": "I'm just a bot, but I'm doing great! Thanks for asking. How can I assist you today?",
        "options": options_list
    }
        
    elif user_message.lower() in ["bye", "goodbye", "see you", "talk to you later"]:
        bot_response = {
        "message": "Goodbye! Have a wonderful day! 🌟",
        "options": options_list
    }

    # Handle "Track Order" option
    elif "track order" in user_message.lower():
        user_states[user_id] = 'awaiting_track_order_id'
        bot_response = {
            "message": "Please provide your Order ID to track your order."
        }

    # Handle "Refund Request" option
    elif "refund request" in user_message.lower():
        user_states[user_id] = 'awaiting_refund_request_id'
        bot_response = {
            "message": "Please provide your Order ID to start the refund process."
        }

    # Handle "search products" flow only if it's not 'Return Products' request
    elif "search products" in user_message.lower() and 'awaiting_return_order_id' not in user_states.get(user_id, ''):
        bot_response = {
            "message": "Sure! Please tell me the product you're looking for."
        }
   
    elif "connect to customer care" in user_message.lower():
     customer_care_message = """
     
     Feel free to reach out to us via email at support@ourstore.com or call us at +123-456-7890.
    Thank you for your patience!
    
    """
     bot_response = {"message": customer_care_message,"options": options_list}
    
    
    # Default case for when no specific action is taken, and product search is attempted
    else:
        cleaned_message = extract_product_name(user_message)
        product = Product.query.filter(Product.name.ilike(f'%{cleaned_message}%')).first()

        if product:
         bot_response = {
            "message": f"{product.name} \n\n{product.description}\n\n Price: Rs.{product.price}", "image_url": product.image_url,
            "options": options_list
            }
        else:
            bot_message = "Sorry, we couldn't find that product. Please choose an option below."
            bot_response = {
                "message": bot_message,
                "options": options_list
            }



    return jsonify(bot_response)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
