

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


menu = [
     {"name": "Pepperoni", "price": 13.10, "description": "Hand-tossed dough, house-made tomato sauce, mozzarella cheese, and savory pepperoni."},
     {"name": "Margherita", "price": 12.95, "description": "Hand-tossed dough, tomato sauce, fresh mozzarella, vine-ripened tomatoes, fresh basil, and extra virgin olive oil."},
     {"name": "Prosciutto", "price": 16.70, "description": "Hand-tossed dough, tomato sauce, fresh mozzarella, thinly sliced prosciutto, arugula, shaved Parmesan, and extra virgin olive oil."},
     {"name": "Patron", "price": 23.99, "description": "Hand-stretched dough, tomato sauce, mozzarella cheese, pepperoni, Italian sausage, green bell peppers, red onions, mushrooms, and black olives."},
]
# Orders list to store current orders
orders = []

@app.route('/')
def home():
    # Redirect to the menu page
    return redirect(url_for('menu_page'))

@app.route('/menu', methods=['GET', 'POST'])
def menu_page():
    if request.method == 'POST':
        # Clear the orders for a new session
        global orders
        orders = []  # Reset orders for a new submission

        # Process selected pizzas and their quantities
        for pizza in menu:
            pizza_name = pizza['name']
            quantity = request.form.get(f'quantity_{pizza_name}')  # Get the quantity for this pizza
            selected = request.form.getlist('selected_pizza')  # Get list of selected pizzas
            
            if pizza_name in selected and quantity.isdigit() and int(quantity) > 0:
                # Add selected pizza and quantity to the order
                orders.append({
                    "name": pizza_name,
                    "price": pizza['price'],
                    "quantity": int(quantity)
                })
        
        return redirect(url_for('order_overview'))

    return render_template('customer_order_page.html', menu=menu)

@app.route('/order/overview')
def order_overview():
    total = sum(order['price'] * order['quantity'] for order in orders)
    return render_template('order_overview.html', orders=orders, total=total)


@app.route('/payment')
def payment():
    return render_template('payment.html')


@app.route('/order/status')
def order_status():
    return render_template('order_status.html')

@app.route('/mario/orders', methods=['GET', 'POST'])
def mario_orders():
    if request.method == 'POST':
        table = request.form.get('table')
        pepperoni = int(request.form.get('pepperoni', 0))
        margherita = int(request.form.get('margherita', 0))
        prosciutto = int(request.form.get('prosciutto', 0))
        patron = int(request.form.get('patron', 0))

        # Add orders for the selected table
        if pepperoni > 0:
            orders.append({"table": table, "name": "Pepperoni", "price": 13.10, "quantity": pepperoni})
        if margherita > 0:
            orders.append({"table": table, "name": "Margherita", "price": 12.95, "quantity": margherita})
        if prosciutto > 0:
            orders.append({"table": table, "name": "Prosciutto", "price": 16.70, "quantity": prosciutto})
        if patron > 0:
            orders.append({"table": table, "name": "Patron", "price": 23.99, "quantity": patron})

        return redirect(url_for('order_overview'))
    return render_template('mario_orders.html')

@app.route('/luigi/orders')
def luigi_orders():
    return render_template('luigi_orders.html')

if __name__ == '__main__':
    app.run(debug=True)









