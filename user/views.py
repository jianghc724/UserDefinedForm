from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from user.models import *

import requests
import json
import html
from datetime import datetime

# Create your views here.
class UserLogin(APIView):
    def get(self):
        pass

    def post(self):
        # to do
        self.check_input('user_id', 'password')
        user = User.objects.get(user=self.input['user_id'])


        raise ValidateError('username or password wrong')