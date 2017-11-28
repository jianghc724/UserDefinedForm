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
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=1,
                                                questionInfo=self.input['info'], createTime=datetime.now(),
                                                creator=self.request.user, choiceOne=self.input['choiceOne'],
                                                choiceTwo=self.input['choiceTwo'],
                                                choiceThree=self.input['choiceThree'],
                                                choiceFour=self.input['choiceFour'])
            elif self.input['type'] == 'multiple':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=2,
                                                questionInfo=self.input['info'], createTime=datetime.now(),
                                                creator=self.request.user, choiceOne=self.input['choiceOne'],
                                                choiceTwo=self.input['choiceTwo'],
                                                choiceThree=self.input['choiceThree'],
                                                choiceFour=self.input['choiceFour'])
            elif self.input['type'] == 'textfilling':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=3,
                                                questionInfo=self.input['info'], createTime=datetime.now(),
                                                creator=self.request.user)
            elif self.input['type'] == 'rating':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=4,
                                                questionInfo=self.input['info'], createTime=datetime.now(),
                                                creator=self.request.user)
            elif self.input['type'] == 'timing':
                q = QuestionBase.objects.create(questionName=self.input['name'], questionType=5,
                                                questionInfo=self.input['info'], createTime=datetime.now(),
                                                creator=self.request.user)
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
                # print(questionBase.createTime)
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
            st = ''
            for q in self.input['id']:
                st = st + str(q) + ','
                i = i + 1
            s.questionCount = i
            s.questionBases = st
            s.save()
        else:
            raise LogicError("You have no authority to access")


class ModifySection(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            sectionBase = SectionBase.objects.get(id=self.input['id'])
            st = sectionBase.questionBases
            q_list = st.split(',')
            questionBases = QuestionBase.objects.all()
            result = []
            for questionBase in questionBases:
                menuIndex = -1
                i = 0
                flag = False
                for q in q_list:
                    i = i + 1
                    if q == '':
                        continue
                    if int(q) == questionBase.id:
                        menuIndex = i
                        break
                result.append({
                    'id': questionBase.id,
                    'menuIndex': menuIndex,
                    'name': questionBase.questionName,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        if self.request.user.is_authenticated():
            self.check_input('id', 'name', 'ids')
            s = SectionBase.objects.get(id=self.input['id'])
            i = 0
            st = ''
            for q in self.input['ids']:
                st = st + str(q) + ','
                i = i + 1
            s.questionCount = i
            s.questionBases = st
            s.createTime = datetime.now()
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
                st = section.questionBases
                int_list = st.split(',')
                for s in int_list:
                    if s == '':
                        continue
                    question = QuestionBase.objects.get(id=int(s))
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
            st = ''
            for s in self.input['id']:
                st = st + str(s) + ','
                i = i + 1
            f.sectionBases = st
            f.sectionCount = i
            f.save()
        else:
            raise LogicError("You have no authority to access")


class ModifyForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            formBase = FormBase.objects.get(id=self.input['id'])
            st = formBase.sectionBases
            s_list = st.split(',')
            # print(s_list)
            sectionBases = SectionBase.objects.all()
            result = []
            for sectionBase in sectionBases:
                menuIndex = -1
                i = 0
                flag = False
                for s in s_list:
                    i = i + 1
                    if s == '':
                        continue
                    if int(s) == sectionBase.id:
                        # print(int(s))
                        menuIndex = i
                        break
                result.append({
                    'id': sectionBase.id,
                    'menuIndex': menuIndex,
                    'name': sectionBase.name,
                })
            return result
        else:
            raise LogicError("You have no authority to access")

    def post(self):
        if self.request.user.is_authenticated():
            self.check_input('id', 'name', 'ids')
            f = FormBase.objects.get(id=self.input['id'])
            i = 0
            st = ''
            for s in self.input['ids']:
                st = st + str(s) + ','
                i = i + 1
            f.sectionBases = st
            f.sectionCount = i
            f.createTime = datetime.now()
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
                s_st = form.sectionBases
                s_list = s_st.split(',')
                for _section in s_list:
                    if _section == '':
                        continue
                    section = SectionBase.objects.get(id=int(_section))
                    _result = []
                    q_st = section.questionBases
                    q_list = q_st.split(',')
                    for _question in q_list:
                        if _question == '':
                            continue
                        question = QuestionBase.objects.get(id=int(_question))
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
                s_st = form.sections
                s_list = s_st.split(',')
                for _section in s_list:
                    if _section == '':
                        continue
                    section = Section.objects.get(id=int(_section))
                    _result = []
                    q_st = section.questions
                    q_list = q_st.split(',')
                    for _question in q_list:
                        if _question == '':
                            continue
                        question = Question.objects.get(id=int(_question))
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
            s_st = fBase.sectionBases
            s_list = s_st.split(',')
            for _section in s_list:
                if _section == '':
                    continue
                sBase = SectionBase.objects.get(id=int(_section))
                _result = []
                q_st = sBase.questionBases
                q_list = q_st.split(',')
                for _question in q_list:
                    if _question == '':
                        continue
                    qBase = QuestionBase.objects.get(id=int(_question))
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
            self.check_input('id', 'question')
            f = Form.objects.create(formId=self.input['id'], finishTime=datetime.now(), rater=self.request.user)
            pre_s_id = -1
            pre_q_id = -1
            pre_s = None
            s_q = ""
            f_s = ""
            r = ""
            for question in self.input['question']:
                st = question['id']
                res = question['value']
                s_id = int(st.split('_')[0])
                q_id = int(st.split('_')[1])
                if not s_id == pre_s_id:
                    if pre_s is not None:
                        q = Question.objects.create(result=r, question=QuestionBase.objects.get(id=pre_q_id))
                        q.save()
                        s_q = s_q + str(pre_q_id) + ','
                        pre_s.questions = s_q
                        pre_s.save()
                        f_s = f_s + str(pre_s_id) + ','
                    pre_s = Section.objects.create(name=SectionBase.objects.get(id=s_id).name)
                    pre_s_id = s_id
                    pre_q_id = q_id
                    r = res
                else:
                    if not pre_q_id == q_id:
                        q = Question.objects.create(result=r, question=QuestionBase.objects.get(id=pre_q_id))
                        s_q = s_q + str(pre_q_id) + ','
                        r = res
                        pre_q_id = q_id
                    else:
                        r = r + " | " + res
            q = Question.objects.create(result=r, question=QuestionBase.objects.get(id=pre_q_id))
            s_q = s_q + str(pre_q_id) + ','
            pre_s.questions = s_q
            pre_s.save()
            f_s = f_s + str(pre_s_id) + ','
            f.sections = f_s
            f.save()
        else:
            raise LogicError("You haven't log in")