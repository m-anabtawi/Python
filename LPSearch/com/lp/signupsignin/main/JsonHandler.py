__author__ = 'manarPC'

import json

class JsonHandler:

    email = 'email'
    password = 'password'
    name = 'name'
    image = 'image'
    directory = 'C:/Users/manarPC/PycharmProjects/LPSearch/images/'
    id = 'id'
    fileupload = 'fileupload'

    def NoData(self):
      json_response='{"error":"No Data","responseMessage":"No Data"}'
      response = json.loads(json_response)
      return response

    def Error(self):
      json_response = '{"response":"Page not found"}'
      response = json.loads(json_response)
      return response['response']

    def NoEmail(self):
       json_response = '{"error":"You must enter email","responseMessage":"You must enter email"}'
       response = json.loads(json_response)
       return response

    def NoPassword(self):
        json_response = '{"error":"You must enter password","responseMessage":"You must enter password"}'
        response = json.loads(json_response)
        return response

    def NoUserName(self):
        json_response = '{"error":"You must enter userName","responseMessage":"You must enter userName"}'
        response = json.loads(json_response)
        return response

    def NoImage(self):
        json_response = '{"error":"You must choose an image ","responseMessage":"You must pick image"}'
        response = json.loads(json_response)
        return response

    def SuccessLogin(self, path):
        json_response = '{"success":1,"responseMessage":"Success", "path":"'+path+'"}'
        response = json.loads(json_response)
        return response

    def ErrorLogin(self):
        json_response='{"error":"Incorrect Email or Password","responseMessage":"Incorrect Email or Password"}'
        response = json.loads(json_response)
        return response

    def ErrorRegister(self):
        json_response = '{"error":"Email Registered","responseMessage":"Email Registered"}'
        response = json.loads(json_response)
        return response

    def ErrorInRegister(self):
        json_response = '{"error":"Can not be registered","responseMessage":"Can not be registered"}'
        response = json.loads(json_response)
        return response

    def SuccessRegister(self, id):
        json_response = '{"success":1,"responseMessage":"Success","id":'+str(id)+'}'
        response = json.loads(json_response)
        return response

    def SuccessUpload(self):
        json_response = '{"success":1,"responseMessage":"Success"}'
        response = json.loads(json_response)
        return response

    def URL(self):
        # json_response = '{"url": ["http://pin2me.comyr.com/upload/image/IMG-20140925-WA0000.jpg.jpg", "http://pin2me.comyr.com/upload/image/100PINT.jpg", "http://pin2me.comyr.com/upload/image/IMG-20140925-WA0000.jpg.jpg"]}'
        # response= json.loads(json_response)
        json_response = '{"url":"http://pin2me.comyr.com/upload/image/IMG-20140925-WA0000.jpg.jpg,http://pin2me.comyr.com/upload/image/100PINT.jpg,http://pin2me.comyr.com/upload/image/100PINT.jpg,http://pin2me.comyr.com/upload/image/100PINT.jpg,http://pin2me.comyr.com/upload/image/100PINT.jpg,http://pin2me.comyr.com/upload/image/IMG-20140925-WA0000.jpg.jpg"}'
        response = json.loads(json_response)
        return response





