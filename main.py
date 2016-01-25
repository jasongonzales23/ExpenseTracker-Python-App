"""`main` is the top level module for your Flask application."""
# Import the Flask Framework
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
from flask import Flask, jsonify, request
import os
import MySQLdb as mysql

app = Flask(__name__)
_INSTANCE_NAME = 'expensetracker-1199:expensetracker-1200'
env = os.getenv('SERVER_SOFTWARE')

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello New World!'

@app.route('/index', methods=['GET'])
def show_health():
    return 'Stuff is working yo!'

@app.route('/api/v1/expenses', methods=['GET'])
def get_expenses():
    if (env and env.startswith('Google App Engine/')):
        db = mysql.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='expensetracker', user='root', charset='utf8')
    else:
        db = mysql.connect(host="127.0.0.1", port=3306, db='expensetracker', user='root', charset='utf8')

    cursor = db.cursor()
    cursor.execute('SELECT * FROM expenses')

    columns = [desc[0] for desc in cursor.description]
    result = []
    rows = cursor.fetchall()

    for row in rows:
        row = dict(zip(columns, row))
        result.append(row)

    return jsonify({'expenses': result})

@app.route('/api/v1/expenses', methods=['POST'])
def create_expense():

    amount = request.json['amount']
    description = request.json['description']

    if (env and env.startswith('Google App Engine/')):
        db = mysql.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='expensetracker', user='root', charset='utf8')
    else:
        db = mysql.connect(host="127.0.0.1", port=3306, db='expensetracker', user='root', charset='utf8')

    cursor = db.cursor()
    cursor.execute('INSERT INTO expenses (amount, description) VALUES (%s, %s)', (amount, description))
    db.commit()
    db.close()

    return jsonify({'expense': {"amount": amount, "description": description}}), 201

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

"""
expenses = [
    {
        'expenseId': 1,
        'amount': 40,
        'description': 'Whole Foods',
        'createdAt': '2016-01-22'
    },
    {
        'expenseId': 2,
        'amount': 45,
        'description': 'Other Aves',
        'createdAt': '2016-01-23'
    }
]
"""
