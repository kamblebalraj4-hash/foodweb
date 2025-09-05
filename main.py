from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# MENU DATA
menu = {
    "Burgers": {
        "Cheese Burger": 90,
        "Veg Burger": 70,
        "Chicken Burger": 110,
        "Double Patty Burger": 130,
        "Spicy Paneer Burger": 100
    },
    "Pizzas": {
        "Chicken Pizza": 100,
        "Veg Pizza": 80,
        "Margherita Pizza": 95,
        "Pepperoni Pizza": 120,
        "Farmhouse Pizza": 110
    },
    "Sides": {
        "Fries": 50,
        "Cheese dip": 10,
        "Garlic Bread": 40,
        "Onion Rings": 45,
        "Mozzarella Sticks": 60
    },
    "Drinks": {
        "Coke": 20,
        "Pepsi": 20,
        "Orange Juice": 30,
        "Lemonade": 25,
        "Iced Tea": 30
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
    selected_items = request.form.getlist('item')
    total_cost = 0
    items_with_prices = []

    # Price lookup
    def find_price(item_name, menu_dict):
        for key, value in menu_dict.items():
            if isinstance(value, dict):
                result = find_price(item_name, value)
                if result is not None:
                    return result
            elif key == item_name:
                return value
        return None

    for item in selected_items:
        price = find_price(item, menu)
        if price is not None:
            total_cost += price
            items_with_prices.append((item, price))

    return render_template('order.html', items=items_with_prices, total=total_cost)

@app.route('/checkout', methods=['POST'])
def checkout():
    return render_template('checkout.html')

@app.route("/confirm", methods=["POST"])
def confirm():
    name = request.form.get("name")
    address = request.form.get("address")
    phone = request.form.get("phone")
    payment_method = request.form.get("payment")

    if not name or not address or not phone or not payment_method:
        return "Missing form data", 400

    if payment_method == "card":
        card_number = request.form.get("card_number")
        expiry = request.form.get("expiry")
        cvv = request.form.get("cvv")
        if not all([card_number, expiry, cvv]):
            return "Missing card details", 400

    # If QR code, card details are not needed
    return render_template("confirmation.html", name=name)

@app.route('/payment')
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
