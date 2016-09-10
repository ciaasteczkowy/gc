import os
import piecash
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def hello():
	book = piecash.open_book(uri_conn=os.environ['JAWSDB_URL'], readonly=False, do_backup=False)
	return render_template("index.html", accounts=book.accounts)


app.run(port=8000, debug=True)