from flask import Flask, redirect, render_template, url_for
app=Flask(__name__)

menu = {
    1: {"name": "Pepperoni", "price": 13.10, "description": "Hand-tossed dough, house-made tomato sauce, mozzarella cheese, and savory pepperoni."},
    2: {"name": "Margherita", "price": 12.95, "description": "Hand-tossed dough, tomato sauce, fresh mozzarella, vine-ripened tomatoes, fresh basil, and extra virgin olive oil."},
    3: {"name": "Prosciutto", "price": 16.70, "description": "Hand-tossed dough, tomato sauce, fresh mozzarella, thinly sliced prosciutto, arugula, shaved Parmesan, and extra virgin olive oil."},
    4: {"name": "Patron", "price": 23.99, "description": "Hand-stretched dough, tomato sauce, mozzarella cheese, pepperoni, Italian sausage, green bell peppers, red onions, mushrooms, and black olives."},
}

orders = []

@app.route('/')
def menu_page():
    return render_template('customer_order_page.html', menu=menu)

@app.route('/menu', methods=['GET', 'POST'])
def order_customer():
    return render_template('customer_order_page.html', pizzas=pizzas)

@app.route('/order/overview')
def order_overview():
    return render_template('order_overview.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/order/status')
def order_status():
    return render_template('order_status.html')

@app.route('/mario/order/overview')
def mario_order_overview():
    return render_template('mario_order_overview.html')

@app.route('/mario/orders')
def mario_orders():
    return render_template('mario_orders.html')

@app.route('/luigi/orders')
def luigi_orders():
    return render_template('luigi_orders.html')



if __name__ == "__main__":
    app.run(port=5000, debug=True)