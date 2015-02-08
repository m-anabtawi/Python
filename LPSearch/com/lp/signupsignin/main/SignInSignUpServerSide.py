from psycopg2._json import Json

__author__ = 'manarPC'

from bottle import run, post, request, error
import json
import os
import DataBaseQuery
import JsonHandler

dbq = DataBaseQuery.DataBaseQuery()
jh = JsonHandler.JsonHandler()

@error(404)
def error404(error):
    return jh.Error()


@post('/login')
def sign_in():
    data = request.body.read()
    if not data:
      return jh.NoData()
    entity = json.loads(data)
    if entity.has_key(jh.email) & entity.has_key(jh.password):
        email=entity[jh.email]
        password=entity[jh.password]
        if not email:
               return jh.NoEmail()
        elif not password:
               return jh.NoPassword()
        else:
                connection = dbq.connection
                cursor = dbq.SelectImage(email, password)
                for row in cursor:
                    if row[0]:
                        cursor.close()
                        del cursor
                        connection.close()
                        return jh.SuccessLogin(row[0])
                return jh.ErrorLogin()


@post('/register')
def sign_up():
    data = request.body.read()
    if not data:
       return jh.NoData()
    entity = json.loads(data)
    if entity.has_key(jh.email) & entity.has_key(jh.password) & entity.has_key(jh.name) & entity.has_key(jh.image):
           email = entity[jh.email]
           password = entity[jh.password]
           userName = entity[jh.name]
           userImage = entity[jh.image]
           if not userName:
               return jh.NoUserName()
           elif not email:
               return jh.NoEmail()
           elif not password:
               return jh.NoPassword()
           elif not userImage:
               return jh.NoImage()
           else:
               connection = dbq.connection
               cursor = dbq.cursor
               for row in dbq.SelectUser(email):
                    if row[0]:
                        return jh.ErrorRegister()
                    else:
                        #dbq.InsertUser(password, userName, email, userImage)
                        cursor.execute("INSERT INTO users (data) VALUES (%s)", [Json({'password': password, 'name': userName, 'email': email, 'image':userImage })])
                        connection.commit()
                        cursor = dbq.SelectUserId(email, password)
                        for row in dbq.SelectUserId(email, password):
                            if row[0]:
                                id = row[0]
                                directory = jh.directory+str(id)
                                if not os.path.exists(directory):
                                   os.makedirs(directory)
                            cursor.close()
                            del cursor
                            connection.close()
                            return jh.SuccessRegister(id)
                        else:
                            return jh.ErrorInRegister()




@post('/upload')
def upload():
    id = request.get_header(jh.id)
    imagefile = request.files[jh.fileupload]
    image = imagefile.file.read()
    imageName = imagefile.filename
    img = open(jh.directory+str(id)+'/'+imageName, 'wb')
    img.write(image)
    return jh.SuccessUpload()


@post('/getImage')
def getImage():
    return jh.URL()

run(host='172.16.228.137', port=7777, debug=True, reloader=True)


