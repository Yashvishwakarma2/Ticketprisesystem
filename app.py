from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# -----------------------------
# Ticket Prices
# -----------------------------

TICKET_PRICES = {
    "movie": 150,
    "bus": 80,
    "train": 120,
    "flight": 5000
}

TICKET_NAMES = {
    "movie": "Movie Ticket",
    "bus": "Bus Ticket",
    "train": "Train Ticket",
    "flight": "Flight Ticket"
}


# -----------------------------
# Home Page
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Calculate Ticket Price
# -----------------------------

@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json()

    ticket_type = data.get("ticket_type")
    quantity = data.get("quantity")

    if ticket_type not in TICKET_PRICES:
        return jsonify({
            "success": False,
            "message": "Invalid ticket type"
        }), 400

    try:
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Quantity must be greater than 0"
        }), 400

    price = TICKET_PRICES[ticket_type]
    total = price * quantity

    return jsonify({
        "success": True,
        "ticket": TICKET_NAMES[ticket_type],
        "price": price,
        "quantity": quantity,
        "total": total
    })


# -----------------------------
# Book Ticket
# -----------------------------

@app.route("/book", methods=["POST"])
def book():

    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    ticket_type = data.get("ticket_type")
    quantity = data.get("quantity")

    # Validation
    if not name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone are required"
        }), 400

    if ticket_type not in TICKET_PRICES:
        return jsonify({
            "success": False,
            "message": "Invalid ticket type"
        }), 400

    try:
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Invalid quantity"
        }), 400

    # Price calculation
    price = TICKET_PRICES[ticket_type]
    total = price * quantity

    # Generate booking ID
    booking_id = str(uuid.uuid4())[:8].upper()

    booking = {
        "booking_id": booking_id,
        "name": name,
        "phone": phone,
        "ticket": TICKET_NAMES[ticket_type],
        "price": price,
        "quantity": quantity,
        "total": total
    }

    return jsonify({
        "success": True,
        "booking": booking
    })


# -----------------------------
# Run Application
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)