from flask import Flask, request, render_template, redirect, url_for, flash, make_response
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Sample menu and seating data
menu = [
    {"name": "Pizza", "price": 10},
    {"name": "Burger", "price": 8},
    {"name": "Idli", "price": 10},
    {"name": "Dosa", "price": 20},
    {"name": "Vada", "price": 15},
    {"name": "Uttapam", "price": 25},
    {"name": "Pesarattu", "price": 20},
    {"name": "Upma", "price": 20},
    {"name": "Puri", "price": 20}
]

seating = ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6", "Table 7", "Table 8", "Table 9", "Table 10", "Table 11", "Table 12", "Table 13", "Table 14", "Table 15", "Table 16"]

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def show_menu():
    if request.method == 'POST':
        selected_items = request.form.getlist('items')
        return redirect(url_for('show_seating', items=selected_items))
    return render_template('menu.html', menu=menu)

@app.route('/seating', methods=['GET', 'POST'])
def show_seating():
    if request.method == 'POST':
        selected_table = request.form.get('table')
        if not selected_table:
            flash('Please select a table.')
            return redirect(url_for('show_seating', items=request.form.getlist('items')))
        selected_items = request.form.getlist('items')
        total = sum(item['price'] for item in menu if item['name'] in selected_items)
        return redirect(url_for('payment', table=selected_table, total=total, items=selected_items))
    selected_items = request.args.getlist('items')
    return render_template('seating.html', seating=seating, items=selected_items)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        table = request.form.get('table')
        total = request.form.get('total')
        items = request.form.getlist('items')
        return render_template('payment.html', table=table, total=total, items=items)
    table = request.args.get('table')
    items = request.args.getlist('items')
    total = sum(item['price'] for item in menu if item['name'] in items)
    return render_template('payment.html', table=table, total=total, items=items)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    table = request.form['table']
    total = request.form['total']
    items = request.form.getlist('items')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Order Details", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Table: {table}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Total: ${total}", ln=True, align='L')
    pdf.cell(200, 10, txt="Items:", ln=True, align='L')
    
    for item in items:
        pdf.cell(200, 10, txt=item, ln=True, align='L')
    
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=order_details.pdf'
    return response

@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    total = request.form['total']
    table = request.form['table']
    items = request.form.getlist('items')
    return render_template('order_confirmation.html', total=total, table=table, items=items)

@app.route('/login', methods=['POST'])
def login_post():
    phone_number = request.form['phone']
    if not phone_number.isdigit():
        flash('Invalid phone number. Please enter digits only.')
        return redirect(url_for('login'))
    return redirect(url_for('show_menu'))

if __name__ == '__main__':
    app.run(debug=True)