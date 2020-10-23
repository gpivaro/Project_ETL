from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
import pandas as pd
import os


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
@app.route("/")
def welcome():
    return (
        f"<H1>Welcome to the ETL Project Page<H1>"
        f"<p>In this page we will show our analysis for stock prices of companies on S&P500<p>"
        f"<p>List of Companies<p>"
        f"/companies<br/>"
    )


# Return a table with the query results for the companies table
@app.route("/companies")
def measurment():
    """Return a table with the last measurments"""

    companies = pd.read_sql(f"SELECT * FROM {table_companies}", engine)

    html = companies.to_html()

    return html


# The server is set to run on the computer IP address on the port 5100
# Go to your http://ipaddress:5100
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
