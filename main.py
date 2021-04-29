from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import json 
import pymysql
import traceback
import jwt
import time

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    if type(error).__name__ == 'NotFound':
        status_code = 404 
    elif type(error).__name__ == 'TypeError':
        status_code = 500
    
    return jsonify({'msg': type(error).__name__}), status_code

# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     valid_token = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'password', \
#         algorithm='HS256')
#     print(valid_token)
#     if token == valid_token:
#         pass
#     else:
#         return {
#             'msg': 'invalid token'
#         }

@app.route("/")
def index():
    return 'Netflix and  Chill'

@app.route("/user/<user_id>/account/<id>/deposit", methods=['POST'])
def deposit(user_id, id):
    connection, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = """
        UPDATE API.accounts SET balance = '{}' WHERE id = '{}' and deleted is not True
    """.format(balance, id)
    response = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'Failed'
        
    connection.commit()
    return jsonify(response)

@app.route("/user/<user_id>/account/<id>/withdraw", methods=['POST'])
def withdraw(user_id, id):
    connection, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response = {}
    if balance < 0:
        response['msg'] = 'Money is not enough to withdraw'
        connection.commit()
        return jsonify(response)
    else:
        sql = """
            UPDATE API.accounts SET balance = '{}' WHERE id = '{}' and deleted is not True
        """.format(balance, id)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'Failed'
            
        connection.commit()
        return jsonify(response)
    
def get_account(id):
    connection = pymysql.connect(host='localhost', user='root', \
                 password='Password1234!', db='API', cursorclass=pymysql.cursors.DictCursor)
    sql = """select * from accounts where id = '{}' and deleted is not True""".format(id)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
    connection.commit()
    return connection, result


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)