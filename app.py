import json

from flask import Flask, render_template, request, make_response
from topproduct import topproducts, get_product_category, get_product_title

app = Flask(__name__)

@app.route('/')
def home():
    # from topproduct import topproducts
    # assert  False, topproducts

    # Maps
    for item in topproducts:
        print(item['title'])

    return render_template('front/index.html', topproducts =topproducts)

@app.route('/about')
def about():
    return render_template('front/about.html')

@app.route('/shop')
def shop():
    return render_template('front/products.html', topproducts=topproducts)

@app.route('/product/<product_name>')
def product(product_name):
    from topproduct import get_product_title
    product = get_product_title(product_name)
    if product is None:
        return "Product not found", 404
    related_product = get_product_category(product['category'])
    # assert False, product_name
    return render_template('front/product.html', product=product, related_product=related_product)

@app.route('/cart')
def cart():
    product_id = request.args.get("product_id")
    qty = request.args.get("qty", 1, type=int)
    
    cart_list = request.cookies.get('cart_list')
    cart_list = json.loads(cart_list) if cart_list else []
    
    if product_id:
        from topproduct import get_product_id
        product = get_product_id(product_id)
        if product:
            found = False
            for item in cart_list:
                if str(item['id']) == str(product_id):
                    item['qty'] += qty
                    if item['qty'] < 1:
                        item['qty'] = 1
                    found = True
                    break
            
            if not found and qty > 0:
                cart_list.append(
                    {
                        "id" : product['id'],
                        "title" : product['title'],
                        "qty" : qty,
                        "price" : product['price'],
                        "category" : product['category'],
                        "image" : product['image'],
                        "description" : product['description'],
                    }
                )

            from flask import redirect, url_for
            resp = redirect(url_for('cart'))
            resp.set_cookie('cart_list', json.dumps(cart_list))
            return resp

    return render_template("front/cart.html", cart_list=cart_list)

@app.route('/cart/remove')
def cart_remove():
    from flask import redirect, url_for
    product_id = request.args.get("product_id")
    cart_list = request.cookies.get('cart_list')
    cart_list = json.loads(cart_list) if cart_list else []
    
    if product_id:
        cart_list = [item for item in cart_list if str(item['id']) != str(product_id)]
        resp = redirect(url_for('cart'))
        resp.set_cookie('cart_list', json.dumps(cart_list))
        return resp
        
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_list = request.cookies.get('cart_list')
    cart_list = json.loads(cart_list) if cart_list else []

    # telegram BOT
    if request.method == 'POST':
        # Telegram Bot Credentials - Replace these with your actual keys
        TELEGRAM_BOT_TOKEN = "8647260942:AAFV7D02rIE2HApyOiJSgNEK33UiMCMmnqw"
        TELEGRAM_CHAT_ID = "-1003914228040"

        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        address = request.form.get('address')
        city = request.form.get('city')
        zip_code = request.form.get('zip')

        if cart_list:
            subtotal = sum(item['price'] * item['qty'] for item in cart_list)
            shipping = 15.00 if subtotal > 0 else 0
            tax = subtotal * 0.08
            total = subtotal + shipping + tax

            msg = f"🛒 *New Order Received!*\n\n"
            msg += f"👤 *Customer:* {first_name} {last_name}\n"
            msg += f"📍 *Address:* {address}, {city}, {zip_code}\n\n"
            msg += f"🛍️ *Items:*\n"
            for item in cart_list:
                msg += f"- {item['title']} (x{item['qty']}): ${item['price'] * item['qty']:.2f}\n"
            
            msg += f"\n💰 *Subtotal:* ${subtotal:.2f}\n"
            msg += f"🚚 *Shipping:* ${shipping:.2f}\n"
            msg += f"🧾 *Tax:* ${tax:.2f}\n"
            msg += f"💳 *Total:* ${total:.2f}\n"

            if TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN" and TELEGRAM_CHAT_ID != "YOUR_TELEGRAM_CHAT_ID":
                import urllib.request
                import json as json_lib
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": msg,
                    "parse_mode": "Markdown"
                }
                try:
                    req = urllib.request.Request(url, data=json_lib.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
                    urllib.request.urlopen(req)
                except Exception as e:
                    print(f"Error sending Telegram message: {e}")

        from flask import redirect, url_for
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('cart_list', '', expires=0)
        return resp

    return render_template('front/checkout.html', cart_list=cart_list)

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

