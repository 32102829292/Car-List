from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Car
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    car = Car.query.all()
    return render_template('index.html', cars=car)


@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        new_car = Car(name=name, quantity=quantity, price=price)
        db.session.add(new_car)
        db.session.commit()
        flash('Car added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_car(id):
    car =Car.query.get_or_404(id)
    if request.method == 'POST':
        car.name = request.form['name']
        car.quantity = request.form['quantity']
        car.price = request.form['price']
        db.session.commit()
        flash('Car updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', car=Car)

@app.route('/delete/<int:id>')
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)