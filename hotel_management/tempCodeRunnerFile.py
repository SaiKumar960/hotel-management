from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Sample menu and seating data
menu = [
    {"name": "Pizza", "price": 10},
    {"name": "Burger", "price": 8}
]

seating = ["Table 1", "Table 2"]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/menu')
def show_menu():
    return render_template('menu.html', menu=menu)

@app.route('/seating')
def show_seating():
    return render_template('seating.html', seating=seating)

@app.route('/confirm_order')
def confirm_order():
    return render_template('order_confirmation.html')

@app.route('/login', methods=['POST'])
def login_post():
    phone_number = request.form['phone']
    return redirect(url_for('show_menu'))

if __name__ == '__main__':
    app.run(debug=True)
