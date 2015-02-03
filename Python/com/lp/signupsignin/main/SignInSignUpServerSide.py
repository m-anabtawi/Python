__author__ = 'manarPC'

from bottle import run, post, request, error, get
import psycopg2
from psycopg2._json import Json
import json
import os

conn_string = "host='localhost' dbname='ASAL_AUD' user='postgres' password='123'"


@error(404)
def error404(error):
    json_response = '{"response":"Page not found"}'
    response = json.loads(json_response)
    return response['response']


@post('/login')
def sign_in():
    data = request.body.read()
    if not data:
      json_response='{"error":"No Data","responseMessage":"No Data"}'
      response = json.loads(json_response)
      return response
    entity = json.loads(data)
    if entity.has_key('email') & entity.has_key('password'):
        email=entity['email']
        password=entity['password']
        if not email:
               json_response='{"error":"You must enter email","responseMessage":"You must enter email"}'
               response = json.loads(json_response)
               return response
        elif not password:
               json_response='{"error":"You must enter password","responseMessage":"You must enter password"}'
               response = json.loads(json_response)
               return response
        else:
                conn = psycopg2.connect(conn_string)
                cursor = conn.cursor()
                cursor.execute("SELECT data->>'image' FROM users WHERE data->>'email'= (%s) AND data->>'password'=(%s)", (email, password))
                for row in cursor:
                    if row[0]:
                        json_response='{"success":1,"responseMessage":"Success", "path":"'+row[0]+'"}'
                        response = json.loads(json_response)
                        cursor.close()
                        del cursor
                        conn.close()
                        return response
                cursor.close()
                del cursor
                conn.close()
                json_response='{"error":"Incorrect Email or Password","responseMessage":"Incorrect Email or Password"}'
                response = json.loads(json_response)
                return response


@post('/register')
def sign_up():
    data = request.body.read()
    if not data:
       json_response='{"error":"No Data","responseMessage":"No Data"}'
       response = json.loads(json_response)
       return response
    entity = json.loads(data)
    if entity.has_key('email') & entity.has_key('password') & entity.has_key('name') & entity.has_key('image'):
           email=entity['email']
           password=entity['password']
           userName=entity['name']
           userImage=entity['image']
           if not userName:
               json_response='{"error":"You must enter userName","responseMessage":"You must enter userName"}'
               response = json.loads(json_response)
               return response
           elif not email:
               json_response='{"error":"You must enter email","responseMessage":"You must enter email"}'
               response = json.loads(json_response)
               return response
           elif not password:
               json_response='{"error":"You must enter password","responseMessage":"You must enter password"}'
               response = json.loads(json_response)
               return response
           elif not userImage:
               json_response='{"error":"You must choose an image ","responseMessage":"You must pick image"}'
               response = json.loads(json_response)
               return response
           else:
               conn = psycopg2.connect(conn_string)
               cursor = conn.cursor()
               cursor.execute("SELECT exists (SELECT 1 FROM users WHERE data->>'email'=(%s) LIMIT 1)",(email,))
               for row in cursor:
                    if row[0]:
                        json_response='{"error":"Email Registered","responseMessage":"Email Registered"}'
                        response = json.loads(json_response)
                        cursor.close()
                        del cursor
                        conn.close()
                        return response
                    else:
                        cursor.execute("INSERT INTO users (data) VALUES (%s)", [Json({'password': password, 'name': userName, 'email': email, 'image':userImage })])
                        conn.commit()
                        cursor.execute("SELECT id FROM users WHERE data->>'email'= (%s) AND data->>'password'=(%s)", (email, password))
                        for row in cursor:
                            if row[0]:
                                id = row [0]
                                directory='C:/Users/manarPC/PycharmProjects/LPSearch/images/'+str(id)
                                if not os.path.exists(directory):
                                   os.makedirs(directory)
                        cursor.close()
                        del cursor
                        conn.close()
                        json_response='{"success":1,"responseMessage":"Success"}'
                        response = json.loads(json_response)
                        return response


@post('/upload')
def upload():
    email=request.get_header('email')
    imagefile=request.files['fileupload']
    image = imagefile.file.read()
    imageName = imagefile.filename
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE data->>'email'= (%s)", (email,))
    for row in cursor:
      if row[0]:
         img = open('C:/Users/manarPC/PycharmProjects/LPSearch/images/'+str(row[0])+'/'+imageName, 'wb')
         img.write(image)
    json_response = '{"success":1,"responseMessage":"Success"}'
    response = json.loads(json_response)
    cursor.close()
    del cursor
    conn.close()
    return response


run(host='10.10.10.52', port=7777, debug=True, reloader=True)


