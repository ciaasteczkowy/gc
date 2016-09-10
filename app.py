import os
import piecash
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	try:
		book = piecash.open_book(uri_conn=os.environ['JAWSDB_URL'], readonly=False)
	except Exception as e:
		return e.message
	return 'Hello World!'