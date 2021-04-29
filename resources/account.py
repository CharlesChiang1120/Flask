from flask_restful import Resource, reqparse
import pymysql
from flask import jsonify
import traceback

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')

class Account(Resource):
    
    def db_init(self):
        connection = pymysql.connect(host='localhost', user='root', \
            password='Password1234!', db='API', cursorclass=pymysql.cursors.DictCursor)
        return connection
    
    def get(self, user_id, id):
        connection = self.db_init()
        with connection.cursor() as cursor:
            sql = """select * from accounts where id = '{}' and deleted is not True""".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
        connection.commit()
        return jsonify({'data': result})
    
    def patch(self, user_id, id):
        connection = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']
        }
        
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + " = "+ "'{}'".format(value))
        query = ", ".join(query)
        
        sql = """
            UPDATE accounts SET {} WHERE (id = '{}')
        """.format(query, id)
        
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
    
    def delete(self, user_id, id):
        connection = self.db_init()
        sql = """
            UPDATE accounts SET deleted = True WHERE (id = '{}')
        """.format(id)
        
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
        
        
class Accounts(Resource):
    
    def db_init(self):
        connection = pymysql.connect(host='localhost', user='root', \
            password='Password1234!', db='API', cursorclass=pymysql.cursors.DictCursor)
        return connection
    
    def get(self, user_id):
        connection = self.db_init()
        with connection.cursor() as cursor:
            sql = 'select * from accounts where user_id = "{}" and deleted is not True'.format(user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
        return jsonify({'data': result})
        
    def post(self, user_id):
        connection = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance': arg['balance'],
            'account_number': arg['account_number'],
            'user_id': arg['user_id']
        }
        
        sql = """
            INSERT INTO accounts (balance, account_number, user_id) VALUES ('{}', '{}', '{}')
        """.format(account['balance'], account['account_number'], account['user_id'])
        
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