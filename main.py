from flask import Flask, render_template, request, redirect, flash
from database import conn, cur
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

cur.execute("CREATE TABLE IF NOT EXISTS products(id SERIAL PRIMARY KEY, name VARCHAR(100), buying_price NUMERIC(14,2),selling_price NUMERIC(14,2), stock_quantity INTEGER);")

cur.execute("CREATE TABLE IF NOT EXISTS sales(id SERIAL PRIMARY KEY, pid INTEGER REFERENCES products(id), quantity INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

conn.commit()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact-us')
def contact():
    return render_template("contact.html")


@app.route('/products', methods=["GET", "POST"])
def products():
    if request.method == "GET":
        cur.execute("select * from products")
        products = cur.fetchall()
        return render_template("products.html", products=products)
    else:
        print("-------", request.form)
        name = request.form["name"]
        buying_price = float(request.form["bp"])
        selling_price = float(request.form["sp"])
        stock_quantity = int(request.form["stq"])
        query_insert = "insert into products(name,buying_price,selling_price,stock_quantity)"\
            "values('{}',{},{},{})".format(
                name, buying_price, selling_price, stock_quantity)
        cur.execute(query_insert)
        conn.commit()
        return redirect('/products')


@app.route("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        cur.execute("select * from sales")
        sales = cur.fetchall()
        cur.execute("select * from products")
        products = cur.fetchall()
        return render_template("sales.html", sales=sales, products=products)
    else:
        pid = int(request.form["pid"])
        quantity = int(request.form["quantity"])
        query_make_sales = "insert into sales(pid,quantity,created_at)"\
            "values({},{},now())".format(pid, quantity)
        cur.execute(query_make_sales)
        conn.commit()
        return redirect('/sales')


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    cur.execute("SELECT prodcuts.name AS product_name, SUM(sales.quantity * (products.selling_price - products.buying_price)) AS total_profit FROM sales JOIN products ON")
    sales_result = cur.fetchall()
    x = []
    y = []
    for i in sales_result:
        x.append(i[0])
        y.append(float(i[1]))

    cur.execute(
        "select products.name as product_name, sum(sales.quantity * (products.selling.price - products.buying_price) as total_profit from sales")
    profit_results = cur.fetchall()

    return render_template("dasboard.html", x-x, y-y, profit_results-profit_results)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()

        print("GET request received. users fecthed:", users)  # Debugging output
        return render_template("register.html", users=users)
    else:
        # Get from data
        full_name = request.form["name"]
        email_address = request.form["email"]
        password = request.form["Pass"]

        # Inster user into database safely
        query = """
    INSERT INTO users (full_name,email_address,password)
    values (%s, %s, %s) RETURNING id;
    """
        cur.execute(query, (full_name, email_address, password))
        user_id = cur.fetchone()[0]  # Retrive inserted user ID
        conn.commit()

        print(f"User registered with ID: {user_id}")

        # Redirect back to \register after successful registration
        return redirect("/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_address = request.form["emailaddress"]
        password = request.form["password"]
        querylogin = "select id from users where email_address = '{}' and password = '{}'".format(
            email_address, password)
        cur.execute(querylogin)
        row = cur.fetchone()

        if row is None:
            flash("Invalid credentials")
            return render_template("login.html")
        else:
            return redirect("/dashboard")
    else:
        return render_template("login.html")


app.run(debug=True)
