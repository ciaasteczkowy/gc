import os
import piecash
from flask import Flask, render_template
import json

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

@app.route('/')
def hello():
	book = piecash.open_book(uri_conn=os.environ['JAWSDB_URL'], readonly=False, do_backup=False)



	return render_template("index.html", accounts=book.root_account.children(name="Wydatki").children)


# app.run(host="0.0.0.0", port=8000, debug=True)