# -*- coding: utf-8 -*-
import json

import os
import piecash
import pymysql
from flask import Flask, request, render_template
from flask_basicauth import BasicAuth
from piecash import Transaction, Split, factories

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['DEBUG'] = False

app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_USER')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_PASS')
app.config['BASIC_AUTH_FORCE'] = not app.config['DEBUG']

basic_auth = BasicAuth(app)


@app.route('/')
def hello():
    return render_template("index.html")

def get_book():
    book = piecash.open_book(uri_conn=os.environ['JAWSDB_URL'], readonly=False, do_backup=False,
                             open_if_lock=True)

    return book


@app.route('/data')
def get_income_ajax():
    try:
        book = get_book()
    except Exception as e:
        print(e)
        return json.dumps({'error': '{}'.format(e)}), 500

    income = get_income(book)
    expense = get_expense(book)
    accounts = [{'id': a.guid, 'name': a.fullname, 'shortname': a.name} for a in book.accounts]
    transactions = sorted(book.transactions, key=lambda x: x.post_date, reverse=True)[:6]
    print(transactions)
    splits = [{
        'amount': -float((t.splits[0] if t.splits[0].account.type == 'EXPENSE' else t.splits[1]).value),
        'account': (t.splits[0] if t.splits[0].account.type == 'EXPENSE' else t.splits[1]).account.fullname
        } for t in transactions]

    ctx = {
        'income': '{:.2f}'.format(income),
        'expense': '{:.2f}'.format(expense),
        'balance': '{:.2f}'.format(income + expense),
        'accounts': accounts,
        'splits': splits
    }

    return json.dumps(ctx)


@app.route('/add_entry', methods=("POST",))
def add_entry():
    account = request.form.get('expense_account')
    amount = request.form.get('expense_amount')

    if not account or not amount:
        json.dumps({'error': 'Buuuu!'})

    try:
        book = get_book()
    except Exception as e:
        print(e)
        return json.dumps({'error': '{}'.format(e)})

    try:
        c1 = book.commodities[0]

        account = book.accounts(fullname=account)
        account_from = book.accounts(fullname="Aktywa:Aktywa bie??ce:ROR")

        tr = Transaction(currency=c1, description='', splits=[
            Split(account=account_from, value='-{}'.format(amount)),
            Split(account=account, value=amount)
        ])

        book.save()
        book.close()

    except Exception as e:
        print(e)
        return json.dumps({'error': '{}'.format(e)}), 500

    return json.dumps({'status': 'success'})


def get_splits_sum(book, account_type):
    _sum = 0
    for account in book.accounts:
        if account.type == account_type and account.placeholder != 1:
            for split in account.splits:
                _sum -= split.value

    return _sum


def account_balance(account):
    balance = 0
    for split in account.splits:
        balance -= split.value

    return balance


def get_income(book):
    return float(get_splits_sum(book, "INCOME"))


def get_expense(book):
    return float(get_splits_sum(book, "EXPENSE"))


def income_tree(account):
    tree = {
        'name': u'{}'.format(account.name),
        'balance': account_balance(account),
        'children': []
    }
    for acc in account.children:
        tree['children'].append(income_tree(acc))

    for child in tree['children']:
        tree['balance'] += child['balance']

    return tree

# app.run(host="0.0.0.0", port=8000, debug=True)
