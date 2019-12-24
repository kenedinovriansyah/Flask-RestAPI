import os
import json
import string
import random
from io import BytesIO
from flask_testing import TestCase
from app import Servers
from app.database.models import User
from app.serializer.extension import guard

app = Servers.create_app()


def random_code(length=20):
    strings = string.ascii_uppercase
    return ''.join(random.choice(strings) for i in range(length))


class TestUser(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def testing_user(self):
        with self.app.test_client() as client:
            create = {'username':'models','email':'lymad@yahoo.com','gender':'Male','country':'Indonesia','work':'Programmer','education':'University','password':'Password@123'}
            create_user = client.post('/api/access/user/register',data=create,content_type='multipart/form-data',follow_redirects=True)
            data = json.loads(create_user.data.decode())
            self.assertTrue(data['message'] == True)
            self.assertTrue(create_user.content_type == 'application/json')
            self.assertEqual(create_user.status_code,200)
            self.assertIn(b'message',create_user.data)


            create1 = {'username':'hello_worlds','email':'putri@gmail.com','gender':'Male','country':'Indonesia','work':'Programmer','education':'University','password':'Password@123'}
            create1 = {key: str(value) for key, value in create1.items()}
            create1['profil'] = (BytesIO(b'avddqwdqw'),'testing.jpg')
            create_user1 = client.post('/api/access/user/register',data=create1,content_type='multipart/form-data',follow_redirects=True)
            data = json.loads(create_user1.data.decode())
            self.assertTrue(data['message'] == True)
            self.assertTrue(create_user1.content_type == 'application/json')
            self.assertEqual(create_user1.status_code,200)
            self.assertIn(b'message',create_user1.data)

            access_user = client.post('/api/access/user',data=json.dumps({'email':'lymad@yahoo.com','password':'Password@123'}),content_type='application/json',follow_redirects=True)
            data = json.loads(access_user.data.decode())
            self.assertTrue(data['access_token'])
            self.assertTrue(access_user.content_type == 'application/json')
            self.assertEqual(access_user.status_code,200)
            self.assertIn(b'access_token',access_user.data)

            reset_user = client.post('/api/access/uset/reset',data=json.dumps({'email':'lymad@yahoo.com'}),content_type='application/json',follow_redirects=True)
            data = json.loads(reset_user.data.decode())
            self.assertTrue(data['message'] == True)
            self.assertTrue(reset_user.content_type == 'application/json')
            self.assertEqual(reset_user.status_code,200)
            self.assertIn(b'message',reset_user.data)

            data_user_text = User.query.filter_by(email="lymad@yahoo.com").first()
            data_update_user_text = {'username':'powerrange','email':'lymad@yahoo.com','gender':'powerrange','country':'powerrange','work':'powerrange','education':'powerrange'}
            update_user_text = client.put('/api/access/user/'+data_user_text.public_id,data=data_update_user_text,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='multipart/form-data',follow_redirects=True)  
            self.assertTrue(update_user_text.content_type == 'application/json')
            self.assertEqual(update_user_text.status_code,200)
            self.assertIn(b'message',update_user_text.data)

            data_user_image = User.query.filter_by(email="lymad@yahoo.com").first()
            data_update_user_image = {'username':'powerrange','email':'lymad@yahoo.com','gender':'powerrange','country':'powerrange','work':'powerrange','education':'powerrange'}
            data_update_user_image = {key:str(value) for key, value in data_update_user_image.items()}
            data_update_user_image['profil'] = (BytesIO(b'dwqdqw'),'testing.jpg')
            data_update_user_image['profil_header'] = (BytesIO(b'dqwdwq'),'testing.jpg')
            data_update_user_image['profil_background'] = (BytesIO(b'dqwdwqdqw'),'testing.jpeg')
            update_user_image = client.put('/api/access/user/'+data_user_image.public_id,data=data_update_user_image,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='multipart/form-data',follow_redirects=True)  
            self.assertTrue(update_user_image.content_type == 'application/json')
            self.assertEqual(update_user_image.status_code,200)
            self.assertIn(b'message',update_user_image.data)
    
            # if os.path.isfile('testing_answer.txt'):
            #     with open('testing_answer.txt','r') as f:
            #         d = f.read().split(',')
            #         answersv1 = d[0]
            #         answersv2 = d[1]
            data_user_answer = User.query.filter_by(email="lymad@yahoo.com").first()
            data_update_user_answer = {'change_answer':'true','answersv1':data_user_answer.check_answersv1,'answersv2':data_user_answer.check_answersv2,'new_answersv1':'hello'}
            update_user_answer = client.put('/api/access/user/'+data_user_answer.public_id,data=data_update_user_answer,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='multipart/form-data',follow_redirects=True)  
            self.assertTrue(update_user_answer.content_type == 'application/json')
            self.assertEqual(update_user_answer.status_code,200)
            self.assertIn(b'message',update_user_answer.data)

            data_user_answer1 = User.query.filter_by(email="lymad@yahoo.com").first()
            data_update_user_answer1 = {'change_answer':'true','answersv1':data_user_answer1.check_answersv1,'answersv2':data_user_answer1.check_answersv2,'new_answersv1':'Worlds'}
            update_user_answer1 = client.put('/api/access/user/'+data_user_answer.public_id,data=data_update_user_answer1,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='multipart/form-data',follow_redirects=True)  
            self.assertTrue(update_user_answer1.content_type == 'application/json')
            self.assertEqual(update_user_answer1.status_code,200)
            self.assertIn(b'message',update_user_answer1.data)

            data_user_answer2 = User.query.filter_by(email="lymad@yahoo.com").first()
            data_update_user_answer2 = {'change_answer':'true','answersv1':data_user_answer2.check_answersv1,'answersv2':data_user_answer2.check_answersv2,'new_answersv2':'MSKMSKQMK'}
            update_user_answer2 = client.put('/api/access/user/'+data_user_answer.public_id,data=data_update_user_answer2,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='multipart/form-data',follow_redirects=True)  
            self.assertTrue(update_user_answer2.content_type == 'application/json')
            self.assertEqual(update_user_answer2.status_code,200)
            self.assertIn(b'message',update_user_answer2.data)

            data_user_password = User.query.filter_by(email="lymad@yahoo.com").first()
            data_update_user_password = {'change_password':'true','answersv1':data_user_password.check_answersv1,'answersv2':data_user_password.check_answersv2,'oldpassword':'Password@123','newpassword':'Kenedi@1234'}
            update_user_password = client.put('/api/access/user/'+data_user_password.public_id,data=data_update_user_password,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='multipart/form-data',follow_redirects=True)  
            self.assertTrue(update_user_password.content_type == 'application/json')
            self.assertEqual(update_user_password.status_code,200)
            self.assertIn(b'message',update_user_password.data)

            data_user_delete = User.query.filter_by(email='putri@gmail.com').first()
            delete_user = client.delete('/api/access/user/'+data_user_delete.public_id,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='application/json',follow_redirects=True)
            data = json.loads(delete_user.data.decode())
            self.assertTrue(data['message'] == True)
            self.assertTrue(delete_user.content_type == 'application/json')
            self.assertEqual(delete_user.status_code,200)
            self.assertIn(b'message',delete_user.data)

            data_access_user_id = User.query.filter_by(email='lymad@yahoo.com').first()
            access_user_id = client.get('/api/access/user/'+data_access_user_id.public_id,headers=dict(authorization='Bearer'+json.loads(access_user.data.decode())['access_token']),content_type='application/json',follow_redirects=True)
            data = json.loads(access_user_id.data.decode())
            self.assertTrue(data['access_user'])
            self.assertTrue(access_user_id.content_type == 'application/json')
            self.assertEqual(access_user_id.status_code,200)
            self.assertIn(b'access_user',access_user_id.data)


