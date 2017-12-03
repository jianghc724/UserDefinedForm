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
            u_id = self.request.user.id
            u = UserInfo.objects.get(user_id=u_id)
            apply = []
            if u.authority == 1:
                _a = Apply.objects.filter(isHandled=False)
            elif u.authority == 2:
                _a = Apply.objects.filter(organization=u.organization, isHandled=False)
            elif u.authority == 3:
                _a = Apply.objects.filter(organization=u.id, isHandled=False)
            else:
                raise LogicError("unknown authority")
            for a in _a:
                t_name = User.objects.get(id=a.trainee).username
                apply.append({
                    'id': a.id,
                    'apply_time': a.applyTime.timestamp(),
                    'trainee': t_name,
                    'form_base': a.formBaseId,
                })
            result = {
                'user_status': u.authority,
                'apply': apply,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class FormList(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            u_id = self.request.user.id
            u = UserInfo.objects.get(user_id=u_id)
            apply = []
            if u.authority == 1:
                _a = Apply.objects.filter(isHandled=True)
            elif u.authority == 2:
                _a = Apply.objects.filter(organization=u.organization, isHandled=True)
            elif u.authority == 3:
                _a = Apply.objects.filter(organization=u.id, isHandled=True)
            else:
                raise LogicError("unknown authority")
            for a in _a:
                t_name = User.objects.get(id=a.trainee).username
                r_name = User.objects.get(id=a.rater).username
                apply.append({
                    'id': a.id,
                    'apply_time': a.applyTime.timestamp(),
                    'finish_time': a.finishTime.timestamp(),
                    'trainee': t_name,
                    'rater': r_name,
                    'form_base': a.formBaseId,
                    'form_id':a.formId,
                })
            result = {
                'user_status': u.authority,
                'apply': apply,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateApply(APIView):
    def get(self):
        pass

    def post(self):
        if self.request.user.is_authenticated():
            self.check_input('type')
            t = self.input['type']
            t_id = self.request.user.id
            u = UserInfo.objects.get(user_id=t_id)
            if t == 'cbd':
                a = Apply.objects.create(trainee=t_id, organization=u.organization, formBaseId=1,
                                         applyTime=datetime.now())
            elif t == 'cex':
                a = Apply.objects.create(trainee=t_id, organization=u.organization, formBaseId=2,
                                         applyTime=datetime.now())
            elif t == 'dops':
                a = Apply.objects.create(trainee=t_id, organization=u.organization, formBaseId=3,
                                         applyTime=datetime.now())
            elif t == 'oot':
                a = Apply.objects.create(trainee=t_id, organization=u.organization, formBaseId=4,
                                         applyTime=datetime.now())
            elif t == 'pat':
                a = Apply.objects.create(trainee=t_id, organization=u.organization, formBaseId=5,
                                         applyTime=datetime.now())
            else:
                raise LogicError("No such type")
        else:
            raise LogicError("You haven't log in")


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


class PATForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u_id = self.request.user.id
            f = PAT.objects.get(id=self.input['id'])
            u = UserInfo.objects.get(user_id=u_id)
            r = UserInfo.objects.get(user_id=f.rater)
            t = UserInfo.objects.get(user_id=f.trainee)
            if u.authority == 3 and not f.trainee == u_id:
                raise LogicError("You have no access to it")
            elif u.authority == 2 and not t.organization == u.organization:
                raise LogicError("You have no access to it")
            result = {
                'user_status': u.authority,
                'assessTime': f.assessTime,
                'hospital': f.hospital,
                'occupation': f.occupation,
                'trainee': f.trainee,
                'trainee_license': t.license,
                'year': t.grade,
                'environment': f.environment,
                'experience': f.experience,
                'historyGrade': f.historyGrade,
                'knowledgeGrade': f.knowledgeGrade,
                'formulaGrade': f.formulaGrade,
                'technicalGrade': f.technicalGrade,
                'recordGrade': f.recordGrade,
                'timingGrade': f.timingGrade,
                'decisionGrade': f.decisionGrade,
                'awarenessGrade': f.awarenessGrade,
                'leadershipGrade': f.leadershipGrade,
                'patientGrade': f.patientGrade,
                'feedbackGrade': f.feedbackGrade,
                'teachingGrade': f.teachingGrade,
                'patientCommunicationGrade': f.patientCommunicationGrade,
                'selfCommunicationGrade': f.selfCommunicationGrade,
                'involvementGrade': f.involvementGrade,
                'reliabilityGrade': f.reliabilityGrade,
                'overallGrade': f.overallGrade,
                'goodPart': f.goodPart,
                'developPart': f.developPart,
                'probityPart': f.probityPart,
                'assessorSatisfaction': f.assessorSatisfaction,
                'assessTimeTaken': f.assessTimeTaken,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class OOTForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u_id = self.request.user.id
            f = OOT.objects.get(id=self.input['id'])
            u = UserInfo.objects.get(user_id=u_id)
            r = UserInfo.objects.get(user_id=f.rater)
            t = UserInfo.objects.get(user_id=f.trainee)
            if u.authority == 3 and not f.trainee == u_id:
                raise LogicError("You have no access to it")
            elif u.authority == 2 and not t.organization == u.organization:
                raise LogicError("You have no access to it")
            result = {
                'user_status': u.authority,
                'assessTime': f.assessTime,
                'hospital': f.hospital,
                'rater': f.rater,
                'rater_license': r.license,
                'trainee': f.trainee,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'groupType': f.groupType,
                'groupOther': f.groupOther,
                'groupName': f.groupName,
                'groupNumber': f.groupNumber,
                'groupTitle': f.groupTitle,
                'groupIntro': f.groupIntro,
                'introGrade': f.introGrade,
                'introComment': f.introComment,
                'presentGrade': f.presentGrade,
                'presentComment': f.presentComment,
                'concludeGrade': f.concludeGrade,
                'concludeComment': f.concludeComment,
                'overallGrade': f.overallGrade,
                'overallComment': f.overallComment,
                'goodPart': f.goodPart,
                'developPart': f.developPart,
                'agreedPart': f.agreedPart,
                'traineeSatisfaction': f.traineeSatisfaction,
                'assessorSatisfaction': f.assessorSatisfaction,
                'assessTimeTaken': f.assessTimeTaken,
                'feedbackTimeTaken': f.feedbackTimeTaken,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class DOPSForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u_id = self.request.user.id
            f = DOPS.objects.get(id=self.input['id'])
            u = UserInfo.objects.get(user_id=u_id)
            r = UserInfo.objects.get(user_id=f.rater)
            t = UserInfo.objects.get(user_id=f.trainee)
            if u.authority == 3 and not f.trainee == u_id:
                raise LogicError("You have no access to it")
            elif u.authority == 2 and not t.organization == u.organization:
                raise LogicError("You have no access to it")
            result = {
                'user_status': u.authority,
                'assessTime': f.assessTime,
                'hospital': f.hospital,
                'rater': f.rater,
                'rater_license': r.license,
                'trainee': f.trainee,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'clinicalSetting': f.clinicalSetting,
                'procedureName': f.procedureName,
                'observeName': f.observeName,
                'procedureTime': f.procedureTime,
                'complexity': f.complexity,
                'descriptionGrade': f.descriptionGrade,
                'explanationGrade': f.explanationGrade,
                'preparationGrade': f.preparationGrade,
                'sedationGrade': f.sedationGrade,
                'safetyGrade': f.safetyGrade,
                'performanceGrade': f.performanceGrade,
                'emergencyGrade': f.emergencyGrade,
                'documentationGrade': f.documentationGrade,
                'communicationGrade': f.communicationGrade,
                'demonstrationGrade': f.demonstrationGrade,
                'overallGrade': f.overallGrade,
                'goodPart': f.goodPart,
                'developPart': f.developPart,
                'agreedPart': f.agreedPart,
                'traineeSatisfaction': f.traineeSatisfaction,
                'assessorSatisfaction': f.assessorSatisfaction,
                'assessTimeTaken': f.assessTimeTaken,
                'feedbackTimeTaken': f.feedbackTimeTaken,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CEXForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u_id = self.request.user.id
            f = CEX.objects.get(id=self.input['id'])
            u = UserInfo.objects.get(user_id=u_id)
            r = UserInfo.objects.get(user_id=f.rater)
            t = UserInfo.objects.get(user_id=f.trainee)
            if u.authority == 3 and not f.trainee == u_id:
                raise LogicError("You have no access to it")
            elif u.authority == 2 and not t.organization == u.organization:
                raise LogicError("You have no access to it")
            result = {
                'user_status': u.authority,
                'assessTime': f.assessTime,
                'hospital': f.hospital,
                'rater': f.rater,
                'rater_license': r.license,
                'trainee': f.trainee,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'clinicalSetting': f.clinicalSetting,
                'clinicalOther': f.clinicalOther,
                'clinicalSummary': f.clinicalSummary,
                'clinicalFocus': f.clinicalFocus,
                'complexity': f.complexity,
                'historyGrade': f.historyGrade,
                'examGrade': f.examGrade,
                'knowledgeGrade': f.knowledgeGrade,
                'managementGrade': f.managementGrade,
                'judgmentGrade': f.judgmentGrade,
                'communicationGrade': f.communicationGrade,
                'organisationGrade': f.organisationGrade,
                'overallGrade': f.overallGrade,
                'goodPart': f.goodPart,
                'developPart': f.developPart,
                'agreedPart': f.agreedPart,
                'traineeSatisfaction': f.traineeSatisfaction,
                'assessorSatisfaction': f.assessorSatisfaction,
                'assessTimeTaken': f.assessTimeTaken,
                'feedbackTimeTaken': f.feedbackTimeTaken,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CBDForm(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u_id = self.request.user.id
            f = OOT.objects.get(id=self.input['id'])
            u = UserInfo.objects.get(user_id=u_id)
            r = UserInfo.objects.get(user_id=f.rater)
            t = UserInfo.objects.get(user_id=f.trainee)
            if u.authority == 3 and not f.trainee == u_id:
                raise LogicError("You have no access to it")
            elif u.authority == 2 and not t.organization == u.organization:
                raise LogicError("You have no access to it")
            result = {
                'user_status': u.authority,
                'assessTime': f.assessTime,
                'hospital': f.hospital,
                'rater': f.rater,
                'rater_license': r.license,
                'trainee': f.trainee,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'clinicalSetting': f.clinicalSetting,
                'clinicalSummary': f.clinicalSummary,
                'clinicalFocus': f.clinicalFocus,
                'complexity': f.complexity,
                'recordGrade': f.recordGrade,
                'assessmentGrade': f.assessmentGrade,
                'knowledgeGrade': f.knowledgeGrade,
                'managementGrade': f.managementGrade,
                'judgmentGrade': f.judgmentGrade,
                'communicationGrade': f.communicationGrade,
                'leadershipGrade': f.leadershipGrade,
                'reflectiveGrade': f.reflectiveGrade,
                'overallGrade': f.overallGrade,
                'goodPart': f.goodPart,
                'developPart': f.developPart,
                'agreedPart': f.agreedPart,
                'traineeSatisfaction': f.traineeSatisfaction,
                'assessorSatisfaction': f.assessorSatisfaction,
                'assessTimeTaken': f.assessTimeTaken,
                'feedbackTimeTaken': f.feedbackTimeTaken,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateUser(APIView):
    def get(self):
        pass

    def post(self):
        pass
