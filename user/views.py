from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from user.models import *
from django.contrib.auth import authenticate,login,logout

import requests
import json
import html
from datetime import datetime

# Create your views here.


class UserLogin(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            return
        else:
            raise LogicError("")

    def post(self):
        self.check_input('user_id', 'password')
        user = authenticate(username=self.input['user_id'], password=self.input['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return
        raise ValidateError('username or password wrong')


class ApplyList(APIView):
    def get(self):
        pass

    def post(self):
        pass


class CreateQuestion(APIView):
    def get(self):
        pass

    def post(self):
        pass


class CreateSection(APIView):
    def get(self):
        pass

    def post(self):
        pass


class CreateForm(APIView):
    def get(self):
        pass

    def post(self):
        pass


class HandleApply(APIView):
    def get(self):
        pass

    def post(self):
        pass
