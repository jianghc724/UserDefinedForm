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


class CreatePAT(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            result = {
                'user_status': u.authority,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateOOT(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            result = {
                'user_status': u.authority,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateDOPS(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            result = {
                'user_status': u.authority,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateCEX(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            result = {
                'user_status': u.authority,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


class CreateCBD(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            result = {
                'user_status': u.authority,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        pass


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
        if self.request.user.is_authenticated():
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            result = {
                'user_status': u.authority,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            self.check_input('user')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            if u.authority == 3:
                raise LogicError("You have no authority")
            elif u.authority == 2:
                for info in self.input['user']:
                    _nu = User.objects.create(username=info['username'], password=info['password'])
                    _nu.save()
                    nu = UserInfo.objects.create(user=_nu, name=info['name'], license=info['license'],
                                                 grade=info['grade'], authority=3, organization=u.organization)
                    nu.save()
            elif u.authority == 1:
                for info in self.input['user']:
                    _nu = User.objects.create(username=info['username'], password=info['password'])
                    _nu.save()
                    nu = UserInfo.objects.create(user=_nu, name=info['name'], license=info['license'],
                                                 grade=info['grade'], authority=2, organization=info['organization'])
                    nu.save()
            else:
                raise LogicError("No such authority")
        else:
            raise LogicError("You haven't log in")
