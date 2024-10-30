from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulated data for tables and orders
tables = {
    1: "Free",
    2: "Free",
    3: "Free",
    4: "Free"
}

orders = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard_front')
def front_dashboard():
    return render_template('dashboard_front.html', tables=tables, orders=orders)

@app.route('/dashboard_kitchen')
def kitchen_dashboard():
    return render_template('dashboard_kitchen.html', orders=orders)

@app.route('/new_order', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        table_number = int(request.form['table_number'])
        tables[table_number] = "Occupied"

        pizza_types = ["Margherita", "Prosciutto", "Pepperoni", "Patron"]
        for pizza_type in pizza_types:
            quantity = int(request.form.get(f'pizza_choice[{pizza_type}]', 0))
            if quantity > 0:
                for _ in range(quantity):
                    orders.append({"table": table_number, "pizza": pizza_type, "status": "In Progress"})
        
        return redirect(url_for('front_dashboard'))

    return render_template('new_order.html', tables=tables)

@app.route('/update_table/<int:table_number>')
def update_table(table_number):
    tables[table_number] = "Free"
    global orders
    updated_orders = []
    
    for order in orders:
        if order['table'] != table_number:
            updated_orders.append(order)
    
    orders = updated_orders
    return redirect(url_for('front_dashboard'))

@app.route('/mark_pizza_done/<int:order_index>')
def mark_pizza_done(order_index):
    orders[order_index]['status'] = "Completed"
    table_number = orders[order_index]['table']
    all_completed = True
    
    for order in orders:
        if order['table'] == table_number:
            if order['status'] != "Completed":
                all_completed = False
                break

    if all_completed:
        tables[table_number] = "Free"

    return redirect(url_for('kitchen_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
