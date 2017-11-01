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


class UserLogout(APIView):
    def get(self):
        pass

    def post(self):
        if self.request.user.is_authenticated():
            logout(self.request)
        else:
            raise LogicError("You haven't log in")


class ApplyList(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            user = self.request.user
            if user.is_superuser:
                applies = Apply.objects.all()
                result = {}
                for apply in applies:
                    result.append({
                        'status': apply.isHandled,
                        'id': apply.id,
                        'time':apply.applyTime,
                    })
                return result
            else:
                applies = Apply.objects.filter(trainee=user)
                result = {}
                for apply in applies:
                    result.append({
                        'status': apply.isHandled,
                        'id': apply.id,
                        'time':apply.applyTime,
                    })
                return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateQuestion(APIView):
    def get(self):
        pass

    def post(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            pass
        else:
            raise LogicError("You have no authority to access")


class CheckQuestionBase(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            self.check_input('id')
            question = QuestionBase.objects.get(id=self.input['id'])
            if question:
                result = {
                    'question_type': question.question.questionType,
                    'question_info': question.question.questionInfo,
                    'choice_number': question.question.choiceCount,
                    'choice_one': question.question.choiceOne,
                    'choice_two': question.question.choiceTwo,
                    'choice_three': question.question.choiceThree,
                    'choice_four': question.question.choiceFour,
                }
                return result
            else:
                raise LogicError('No such question base')
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class QuestionBaseList(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            questionBases = QuestionBase.objects.all()
            result = {}
            for questionBase in questionBases:
                result.append({
                    'id': questionBase.id,
                    'creator': questionBase.creator.username,
                    'create_time':questionBase.createTime,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CreateSection(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            pass
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CheckSectionBase(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            self.check_input('id')
            section = SectionBase.objects.get(id=self.input['id'])
            if section:
                result = {}
                for question in section.questions:
                    result.append({
                        'question_type': question.question.questionType,
                        'question_info': question.question.questionInfo,
                        'choice_number': question.question.choiceCount,
                        'choice_one': question.question.choiceOne,
                        'choice_two': question.question.choiceTwo,
                        'choice_three': question.question.choiceThree,
                        'choice_four': question.question.choiceFour,
                    })
                return result
            else:
                raise LogicError('No such section base')
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class SectionBaseList(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            sectionBases = SectionBase.objects.all()
            result = {}
            for sectionBase in sectionBases:
                result.append({
                    'id': sectionBase.id,
                    'creator': sectionBase.creator.username,
                    'create_time':sectionBase.createTime,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CreateForm(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            pass
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CheckFormBase(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            self.check_input('id')
            form = FormBase.objects.get(id=self.input['id'])
            if form:
                result = {}
                for section in form.sections:
                    for question in section.questions:
                        result.append({
                            'question_type': question.question.questionType,
                            'question_info': question.question.questionInfo,
                            'choice_number': question.question.choiceCount,
                            'choice_one': question.question.choiceOne,
                            'choice_two': question.question.choiceTwo,
                            'choice_three': question.question.choiceThree,
                            'choice_four': question.question.choiceFour,
                        })
                return result
            else:
                raise LogicError('No such form base')
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class FormBaseList(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            formBases = FormBase.objects.all()
            result = {}
            for formBase in formBases:
                result.append({
                    'id': formBase.id,
                    'creator': formBase.creator.username,
                    'create_time':formBase.createTime,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class HandleApply(APIView):
    def get(self):
        if self.request.user.is_authenticated() and self.request.user.is_superuser():
            formBases = FormBase.objects.all()
            result = {}
            for formBase in formBases:
                result.append({
                    'id': formBase.id,
                    'creator': formBase.creator.username,
                    'create_time':formBase.createTime,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CheckForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            form = Form.objects.get(id=self.input['id'])
            if form:
                result = {}
                for section in form.sections:
                    for question in section.questions:
                        result.append({
                            'question_type': question.question.questionType,
                            'question_info': question.question.questionInfo,
                            'result': question.result,
                            'choice_number': question.question.choiceCount,
                            'choice_one': question.question.choiceOne,
                            'is_choice_one': question.isChoiceOne,
                            'choice_two': question.question.choiceTwo,
                            'is_choice_two': question.isChoiceTwo,
                            'choice_three': question.question.choiceThree,
                            'is_choice_three': question.isChoiceThree,
                            'choice_four': question.question.choiceFour,
                            'is_choice_four': question.isChoiceFour,
                        })
                return result
            else:
                raise LogicError("No such Form")
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass
