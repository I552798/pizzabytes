from flask import Flask, render_template
app=Flask(__name__)

# @app.route('/')
# def Display():

@app.route('/menu')
def order_customer():
    return render_template('customer_order_page.html')

@app.route('/order/overview')
def order_overview():
    return render_template('order_overview.html')

@app.route('/payment')
def  payment():
    return render_template('payment.html')

@app.route('/order/status')
def  order_status():
    return  render_template('order_status.html')




if __name__ == "__main__":
    app.run(port=5000, debug=True)