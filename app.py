from flask import Flask, render_template, request, redirect, url_for, session, flash
from authlib.integrations.flask_client import OAuth
import mysql.connector

from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Orders, OrderTracking

app = Flask(__name__)
app.secret_key = "super_secret_key"


#-----------------------------------
# SQLAlchemy configuration
#----------------------------------
app.config.from_object(Config)

db.init_app(app)


with app.app_context():
    db.create_all()


#-----------------------------------
# OAuth configuration (Google)
#----------------------------------
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id="885034579992-mn8lgacub75v0rnrferc14834tg322bj.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Hitesh123",
    database="bookish_db",
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()

# ========================
# HOME PAGE
# ========================
@app.route("/")
def home():
    if "username" in session:
        return render_template("index.html")
    else:
        return render_template("index.html")

from flask import Flask, request, redirect, url_for, flash, render_template, session
import re   # ✅ FIX ADDED

@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        action = request.form.get("action")

        # ========================
        # SIGNUP
        # ========================
        if action == "signup":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|[a-zA-Z0-9.-]+\.edu|[a-zA-Z0-9.-]+\.in)$'

            # ✅ FIX WORKING
            if not email or not re.match(email_pattern, email):
                flash("Invalid email! Use gmail.com, any .edu or .in domain.", "error")
                return redirect(url_for("auth"))

            cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
            existing = cursor.fetchone()

            if existing:
                flash("Email already exists!", "error")
                return redirect(url_for("auth"))

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            mysql_db.commit()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth"))

        # ========================
        # LOGIN
        # ========================
        elif action == "login":
            email = request.form.get("email")
            password = request.form.get("password")

            cursor.execute("SELECT username, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                db_username, db_password = user

                if password == db_password:
                    session.clear()
                    session["users"] = email
                    session["username"] = db_username

                    flash(f"Welcome, {db_username}!", "success")

                    response = redirect(url_for("home"))
                    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                    response.headers["Pragma"] = "no-cache"
                    response.headers["Expires"] = "0"
                    return response
                else:
                    flash("Incorrect password!", "error")
                    return redirect(url_for("auth"))
            else:
                flash("Email not found!", "error")
                return redirect(url_for("auth"))

    return render_template("new.html")

# ========================
# GOOGLE LOGIN
# ========================
@app.route("/google_login")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

# ========================
# GOOGLE CALLBACK
# ========================
@app.route("/google_callback")
def google_callback():
    token = google.authorize_access_token()
    user_info = token.get("userinfo")

    if not user_info:
        flash("Google login failed!", "error")
        return redirect(url_for("auth"))

    email = user_info["email"]
    username = user_info.get("name", email.split("@")[0])

    session.clear()
    session["users"] = email
    session["username"] = username

    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, "google_oauth")
        )
        db.commit()

    flash(f"Welcome, {username}!", "success")
    return redirect(url_for("home"))


# ========================
# ADMIN PAGE
# ========================
@app.route("/admin")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("auth"))

    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()

    return render_template("admin.html", orders=orders)

# ========================
# SEARCH BOX
# ========================
@app.route("/search")
def search():
    query = request.args.get("q")

    # Simple filter
    results = []
    if query:
        results = [book for book in books if query.lower() in book.lower()]

    return render_template("search.html", query=query, results=results)

# ========================
# SHOP PAGE
# ========================
@app.route("/shop")
def shop():
    return render_template("shop.html")

# ========================
# BOOK DETAILS (ID BASED)
# ========================
@app.route("/book/<int:book_id>")
def book_details_by_id(book_id):

    book = {
        "id": book_id,
        "title": "Sample Novel Title",
        "author": "John Writer",
        "price": 199,
        "image": "/static/images/book1.jpg",
        "description": "Lorem ipsum dolor sit amet..."
    }

    return render_template("book_details.html", book=book)


# ========================
# BOOK DETAILS (DYNAMIC URL PARAM)
# ========================
@app.route('/book_details')
def book_details():
    title = request.args.get('title')
    price = request.args.get('price')
    image = request.args.get('image')

    # 🔥 IMAGE → PDF mapping
    pdf = BOOK_PDF_MAP.get(image)

    return render_template(
        "book_details.html",
        # title=title,
        price=int(price),
        image=image,
        pdf=pdf
    )

# =======================
# READ PAGE
# =======================
@app.route('/read')
def read_page():
    pdf = request.args.get("pdf")
    return render_template('read.html', pdf=pdf)

BOOK_PDF_MAP = {
    "images/novel2.jpg": "demon_slayer.pdf",
    "images/novel3.jpg": "jujutsu_kaisan.pdf",
    "images/novel4.jpg": "one_piece.pdf",
    "images/novel5.jpg": "magic_and_mashle.pdf",
    "images/novel6.jpg": "solo_leveling.pdf",

    "images/novel7.jpg": "verity.pdf",
    "images/novel8.jpg": "friend.pdf",
    "images/novel9.jpg": "orient.pdf",
    "images/novel10.jpg": "the_girl.pdf",
    "images/novel11.jpg": "family_upstar.pdf",

    "images/novel12.jpg": "dragon_ball.pdf",
    "images/novel13.jpg": "chainsaw_man.pdf",
    "images/novel14.jpg": "my_dreams.pdf",
    "images/novel15.jpg": "legacy_of_gods.pdf",
    "images/novel16.jpg": "five_survive.pdf"
}

