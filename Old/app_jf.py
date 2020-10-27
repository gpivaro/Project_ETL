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
    return render_template("index.html")


# Home page. List all routes that are available.
@app.route("/etl/about")
def about():
    return render_template("about.html")


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
@app.route("/etl/<company>/<start>/<end>")
def listprice(company, start, end):
    """Return a table with the list stock price"""

    prices_df = pd.read_sql(f"Select c.comp_tick, c.sect_name, c.sub_sect_name, p.close_price AS CLOSING_PRICE, p.volume, p.date from {table_companies} AS c join {table_price} as p on p.comp_tick = c.comp_tick where c.comp_tick = '{company}' and p.date between '{start}' and '{end}'",engine)

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