from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Chemin correct pour la base de données dans le répertoire "instance"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définition du modèle Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    site = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        price = request.form['price']
        site = request.form['site']
        website = request.form['website']
        image_url = request.form.get('image_url', '')

        new_product = Product(name=name, type=type, price=price, site=site, website=website, image_url=image_url)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.type = request.form['type']
        product.price = float(request.form['price'])
        product.site = request.form['site']
        product.website = request.form['website']
        product.image_url = request.form.get('image_url', '')

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
