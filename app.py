from flask import Flask, jsonify, render_template, url_for
from sqlalchemy import create_engine
import pandas as pd
import os
import json

"""To configure the SDK, initialize it with the integration 
before or after your app has been initialized:"""
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


#################################################
# MySQL Database Setup
#################################################
# Import DB user and password
try:
    from api_keys import mysql_hostname
    from api_keys import mysql_port
    from api_keys import mysql_username
    from api_keys import mysql_pass
    from api_keys import sentry_sdk_dsn

except:
    pass


# MySQL specific connection string
database_name = "etlprojectdb"
table_price = "price"
table_companies = "companies"
table_subsectors = "sub_sectors"

# Try to find an environment variable (specially for Heroko) or use database credentials.
try:
    database_url = os.environ["DATABASE_URL"]
    sentry_sdk_dsn = os.environ["Sentry_Sdk_DSN"]
except KeyError:
    database_url = f"mysql+mysqlconnector://{mysql_username}:{mysql_pass}@{mysql_hostname}:{mysql_port}/{database_name}"


# Create the engine
engine = create_engine(database_url)


# Sentry monitoring setup
# https://sentry.io/
sentry_sdk.init(
    dsn=sentry_sdk_dsn, integrations=[FlaskIntegration()], traces_sample_rate=1.0,
)


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
# Home page.
@app.route("/")
def welcome():
    return render_template("index.html")


# About page.
@app.route("/about")
def about():
    return render_template("about.html")


# Return a table with the query results for the companies table
@app.route("/SP500")
def companies_table():
    """Return a table with the list of companies"""

    companies_df = pd.read_sql(f"SELECT * FROM {table_companies}", engine)
    # html = companies_df.to_html()
    # return html

    list_companies = companies_df.to_dict(orient="records")

    return render_template("company_list.html", list_companies=list_companies)


# Return a json with the query results for the companies table
@app.route("/company/json")
def company_json():

    companies_df = pd.read_sql(f"SELECT * FROM {table_companies}", engine)

    result = companies_df.to_json(orient="records")
    parsed = json.loads(result)

    return jsonify(parsed)


# Return a table with the query results for the companies table
@app.route("/<company>/<string:start>/<string:end>")
def price_list(company, start, end):
    """Return a table with the list stock price"""

    prices_df = pd.read_sql(
        f"Select c.comp_tick, c.sect_name, c.sub_sect_name, p.close_price AS CLOSING_PRICE, p.volume, p.date from {table_companies} AS c join {table_price} as p on p.comp_tick = c.comp_tick where c.comp_tick = '{company}' and p.date between '{start}' and '{end}'",
        engine,
    )

    # html = prices_df.to_html()
    # return html

    company_prices = prices_df.to_dict(orient="records")

    return render_template("company_closing.html", company_prices=company_prices)


# Return a table with the query results for the companies table
@app.route("/<company>/<start>/<end>/json")
def price_list_json(company, start, end):
    """Return a table with the list stock price"""

    prices_df = pd.read_sql(
        f"Select c.comp_tick, c.sect_name, c.sub_sect_name, p.close_price AS CLOSING_PRICE, p.volume, p.date from {table_companies} AS c join {table_price} as p on p.comp_tick = c.comp_tick where c.comp_tick = '{company}' and p.date between '{start}' and '{end}'",
        engine,
    )

    result = prices_df.to_json(orient="records")
    parsed = json.loads(result)

    return jsonify(parsed)


# Return a json version of the company
@app.route("/company/<tick>/json")
def company_tick_json(tick):

    Comp_info = pd.read_sql(
        f"Select c.comp_name, c.sect_name, c.first_trade_date from {table_companies} AS c  WHERE c.comp_tick = '{tick.upper()}'",
        engine,
    )

    result = Comp_info.to_json(orient="records")
    parsed = json.loads(result)

    return jsonify(parsed)


# Return a table data of the company
@app.route("/company/<tick>")
def company_tick_table(tick):

    Comp_info = pd.read_sql(
        f"Select c.comp_name, c.sect_name, c.first_trade_date from {table_companies} AS c  WHERE c.comp_tick = '{tick.upper()}'",
        engine,
    )

    # html = Comp_info.to_html()
    # return html

    company_data = Comp_info.to_dict(orient="records")

    return render_template("company_detail.html", company_data=company_data)


# The server is set to run on the computer IP address on the port 5100
# Go to your http://ipaddress:5100
if __name__ == "__main__":
    app.run(debug=False)
    # app.run(host="0.0.0.0", port=5100, debug=False)
