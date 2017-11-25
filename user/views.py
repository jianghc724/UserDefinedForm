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


class FormList(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            user = self.request.user
            if user.is_superuser:
                forms = Form.objects.all()
                result = []
                for form in forms:
                    result.append({
                        'status': form.formFinished,
                        'id': form.id,
                        'time': form.finishTime,
                        'rater': form.rater.user.username
                    })
                return result
            else:
                forms = Form.objects.filter(rater=user)
                result = []
                for form in forms:
                    result.append({
                        'status': form.formFinished,
                        'id': form.id,
                        'time': form.finishTime,
                        'rater': form.rater.user.username
                    })
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateQuestion(APIView):
    def get(self):
        pass

    def post(self):
        if self.request.user.is_authenticated():
            self.check_input('type', 'info', 'name')
            if self.input['type'] == 'single' or self.input['type'] == 'multiple':
                self.check_input('choiceOne', 'choiceTwo', 'choiceThree', 'choiceFour')
            if self.input['type'] == 'single':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=1, questionInfo=self.input['info'], createTime = datetime.now(), creator = self.request.user, choiceOne = self.input['choiceOne'], choiceTwo = self.input['choiceTwo'], choiceThree = self.input['choiceThree'], choiceFour = self.input['choiceFour'])
            elif self.input['type'] == 'multiple':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=2, questionInfo=self.input['info'], createTime = datetime.now(), creator = self.request.user, choiceOne = self.input['choiceOne'], choiceTwo = self.input['choiceTwo'], choiceThree = self.input['choiceThree'], choiceFour = self.input['choiceFour'])
            elif self.input['type'] == 'textfilling':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=3, questionInfo=self.input['info'], createTime = datetime.now(), creator = self.request.user)
            else:
                raise InputError("No such type")
            q.save()
        else:
            raise LogicError("You have no authority to access")


class CheckQuestionBase(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            question = QuestionBase.objects.get(id=self.input['id'])
            if question:
                choice = []
                choice.append(question.choiceOne)
                choice.append(question.choiceTwo)
                choice.append(question.choiceThree)
                choice.append(question.choiceFour)
                result = {
                    'question_type': question.questionType,
                    'question_info': question.questionInfo,
                    'choices': choice,
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
        if self.request.user.is_authenticated():
            questionBases = QuestionBase.objects.all()
            result = []
            for questionBase in questionBases:
                # bug to fix: creator
                print (questionBase.createTime)
                result.append({
                    'id': questionBase.id,
                    'name':questionBase.questionName,
                    'creator': questionBase.creator_id,
                    'time':questionBase.createTime.timestamp(),
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CreateSection(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            questionBases = QuestionBase.objects.all()
            result = []
            for questionBase in questionBases:
                result.append({
                    'id': questionBase.id,
                    'name': questionBase.questionName,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        if self.request.user.is_authenticated():
            s = SectionBase.objects.create(creator=self.request.user, createTime=datetime.now())
            i = 0
            for q in self.input:
                s.questionBases.add(QuestionBase.objects.get(id=q))
                i = i + 1
            s.questionCount = i
            s.save()
        else:
            raise LogicError("You have no authority to access")


class CheckSectionBase(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            section = SectionBase.objects.get(id=self.input['id'])
            if section:
                result = []
                for question in section.questions:
                    result.append({
                        'question_type': question.questionType,
                        'question_info': question.questionInfo,
                        'choice_number': question.choiceCount,
                        'choice_one': question.choiceOne,
                        'choice_two': question.choiceTwo,
                        'choice_three': question.choiceThree,
                        'choice_four': question.choiceFour,
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
        if self.request.user.is_authenticated():
            sectionBases = SectionBase.objects.all()
            result = []
            for sectionBase in sectionBases:
                result.append({
                    'id': sectionBase.id,
                    'creator': sectionBase.creator_id,
                    'time':sectionBase.createTime.timestamp(),
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class CreateForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            sectionBases = SectionBase.objects.all()
            result = []
            for sectionBase in sectionBases:
                result.append({
                    'id': sectionBase.id,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        if self.request.user.is_authenticated():
            f = FormBase.objects.create(creator=self.request.user, createTime=datetime.now())
            i = 0
            for s in self.input:
                f.sectionBases.add(SectionBase.objects.get(id=s))
                i = i + 1
            f.sectionCount = i
            f.save()
        else:
            raise LogicError("You have no authority to access")


class CheckFormBase(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            form = FormBase.objects.get(id=self.input['id'])
            if form:
                result = []
                for section in form.sections:
                    for question in section.questions:
                        result.append({
                            'question_type': question.questionType,
                            'question_info': question.questionInfo,
                            'choice_number': question.choiceCount,
                            'choice_one': question.choiceOne,
                            'choice_two': question.choiceTwo,
                            'choice_three': question.choiceThree,
                            'choice_four': question.choiceFour,
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
        if self.request.user.is_authenticated():
            formBases = FormBase.objects.all()
            result = []
            for formBase in formBases:
                result.append({
                    'id': formBase.id,
                    'creator': formBase.creator_id,
                    'time':formBase.createTime.timestamp(),
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        pass


class HandleApply(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            formBases = FormBase.objects.all()
            result = []
            for formBase in formBases:
                result.append({
                    'id': formBase.id,
                    'creator': formBase.creator.user.username,
                    'create_time': formBase.createTime,
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
                result = []
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


class FinishForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            fBase = FormBase.objects.get(id=self.input['id'])
            result = []
            for sBase in fBase.sectionBases:
                _result = []
                for qBase in sBase.questionBases:
                    choice = []
                    for i in range(0,qBase.choiceCount):
                        if i == 0:
                            choice.append(qBase.choiceOne)
                        elif i == 1:
                            choice.append(qBase.choiceTwo)
                        elif i == 2:
                            choice.append(qBase.choiceThree)
                        elif i == 3:
                            choice.append(qBase.choiceFour)
                    _result.append({
                        'section_id': sBase.id,
                        'question_id': qBase.id,
                        'question_type': qBase.questionType,
                        'question_info': qBase.questionInfo,
                        'choices': choice,
                    })
                result.append(_result)
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            pass
        else:
            raise LogicError("You haven't log in")