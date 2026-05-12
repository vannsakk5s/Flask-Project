from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('front/index.html')

@app.route('/about')
def about():
    return render_template('front/about.html')

@app.route('/shop')
def shop():
    return render_template('front/products.html')

@app.route('/product')
def product():
    return render_template('front/product.html')

@app.route('/cart')
def cart():
    return render_template('front/cart.html')

@app.route('/checkout')
def checkout():
    return render_template('front/checkout.html')

@app.route('/account')
def account():
    return render_template('front/account.html')

@app.route('/login')
def login():
    return render_template('front/createUser.html')
    
@app.route('/register')
def register():
    return render_template('front/createUser.html')
    
@app.route('/forgot-password')
def forgot_password():
    return render_template('front/forgotPw.html')

if __name__ == '__main__':
    app.run(debug=True)

