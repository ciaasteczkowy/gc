import os
import piecash
from flask import Flask, render_template
import json

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

@app.route('/')
def hello():
	try:
		book = piecash.open_book(uri_conn=os.environ['JAWSDB_URL'], readonly=False, do_backup=False, open_if_lock=True)
	except Exception as e:
		return e.message

	income = get_income(book)
	outcome = get_expense(book)

	return render_template("index.html", income=income, outcome=outcome, balance=income-outcome)

def get_splits_sum(account):
	_sum = 0
	for split in account.splits:
		_sum += split.value
	return _sum

def get_income(book):
	income = 0
	for account in book.accounts:
		if account.type == "INCOME" and account.placeholder != 1:
			income -= get_splits_sum(account)

	return income

def get_expense(book):
	expense = 0
	for account in book.accounts:
		if account.type == "EXPENSE" and account.placeholder != 1:
			expense += get_splits_sum(account)

	return expense


# app.run(host="0.0.0.0", port=8000, debug=True)