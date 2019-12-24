import uuid
import re
import random
import string
from app.serializer.extension import db, guard, mail,pusher
from app.component.user.utils import Profil as user_profil
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256, oracle10
from flask import render_template,url_for
from flask_mail import Message
from datetime import datetime

class User(db.Model):
    __table_name__ = 'user',
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(100),unique=True,nullable=False)
    username = db.Column(db.String(100),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    profil = db.Column(db.String(100),unique=False,nullable=False,default='profil.jpg')
    profil_header = db.Column(db.String(100),unique=False,nullable=False,default='profil_header.jpg')
    profil_background = db.Column(db.String(100),unique=False,nullable=False,default='profil_background.jpg')
    gender = db.Column(db.String(100),unique=False,nullable=False)
    country = db.Column(db.String(100),unique=False,nullable=False)
    work = db.Column(db.String(100),unique=False,nullable=False)
    education = db.Column(db.String(100),unique=False,nullable=False)
    answersv1 = db.Column(db.String(100),unique=False,nullable=False)
    answersv2 = db.Column(db.String(100),unique=False,nullable=False)
    check_answersv1 = db.Column(db.String(100),unique=False,nullable=False)
    check_answersv2 = db.Column(db.String(100),unique=False,nullable=False)
    roles = db.Column(db.Text,nullable=True,default='operator')
    password = db.Column(db.String(100),unique=False,nullable=False)
    check_password = db.Column(db.String(100),unique=False,nullable=False)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active
    
    @classmethod
    def filter_public_id(cls,datauser):
        return cls.query.filter_by(public_id=datauser).first()

    @classmethod
    def filter_username(cls,datauser):
        return cls.query.filter_by(username=datauser).first()
    
    @classmethod
    def filter_email(cls,datauser):
        return cls.query.filter_by(email=datauser).first()

    def random_string_for_answer(data=15):
        strings = string.ascii_lowercase
        return ''.join(random.choice(strings) for i in range(data))

    @classmethod
    def create_user(cls,datauser):
        username = cls.filter_email(datauser['username'])
        email = cls.filter_email(datauser['email'])
        if not username and not email:
            Remail = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.search(Remail,datauser['email']):
                public_id = str(uuid.uuid4())
                answersv1 = cls.random_string_for_answer(random.randint(10,15))
                answersv1_hash = generate_password_hash(answersv1,method='pbkdf2:sha256',salt_length=8)
                answersv2 = cls.random_string_for_answer(random.randint(10,16))
                answersv2_hash = pbkdf2_sha256.hash(answersv2)
                Rpassword = r'(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'
                if re.search(Rpassword,datauser['password']):
                    password_hash = guard.hash_password(datauser['password'])
                    if datauser['profil'] != None:
                        profil = user_profil.save_profil(datauser['profil'])
                        create = cls(public_id=public_id,username=datauser['username'],email=datauser['email'],profil=profil,gender=datauser['gender'],country=datauser['country'],
                                    work=datauser['work'],education=datauser['education'],answersv1=answersv1_hash,answersv2=answersv2_hash,check_answersv1=answersv1,
                                    check_answersv2=answersv2,password=password_hash,check_password=datauser['password'])
                        db.session.add(create)
                        db.session.commit()
                        msg = Message('Your data information',sender='kenedynpsyh@gmail.com',recipients=[datauser['email']])
                        msg.html = render_template('register.html',username=datauser['username'],email=datauser['email'],answersv1=answersv1,answersv2=answersv2,password=datauser['password'])
                        mail.send(msg)
                        with open('testing_answer.txt','w') as w:
                            w.write(f'{answersv1},{answersv2}')
                        pusher.trigger('Main-Api-User', 'Create-User', {'message': 'Success Create New User'})
                        return {'message': True}
                    else:
                        create = cls(public_id=public_id,username=datauser['username'],email=datauser['email'],gender=datauser['gender'],country=datauser['country'],
                                    work=datauser['work'],education=datauser['education'],answersv1=answersv1_hash,answersv2=answersv2_hash,check_answersv1=answersv1,
                                    check_answersv2=answersv2,password=password_hash,check_password=datauser['password'])
                        db.session.add(create)
                        db.session.commit()
                        msg = Message('Your data information',sender='kenedynpsyh@gmail.com',recipients=[datauser['email']])
                        msg.html = render_template('register.html',username=datauser['username'],email=datauser['email'],answersv1=answersv1,answersv2=answersv2,password=datauser['password'])
                        mail.send(msg)
                        pusher.trigger('Main-Api-User', 'Create-User', {'message': 'Success Create New User'})
                        return {'message': True}
        return False

    @classmethod
    def access_user(cls,datauser):
        check = cls.filter_email(datauser['email'])
        if check:
            users = guard.authenticate(check.username,datauser['password'])
            ret = {'access_token': guard.encode_jwt_token(users)}
            pusher.trigger('Main-Api-User', 'Access-User', {'message': 'Success Login'})
            return ret
        return False

    @classmethod
    def reset_user(cls,datauser):
        check = cls.filter_email(datauser['email'])
        if check:
            msg = Message('Reset Password',sender='kenedynpsyh@gmail.com',recipients=[check.email])
            msg.html = render_template('reset.html',username=check.username,email=check.email,answersv1=check.check_answersv1,answersv2=check.check_answersv2,password=check.check_password)
            mail.send(msg)
            pusher.trigger('Main-Api-User', 'Reset-User', {'message': 'Success Reset User'})
            return {'message': True}
        return False

    @classmethod
    def put_user(cls,users,token,datauser):
        check = cls.filter_public_id(token)
        if check == users:
            datausers = {}
            if datauser['change_answer'] == 'true':
                if check_password_hash(check.answersv1,datauser['answersv1']) and pbkdf2_sha256.verify(datauser['answersv2'],check.answersv2):
                    if datauser['new_answersv1'] != None and datauser['new_answersv2'] != None:
                        answersv1_hash = generate_password_hash(datauser['new_answersv1'],method='pbkdf2:sha256',salt_length=8)
                        answersv2_hash = pbkdf2_sha256.hash(datauser['new_answersv2'])
                        datausers['answersv1'] = check.answersv1 = answersv1_hash
                        datausers['answersv2'] = check.answersv2 = answersv2_hash
                        datausers['check_answersv1'] = check.check_answersv1 = datauser['new_answersv1']
                        datausers['check_answersv2'] = check.check_answersv2 = datauser['new_answersv2']
                        db.session.commit()
                        pusher.trigger('Main-Api-User', 'Update-User', {'message': 'Success Update User'})
                        return {'message': True}
                    elif datauser['new_answersv1'] != None:
                        answersv1_hash = generate_password_hash(datauser['new_answersv1'],method='pbkdf2:sha256',salt_length=8)
                        datausers['answersv1'] = check.answersv1 = answersv1_hash
                        datausers['check_answersv1'] = check.check_answersv1 = datauser['new_answersv1']
                        db.session.commit()
                        pusher.trigger('Main-Api-User', 'Update-User', {'message': 'Success Update User'})
                        return {'message': True}
                    elif datauser['new_answersv2'] != None:
                        answersv2_hash = pbkdf2_sha256.hash(datauser['new_answersv2'])
                        datausers['answersv2'] = check.answersv2 = answersv2_hash
                        datausers['check_answersv2'] = check.check_answersv2 = datauser['new_answersv2']
                        db.session.commit()
                        pusher.trigger('Main-Api-User', 'Update-User', {'message': 'Success Update User'})
                        return {'message': True}
            elif datauser['change_password'] == 'true':
                if check_password_hash(check.answersv1,datauser['answersv1']) and pbkdf2_sha256.verify(datauser['answersv2'],check.answersv2):
                    if check.check_password == datauser['oldpassword']:
                        Rpassword = r'(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'
                        if re.search(Rpassword,datauser['newpassword']):
                            password_hash = guard.hash_password(datauser['newpassword'])
                            datausers['password'] = check.passowrd = password_hash
                            datausers['check_password'] = check.check_password = datauser['newpassword']
                            db.session.commit()
                            pusher.trigger('Main-Api-User', 'Update-User', {'message': 'Success Update User'})
                            return {'message': True}
            else:
                datausers['username'] = check.username = datauser['username']
                datausers['email'] = check.email = datauser['email']
                if datauser['profil'] != None:
                    datausers['profil'] = check.profil = user_profil.save_profil(datauser['profil'])
                if datauser['profil_header'] != None:
                    datausers['profil_header'] = check.profil_header = user_profil.save_profil(datauser['profil_header'])
                if datauser['profil_background'] != None:
                    datausers['profil_background'] = check.profil_background = user_profil.save_profil(datauser['profil_background'])
                datausers['gender'] = check.gender = datauser['gender']
                datausers['country'] = check.country = datauser['country']
                datausers['work'] = check.work = datauser['work']
                datausers['education'] = check.education = datauser['education']
                db.session.commit()
                pusher.trigger('Main-Api-User', 'Update-User', {'message': 'Success Update User'})
                return {'message': True}
        return False

    @classmethod
    def delete_user(cls,datauser):
        check = cls.filter_public_id(datauser)
        if check:
            db.session.delete(check)
            db.session.commit()
            pusher.trigger('Main-Api-User', 'Delete-User', {'message': 'Success Delete User'})
            return {'message': True}
        return False

    @classmethod
    def get_data_user(cls,token):
        check = cls.filter_public_id(token)
        if check:
            datauser = {}
            datauser['username'] = check.username
            if check.profil:
                datauser['profil'] = url_for('static',filename='profil/' + check.profil)
            if check.profil_header:
                datauser['profil_header'] = url_for('static',filename='profil/' + check.profil_header)
            if check.profil_background:
                datauser['profil_background'] = url_for('static',filename='profil/' + check.profil_background)
            datauser['gender'] = check.gender
            datauser['country'] = check.country
            datauser['work'] = check.work
            datauser['education'] = check.education
            pusher.trigger('Main-Api-User', 'Access-User', {'message': 'Success Access User'})
            return {'access_user':datauser}
        return False









