

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample menu data
menu = [
    {"name": "Pepperoni", "price": 13.10, "description": "Hand-tossed dough, house-made tomato sauce, mozzarella cheese, and savory pepperoni."},
    {"name": "Margherita", "price": 12.95, "description": "Hand-tossed dough, tomato sauce, fresh mozzarella, vine-ripened tomatoes, fresh basil, and extra virgin olive oil."},
    {"name": "Prosciutto", "price": 16.70, "description": "Hand-tossed dough, tomato sauce, fresh mozzarella, thinly sliced prosciutto, arugula, shaved Parmesan, and extra virgin olive oil."},
    {"name": "Patron", "price": 23.99, "description": "Hand-stretched dough, tomato sauce, mozzarella cheese, pepperoni, Italian sausage, green bell peppers, red onions, mushrooms, and black olives."},
]

# Orders list to store current orders
orders = []
order_index = 0

@app.route('/')
def home():
    # Redirect to the menu page
    return redirect(url_for('menu_page'))

@app.route('/menu/<int:table>', methods=['GET', 'POST'])
def menu_page(table):
    if request.method == 'POST':
        global orders

        # Process selected pizzas and their quantities
        for pizza in menu:
            pizza_name = pizza['name']
            pizza_price = pizza['price']
            quantity = request.form.get(f'quantity_{pizza_name}')  # Get the quantity for this pizza
            selected = request.form.getlist('selected_pizza')  # Get list of selected pizzas

            if pizza_name in selected and quantity.isdigit() and int(quantity) > 0:
                # Add selected pizza, quantity, and default status to the order
                orders.append({
                    "table": table,
                    "name": pizza_name,
                    "price": pizza_price,
                    "quantity": int(quantity),
                    "status": "Preparing"  # Default status for new orders
                })
        
        return redirect(url_for('order_overview'))
    return render_template('customer_order_page.html', menu=menu, table=table)

@app.route('/order/overview')
def order_overview():
    total = sum(order['price'] * order['quantity'] for order in orders)
    return render_template('order_overview.html', orders=orders, total=total)

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/order/status')
def order_status():
    return render_template('order_status.html', orders=orders)

@app.route('/mario/orders', methods=['GET', 'POST'])
def mario_orders_page():
    if request.method == 'POST':
        table = request.form.get('table')
        for pizza in menu:
            pizza_name = pizza["name"].lower()
            quantity = request.form.get(pizza_name)
            
            if quantity and quantity.isdigit() and int(quantity) > 0:
                orders.append({
                    "table": table,
                    "name": pizza["name"],
                    "price": pizza["price"],
                    "quantity": int(quantity),
                    "status": "Preparing"
                })
        return redirect(url_for('order_overview'))
    return render_template('mario_orders.html')


@app.route('/luigi/orders')
def luigi_orders_page():
    return render_template('luigi_orders.html', orders=orders)

@app.route('/mark_order_completed', methods=['POST'])
def mark_next_order_completed():
    global order_index

    data = request.get_json() 
    if order_index < len(orders):
        if data and "message" in data:
            # Decrease the quantity of the current order
            orders[order_index]["quantity"] -= 1
            
            # Check if the quantity has reached zero
            if orders[order_index]["quantity"] <= 0:
                orders[order_index]["status"] = "Completed"
                order_index += 1

    if order_index >= len(orders):  # Ensure the order_index is within bounds
        order_index = 0

if __name__ == '__main__':
    app.run(debug=True)










