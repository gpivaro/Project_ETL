from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
import pandas as pd
import os
import json

# Import DB user and password
from api_keys import mysql_hostname
from api_keys import mysql_port
from api_keys import mysql_username
from api_keys import mysql_pass

# MySQL specific connection string
database_name = "etlprojectdb"
table_price = "price"
table_companies = "companies"
table_subsectors = "sub_sectors"

database_url = f"mysql+mysqlconnector://{mysql_username}:{mysql_pass}@{mysql_hostname}:{mysql_port}/{database_name}"


# Create the engine
engine = create_engine(database_url)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Use Flask to create your routes.

# Routes

# /
# Home page. List all routes that are available.
@app.route("/etl")
def welcome():
    return (
        f"<h1>Welcome to the ETL Project Page</h1>"
        f"<p>In this page we will show our analysis for stock prices of companies on S&P500<p>"
        f"<h4>Links available:</h4>"
        f"/company<br/>"
        f"/company/comp_tick<br/>"
        f"/price<br/>"
        f"/about<br/>"
    )


# Home page. List all routes that are available.
@app.route("/etl/about")
def about():
    return f"<h1>About</h1>"


# Return a table with the query results for the companies table
@app.route("/etl/company")
def listcompanies():
    """Return a table with the list of companies"""

    companies_df = pd.read_sql(f"SELECT * FROM {table_companies}", engine)

    html = companies_df.to_html()

    return html

    #result = companies_df.to_json(orient="records")
    #parsed = json.loads(result)

    #return jsonify(parsed)



# Return a table with the query results for the companies table
@app.route("/etl/price")
def listprice():
    """Return a table with the list stock price"""

    prices_df = pd.read_sql(f"SELECT * FROM {table_price}", engine)

    html = prices_df.to_html()

    return html


# Return a json version of the company
@app.route("/etl/company/<tick>")
def company_tick(tick):

    Comp_info = pd.read_sql(f"Select c.comp_name, c.sect_name, c.first_trade_date from {table_companies} AS c  WHERE c.comp_tick = '{tick.upper()}'", engine)

    result = Comp_info.to_json(orient="records")
    parsed = json.loads(result)

    return jsonify(parsed)


# The server is set to run on the computer IP address on the port 5100
# Go to your http://ipaddress:5100
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
