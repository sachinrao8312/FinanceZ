import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    stocks_db = db.execute("SELECT SUM(shares) AS shares,price,symbol  FROM portfolio GROUP BY symbol HAVING user_id =? ", user_id)

    total_shares_price = db.execute("SELECT SUM(price) AS price FROM portfolio")

    cash_db = db.execute("SELECT cash FROM users WHERE id =?", user_id)

    cash = cash_db[0]["cash"]

    # Total Amount of Money user have
    total = total_shares_price[0]["price"]
    total = total+cash

    for stock in stocks_db:
        look = lookup(stock["symbol"])
        stock["name"] = look["name"]
        stock["cur_price"] = look["price"]
        stock["total_shares_price"] = stock["cur_price"] * stock["shares"]

    return render_template("index.html", stockz=stocks_db, cash=usd(cash), total=usd(total))
    # return apology("HOPE")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":

        #  looking the stocks
        stock = lookup(request.form.get("symbol"))

        # Shares Qty
        shares = int(float((request.form.get("shares"))))

        if not shares == float((request.form.get("shares"))) or shares < 0:
            return apology("Invalid No of Shares", 400)

        if stock == None:
            return apology("Invalid Stock Symbol", 400)

        transaction_amt = shares * int(stock["price"])

        user_id = session["user_id"]

        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        user_cash = user_cash_db[0]["cash"]

        date = datetime.datetime.now()

        if user_cash < transaction_amt:
            return apology("Not enough money")

        update_cash = user_cash - transaction_amt

        # updating user cash
        db.execute("UPDATE users SET cash =? WHERE id =?", update_cash, user_id)

        # Adding user transaction into portfolio
        db.execute("INSERT INTO portfolio(user_id, symbol, price, shares,date) VALUES(?,?,?,?,?)",
                   user_id, stock["symbol"], stock["price"], shares, date)

        flash("Yay! Stocks are bought.")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    shares_hist = db.execute("SELECT *  FROM portfolio GROUP BY symbol HAVING user_id =? ", user_id)

    for stock in shares_hist:
        look = lookup(stock["symbol"])
        stock["name"] = look["name"]
        stock["cur_price"] = look["price"]

    return render_template("history.html", stockz=shares_hist)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":
        symbol = lookup(request.form.get("symbol"))

        if symbol == None:
            return apology("Invalid Stock Symbol", 400)

        else:
            return render_template("quoted.html", symbol=symbol)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide password", 400)

        # Ensure confirmation was given
        elif not request.form.get("confirmation"):
            return apology("Please re-enter password")

        # Ensure password matches was given
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password doesn't password")

        # No errors then pass data in users database
        else:
            username = request.form.get("username")
            hash = generate_password_hash(request.form.get("password"))

        # Query database to ensure username isn't already taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username is already taken", 400)

        # INSERTING into user table
        rows = db.execute("INSERT INTO users(username,hash) VALUES(?,?)", username, hash)

        flash("Yay! You have been registered!!")
        return redirect("/")
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":

        # get the user's current stocks
        portfolio = db.execute("SELECT symbol FROM portfolio GROUP BY symbol   HAVING user_id = ?", session["user_id"])

        # render sell.html form, passing in current stocks
        return render_template("sell.html", portfolio=portfolio)

    elif request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)
        rows = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        # return apology if symbol invalid/ not owned
        if len(rows) < 1:
            return apology("must provide valid stock symbol", 400)

        # cast shares from form to int
        shares = int(shares)
        
        # return apology if shares not provided. buy form only accepts positive integers
        if not shares or shares < 1:
            return apology("must provide valid number of shares", 403)

        # current shares of this stock
        oldshares = rows[0]['shares']

       

        # return apology if trying to sell more shares than own
        if shares > oldshares:
            return apology("shares sold can't exceed shares owned", 400)

        # get current value of stock price times shares
        sold = quote["price"] * shares

        # add value of sold stocks to previous cash balance
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session['user_id'])
        cash = cash[0]["cash"]
        cash = cash + sold

        # update cash balance in users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash, session["user_id"])

        # subtract sold shares from previous shares
        newshares = oldshares - shares

        date = datetime.datetime.now()

        # if shares remain, update portfolio table with new shares
        if newshares > 0:
            db.execute("UPDATE portfolio SET shares =?,date =? WHERE symbol = ? AND user_id = ?",
                       newshares, date, symbol, session["user_id"])

        # otherwise delete stock row because no shares remain
        else:
            db.execute("DELETE FROM portfolio WHERE symbol = ? AND user_id = ?", symbol, session["user_id"])

        flash("Stocks are sold!!")
        # redirect to index page
        return redirect("/")