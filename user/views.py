from codex.baseerror import *
from codex.baseview import APIView
from user.models import *

import requests
import json
import html
from datetime import datetime


class UserRegister(APIView):
    def get(self):
        pass

    def post(self):
        self.check_input('user_id', 'password_one', 'password_two', 'license')
        user = User.objects.get(user=self.input['user_id'])
        if user:
            raise InputError('user_id used')
        else:
            if self.input['password_one'] == self.input['password_two']:
                user = User.objects.create(user=self.input['user_id'], password=self.input['passsword_one'], license=self.input['license'])
                user.save()
            else:
                raise LogicError('password are not same')


class UserLogin(APIView):
    def get(self):
        pass

    def post(self):
        self.check_input('user_id', 'password')
        user = User.objects.get(user=self.input['user_id'])
        if user:
            if user.password == self.input['password']:
                # do something
                return

        raise ValidateError('username or password wrong')



