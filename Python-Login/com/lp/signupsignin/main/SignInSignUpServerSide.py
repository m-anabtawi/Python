import urllib2


__author__ = 'manarPC'

from bottle import run, post, request, error, get
import json
import os
import DataBaseQuery
import JsonHandler
import urllib
from psycopg2._json import Json
from bottle import static_file
from gcm import *

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
                cursor = dbq.SelectImage(email, password)
                for row in cursor:
                    if row[0]:
                        cursor.close()
                        del cursor
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


@post('/getImageName')
def getImage():
    names = os.listdir('C:\Users\manarPC\PycharmProjects\LPSearch\images\explore')
    n = ''
    for name in names:
       n += name + ','
    json_response = '{"url":"'+n+'"}'
    response = json.loads(json_response)
    return response



@get('/getImage/<filename>')
def send_image(filename):
    return static_file(filename, root='C:\\Users\\manarPC\\PycharmProjects\\LPSearch\\images\\explore', mimetype='image/png')
#
@get('/GCM')
def GCM():
    file = open('newfile.txt','r')
    regId = file.read()
    json_data = {"registration_ids": [regId],}
    url ="https://android.googleapis.com/gcm/send"
    apiKey ="AIzaSyCs3E0Fb8pIbSuLsBLL6brr3qU6V-CR9bw"
    myKey ="key=" + apiKey
    message = json.dumps(json_data)
    headers ={'Content-Type': 'application/json', 'Authorization': myKey}
    req = urllib2.Request(url,message,headers)
    f = urllib2.urlopen(req)
    response = json.loads(f.read())
    return response


#register android device id on the server
@post('/gcmRegKey')
def gcmRegKey():
    data = request.body.read()
    entity = json.loads(data)
    regId= entity['regid']
    file = open("newfile.txt", "w")
    file.write(regId)
    file.close()


@post('/download')
def getImage():
    urls = jh.URL()
    listPath = ['']
    urlPath = urls['url']
    image = urlPath.split(',')
    for url in image:
     imageName = url.rsplit('/', 1)[1]
     path = jh.directory+"image/"+imageName
     listPath.append(path)
     urllib.urlretrieve(url, path)

run(host='192.168.1.102', port=7777, debug=True, reloader=True)


