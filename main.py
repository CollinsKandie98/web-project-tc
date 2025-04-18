from flask import Flask,render_template,request,redirect,flash,session,url_for
from database import conn,cur
from functools import wraps
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = '_5#y2L"F4Q8z\n\xebuhbivyc]/'

cur.execute("CREATE TABLE IF NOT EXISTS products(id serial PRIMARY KEY, name VARCHAR(100) NOT NULL, buying_price FLOAT, selling_price FLOAT, stock_quantity INT DEFAULT 0)")
cur.execute("CREATE TABLE IF NOT EXISTS sales(id serial PRIMARY KEY, pid INT, quantity INT, created_at TIMESTAMP,CONSTRAINT myproduct FOREIGN KEY(pid) references products(id) on UPDATE cascade on DELETE restrict)")
cur.execute("CREATE TABLE IF NOT EXISTS purchases(id SERIAL PRIMARY KEY, expense_category VARCHAR(100) NOT NULL, description TEXT, amount DECIMAL(10,2) NOT NULL, purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
cur.execute("CREATE TABLE IF NOT EXISTS stock (id serial PRIMARY KEY, pid int, quantity numeric(5,2), created_at TIMESTAMP, CONSTRAINT myproduct FOREIGN KEY(pid) references products(id) on UPDATE cascade on DELETE restrict);")
cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR,password VARCHAR);")
conn.commit()

def login_required(f):
    @wraps(f)
    def protected(*args, **kwargs):
        if 'email' not in session:
            flash('You must first log in')
            next_url = request.url #Store the requested URL
            return redirect(url_for('login', next=next_url)) #Pass the next URL
        return f(*args, **kwargs)
    return protected


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact-us')
def contact():
    return render_template("contact.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method =="POST":

        fullName = request.form["fullname"]
        email = request.form["emailaddress"]
        password = request.form["password"]
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user_query ="INSERT INTO users(name,email_address,password)"\
                        "VALUES('{}', '{}', '{}')".format(fullName,email, hash_password)
        print("The hashed passowrd is" + hash_password)
        
        cur.execute(new_user_query)
        conn.commit()

        return redirect('/register')
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get('next') #Get the next URL if provided
    if request.method == "POST":
        email_address = request.form["emailaddress"]
        password = request.form["password"]
        querylogin = "select id from users where email_address = '{}' and password = '{}'".format(email_address, password)
        cur.execute(querylogin)
        row = cur.fetchone()

        if row is None:
            flash("Invalid credentials")
            return render_template("login.html")
        else:
            next_url =request.form['next_url']
            session['email'] = email_address
            if next_url == "None":
                return redirect(url_for('dashboard'))
            else:
                url = "/"+next_url.split('/')[-1]
                return redirect(url)
    else:
        return render_template("login.html", next_url=next_url)

if __name__ == '__main__':
    app.run(debug=True)



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
@login_required
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

@app.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():
    if request.method == "GET":
        cur.execute("select * from expenses")
        expenses = cur.fetchall()
        return render_template("expenses.html", expenses=expenses)
    else:
        expense_category = request.form["expense_category"]
        description = request.form["description"]
        amount = float(request.form["amount"])

        query_create_expense = """
            INSERT INTO expenses (expense_category, description, amount, purchase_date) 
            "VALUES ('{}', '{}', '{}', NOW())"
        """
        cur.execute(query_create_expense, (expense_category, description, amount))
        conn.commit()

        return redirect("/expenses")


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
    return render_template("dashboard.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "GET":
#         cur.execute("SELECT * FROM users")
#         users = cur.fetchall()

#         print("GET request received. users fecthed:", users)  # Debugging output
#         return render_template("register.html", users=users)
#     else:
#         # Get from data
#         full_name = request.form["name"]
#         email_address = request.form["email"]
#         password = request.form["Pass"]

#         # Inster user into database safely
#         query = """
#     INSERT INTO users (full_name,email_address,password)
#     values (%s, %s, %s) RETURNING id;
#     """
#         cur.execute(query, (full_name, email_address, password))
#         user_id = cur.fetchone()[0]  # Retrive inserted user ID
#         conn.commit()

#         print(f"User registered with ID: {user_id}")

#         # Redirect back to \register after successful registration
#         return redirect("/register")


