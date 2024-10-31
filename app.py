from flask import Flask, redirect, render_template, url_for
app=Flask(__name__)

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

@app.route('/menu', methods=['GET', 'POST'])
def menu_page():
    if request.method == 'POST':
        pizza_name = request.form.get('pizza_name')
        quantity = request.form.get('quantity')
        
        # Add selected pizza and quantity to the order
        if quantity.isdigit() and int(quantity) > 0:
            orders.append({"name": pizza_name, "price": next(item['price'] for item in menu if item['name'] == pizza_name), "quantity": int(quantity)})
        return redirect(url_for('order_overview'))
    return render_template('customer_order_page.html', menu=menu)

@app.route('/order/overview')
def order_overview():
    return render_template('order_overview.html', orders=orders)

@app.route('/order/status')
def order_status():
    return render_template('order_status.html')

if __name__ == '__main__':
    app.run(debug=True)



# @app.route('/')
# def menu_page():
#     return render_template('customer_order_page.html', menu=menu)


@app.route('/payment')
def payment():
    return render_template('payment.html')


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