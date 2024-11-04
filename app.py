

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
def show_menu():
    return render_template('static_menu.html', menu=menu)

@app.route('/menu/<int:table>', methods=['GET', 'POST'])
def menu_page(table):
    if request.method == 'POST':
        global orders

        # Process selected pizzas and their quantities
        for pizza in menu:
            pizza_name = pizza['name']
            pizza_price = pizza['price']
            description=pizza['description']
            quantity = request.form.get(f'quantity_{pizza_name}')  # Get the quantity for this pizza
            selected = request.form.getlist('selected_pizza')  # Get list of selected pizzas

            if pizza_name in selected and quantity.isdigit() and int(quantity) > 0:
                # Add selected pizza, quantity, and default status to the order
                orders.append({
                    "table": table,
                    "name": pizza_name,
                    "price": pizza_price,
                    "quantity": int(quantity),
                    "status": "Preparing",  # Default status for new orders
                    "description": description
                })
        
        return redirect(url_for('order_overview', table=table))
    return render_template('customer_order_page.html', menu=menu, table=table)

@app.route('/order/overview/<int:table>')
def order_overview(table):
    # Step 1: Create a new list of orders that match the specified table
    filtered_orders = []
    for order in orders:
        if order['table'] == table:
            filtered_orders.append(order)  # Add to the new list if it matches

    # Step 2: Calculate the total cost of the filtered orders
    total = sum(order['price'] * order['quantity'] for order in filtered_orders)

    # Step 3: Render the template with only the filtered orders
    return render_template('order_overview.html', orders=filtered_orders, total=total, table=table)


@app.route('/payment/<int:table>')
def payment(table):
    return render_template('payment.html', table=table)

@app.route('/order/status/<int:table>')
def order_status(table):
    return render_template('order_status.html', orders=orders, table=table)

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
                    "status": "Preparing",
                    "description": pizza['description']
                })
        return redirect(url_for('mario_orders_overview'))
    return render_template('mario_orders.html')

@app.route('/mario/orders/overview')
def mario_orders_overview():
    return render_template('mario_overview.html', orders=orders)

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

@app.route('/delete_order/<int:index>', methods=['POST'])
def delete_order(index):
    # Ensure the index is valid and remove the order
    if 0 <= index < len(orders):
        orders.pop(index)
    return redirect(url_for('luigi_orders_page'))

if __name__ == '__main__':
    app.run(debug=True)










