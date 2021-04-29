from flask_restful import Resource, reqparse
import pymysql
from flask import jsonify, make_response
import traceback

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource):
    def db_init(self):
        connection = pymysql.connect(host='localhost', user='root', \
            password='Password1234!', db='API', cursorclass=pymysql.cursors.DictCursor)
        return connection
    
    def get(self, id):
        connection = self.db_init()
        with connection.cursor() as cursor:
            sql = """select * from users where id = '{}' and deleted is not True""".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
        connection.commit()
        return jsonify({'data': result})
    
    def patch(self, id):
        connection = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note']
        }
        query = []
        for key, value in user.items():
            if value != None:
                query.append(key + " = "+ "'{}'".format(value))
        query = ", ".join(query)
        
        sql = """
            UPDATE users SET {} WHERE (id = '{}')
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
    
    def delete(self, id):
        connection = self.db_init()
        sql = """
            UPDATE users SET deleted = True WHERE (id = '{}')
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
        
        
class Users(Resource):
    def db_init(self):
        connection = pymysql.connect(host='localhost', user='root', \
            password='Password1234!', db='API', cursorclass=pymysql.cursors.DictCursor)
        return connection
    
    def get(self):
        connection = self.db_init()
        arg = parser.parse_args()
        with connection.cursor() as cursor:
            sql = 'select * from users where deleted is not True'
            if arg['gender'] != None:
                sql += ' and gender = "{}"'.format(arg['gender'])
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
        return jsonify({'data': result})
        
    def post(self):
        connection = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note']
        }
        
        sql = """
            INSERT INTO users (name, gender, birth, note) VALUES ('{}', '{}', '{}', '{}')
        """.format(user['name'], user['gender'], user['birth'], user['note'])
        
        response = {}
        status_code = 200
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                response['msg'] = 'success'
        except:
            status_code = 400
            traceback.print_exc()
            response['msg'] = 'Failed'
            
        connection.commit()
        return make_response(jsonify(response), status_code)