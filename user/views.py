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
                    u_name = User.objects.get(id=form.rater_id).username
                    result.append({
                        'id': form.id,
                        'time': form.finishTime.timestamp(),
                        'rater':u_name,
                    })
                return result
            else:
                forms = Form.objects.filter(rater=user)
                result = []
                for form in forms:
                    u_name = User.objects.get(id=form.rater_id).username
                    result.append({
                        'id': form.id,
                        'time': form.finishTimetimestamp(),
                        'rater': u_name,
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
                if not question.choiceThree == '':
                    choice.append(question.choiceThree)
                if not question.choiceFour == '':
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
                u_name = User.objects.get(id=questionBase.creator_id).username
                print (questionBase.createTime)
                result.append({
                    'id': questionBase.id,
                    'name':questionBase.questionName,
                    'creator': u_name,
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
            self.check_input('name', 'id')
            s = SectionBase.objects.create(name=self.input['name'], creator=self.request.user, createTime=datetime.now())
            i = 0
            for q in self.input['id']:
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
                for question in section.questionBases.all():
                    choice = []
                    choice.append(question.choiceOne)
                    choice.append(question.choiceTwo)
                    if not question.choiceThree == '':
                        choice.append(question.choiceThree)
                    if not question.choiceFour == '':
                        choice.append(question.choiceFour)
                    result.append({
                        'question_id': question.id,
                        'question_type': question.questionType,
                        'question_info': question.questionInfo,
                        'choices': choice,
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
                u_name = User.objects.get(id=sectionBase.creator_id).username
                result.append({
                    'id': sectionBase.id,
                    'name': sectionBase.name,
                    'creator': u_name,
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
                    'name': sectionBase.name,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        if self.request.user.is_authenticated():
            self.check_input('name', 'id')
            f = FormBase.objects.create(name=self.input['name'], creator=self.request.user, createTime=datetime.now())
            i = 0
            for s in self.input['id']:
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
                for section in form.sectionBases.all():
                    _result = []
                    for question in section.questionBases.all():
                        choice = []
                        choice.append(question.choiceOne)
                        choice.append(question.choiceTwo)
                        if not question.choiceThree == '':
                            choice.append(question.choiceThree)
                        if not question.choiceFour == '':
                            choice.append(question.choiceFour)
                        _result.append({
                            'section_id': section.id,
                            'question_id': question.id,
                            'question_type': question.questionType,
                            'question_info': question.questionInfo,
                            'choices': choice,
                        })
                    result.append(_result)
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
                u_name = User.objects.get(id=formBase.creator_id).username
                result.append({
                    'id': formBase.id,
                    'name': formBase.name,
                    'creator': u_name,
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
                u_name = User.objects.get(id=formBase.creator_id).username
                result.append({
                    'id': formBase.id,
                    'name': formBase.name,
                    'creator': u_name,
                    'time':formBase.createTime.timestamp(),
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
                for section in form.sections.all():
                    _result = []
                    for question in section.questions.all():
                        _result.append({
                            'section_id': section.id,
                            'question_id': question.id,
                            'question_info': question.question.questionInfo,
                            'result': question.result,
                        })
                    result.append(_result)
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
            for sBase in fBase.sectionBases.all():
                _result = []
                for qBase in sBase.questionBases.all():
                    choice = []
                    choice.append(qBase.choiceOne)
                    choice.append(qBase.choiceTwo)
                    if not qBase.choiceThree == '':
                        choice.append(qBase.choiceThree)
                    if not qBase.choiceFour == '':
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
            f = Form.objects.create(finishTime=datetime.now(), rater=self.request.user)
            pre_s_id = -1
            pre_q_id = -1
            pre_s = None
            r = ""
            for question in self.input:
                str = question['id']
                res = question['value']
                s_id = int(str.split('_')[0])
                q_id = int(str.split('_')[1])
                if not s_id == pre_s_id:
                    if pre_s is not None:
                        q = Question.objects.create(result=r, question=QuestionBase.objects.get(id=pre_q_id))
                        pre_s.questions.add(q)
                        pre_s.save()
                        f.sections.add(pre_s)
                        r = ""
                        pre_q_id = -1
                    pre_s = Section.objects.create(name=SectionBase.objects.get(id=s_id).name)
                    pre_s_id = s_id
                    pre_q_id = q_id
                    r = res
                else:
                    if not pre_q_id == q_id:
                        q = Question.objects.create(result=r, question=QuestionBase.objects.get(id=pre_q_id))
                        pre_s.questions.add(q)
                        r = res
                        pre_q_id = q_id
                    else:
                        r = r + " | " + res
            q = Question.objects.create(result=r, question=QuestionBase.objects.get(id=pre_q_id))
            pre_s.questions.add(q)
            pre_s.save()
            f.sections.add(pre_s)
            f.save()
        else:
            raise LogicError("You haven't log in")