# ========================
# BLOG PAGE
# ========================
@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/blog/<int:blog_id>")
def blog_detail(blog_id):

    blogs = {
        1: {
            "title": "How to Choose Trekking Boots",
            "image": "https://images.unsplash.com/photo-1522163182402-834f871fd851",
            "content": "Choosing trekking boots is very important for comfort and safety. Always select boots based on terrain, weather, and duration. Look for ankle support, waterproof material, and proper grip..."
        },
        2: {
            "title": "Why Renting Boots is Smart",
            "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519",
            "content": "Renting boots helps you save money and avoid carrying heavy luggage. It is perfect for occasional trekkers and travelers who want flexibility without investing in expensive gear..."
        },
        3: {
            "title": "Top 10 Trekking Places",
            "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
            "content": "India offers amazing trekking locations like Manali, Kedarnath, and Valley of Flowers. These places provide breathtaking views and unforgettable adventure experiences..."
        }
    }

    blog = blogs.get(blog_id)

    return render_template("blog_detail.html", blog=blog)

# ========================
# FEATURED PAGE
# ========================
@app.route("/featured")
def featured():
    return render_template("featured.html")

# ========================
# CART
# ========================
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    # CHECK LOGIN FIRST
    if "users" not in session:
        return redirect(url_for("auth"))

    title = request.form.get("title")
    price = request.form.get("price")
    image = request.form.get("image")

    cart = session.get("cart", [])

    cart.append({
        "title": title,
        "price": price,
        "image": image
    })

    session["cart"] = cart

    return redirect(url_for("cart"))


#----------------CART-----------------------
@app.route("/cart")
def cart():

    if "users" not in session:
        return redirect(url_for("auth"))

    # Get saved addresses
    cursor.execute(
        "SELECT * FROM addresses WHERE user_email=%s",
        (session["users"],)
    )

    addresses = cursor.fetchall()

    return render_template(
        "cart.html",
        cart=session.get("cart", []),
        addresses=addresses
    )


# ========================
# DELETE ITEM FROM CART
# ========================
@app.route("/delete_item/<int:index>")
def delete_item(index):

    cart = session.get("cart", [])

    if index < len(cart):
        cart.pop(index)

    session["cart"] = cart

    return redirect(url_for("cart"))


# ========================
# ORDER PAGE ADDRESS
# ========================
@app.route("/add-address", methods=["GET","POST"])
def add_address():

    if "users" not in session:
        return redirect(url_for("auth"))

    if request.method == "POST":

        full_name = request.form.get("full_name")
        mobile = request.form.get("mobile")
        pincode = request.form.get("pincode")
        house = request.form.get("house")
        area = request.form.get("area")
        landmark = request.form.get("landmark")
        city = request.form.get("city")
        state = request.form.get("state")

        cursor.execute("""
        INSERT INTO addresses
        (user_email,full_name,mobile,pincode,house,area,landmark,city,state)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(
        session["users"],
        full_name,
        mobile,
        pincode,
        house,
        area,
        landmark,
        city,
        state
        ))

        db.commit()

        flash("Address added successfully","success")

        return redirect(url_for("cart"))

    return render_template("add_address.html")

# =======================
# SUBSCRIPTION PAGE
# =======================
@app.route('/subscription')
def subscription():
    return render_template('subscription.html')


# ========================
# ORDER
# ========================
from datetime import datetime

@app.route("/order", methods=["GET", "POST"])
def order_page():

    if "users" not in session:
        return redirect(url_for("auth"))

    # ========================
    # GET ADDRESS (DB)
    # ========================
    cursor.execute("""
    SELECT * FROM addresses
    WHERE user_email=%s
    ORDER BY id DESC LIMIT 1
    """, (session["users"],))

    address = cursor.fetchone()

    # ========================
    # BUY NOW PRODUCT (FROM FORM)
    # ========================
    product = None

    if request.method == "POST":
        product = {
            "title": request.form.get("title"),
            "price": request.form.get("price"),
            "image": request.form.get("image")
        }

    # ========================
    # CART ITEMS (SESSION)
    # ========================
    cart = session.get("cart", [])

    # ========================
    # CURRENT DATE
    # ========================
    current_date = datetime.now().strftime("%d %B %Y")

    # ========================
    # RENDER PAGE
    # ========================
    return render_template(
        "order.html",
        product=product,
        cart=cart,
        address=address,
        current_date=current_date
    )


# ========================
# ORDER TRACKING
# ========================
@app.route("/track")
def track_order():
    return render_template("track.html", address=session.get("address"))

# ========================
# LOGOUT
# ========================
@app.route("/logout")
def logout():
    session.pop("users", None)
    session.pop("username", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

# ========================
# CONTACT & PRIVACY PAGES
# ========================
@app.route("/contact")
def contact():
    return "<h2>Contact Page</h2>"

@app.route("/privacy")
def privacy():
    return "<h2>Privacy Policy Page</h2>"

# ========================
# RUN APP
# ========================
if __name__ == "__main__":
    app.run(debug=True)