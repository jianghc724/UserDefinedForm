from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from user.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
            if not UserInfo.objects.filter(user_id=u_id):
                u = UserInfo.objects.create(user=self.request.user, authority=1,
                                            name=User.objects.get(id=u_id).username, license="Supervisor")
                u.save()
            else:
                u = UserInfo.objects.get(user_id=u_id)
            apply = []
            if u.authority == 1:
                _a = Apply.objects.filter(isHandled=False)
            elif u.authority == 2:
                _a = Apply.objects.filter(organization=u.organization, isHandled=False)
            elif u.authority == 3:
                _a = Apply.objects.filter(trainee=u_id, isHandled=False)
            else:
                raise LogicError("unknown authority")
            for a in _a:
                t_name = User.objects.get(id=a.trainee).username
                apply.append({
                    'id': a.id,
                    'apply_time': a.applyTime.timestamp(),
                    'trainee': t_name,
                    'type': a.formBaseId,
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
                _a = Apply.objects.filter(trainee=u_id, isHandled=True)
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
                    'form_id': a.formId,
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
            a.save()
        else:
            raise LogicError("You haven't log in")


class CreatePAT(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            t = UserInfo.objects.get(user_id=a.trainee)
            if a.isHandling:
                raise LogicError("Another rater is handling the apply")
            if a.isHandled:
                raise LogicError("Apply has been handled")
            if u.authority == 3:
                raise LogicError("You have no authority")
            a.isHandling = True
            a.save()
            result = {
                'user_status': u.authority,
                'trainee_license': t.license,
                'trainee_name': t.name,
                'trainee_grade': t.grade,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            info = self.input
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            if u.authority == 3:
                raise LogicError("You have no authority")
            f = PAT.objects.create(assessTime=datetime.now(), hospital=info['hospital'],
                                   occupation=info['occupation'], trainee=a.trainee, rater=self.request.user.id,
                                   environment=info['environment'], experience=info['experience'],
                                   historyGrade=info['history'], knowledgeGrade=info['knowledge'],
                                   formulaGrade=info['formula'], technicalGrade=info['technical'],
                                   recordGrade=info['record'], timingGrade=info['timing'],
                                   decisionGrade=info['decision'], awarenessGrade=info['awareness'],
                                   leadershipGrade=info['leadership'], patientGrade=info['patient'],
                                   feedbackGrade=info['feedback'], teachingGrade=info['teaching'],
                                   patientCommunicationGrade=info['patientCommunication'],
                                   selfCommunicationGrade=info['selfCommunication'],
                                   involvementGrade=info['involvement'], reliabilityGrade=info['reliability'],
                                   overallGrade=info['overall'], goodPart=info['good-part'],
                                   developPart=info['develop-part'], probityPart=info['probity'],
                                   assessorSatisfaction=info['assessor-satisfaction'],
                                   assessTimeTaken=info['assessment-time'])
            f.save()
            a.finishTime = datetime.now()
            a.isHandled = True
            a.isHandling = False
            a.rater = self.request.user.id
            a.formId = f.id
            a.save()
        else:
            raise LogicError("You haven't log in")


class CreateOOT(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            t = UserInfo.objects.get(user_id=a.trainee)
            if a.isHandling:
                raise LogicError("Another rater is handling the apply")
            if a.isHandled:
                raise LogicError("Apply has been handled")
            if u.authority == 3:
                raise LogicError("You have no authority")
            a.isHandling = True
            a.save()
            result = {
                'user_status': u.authority,
                'rater_name': u.name,
                'rater_license': u.license,
                'trainee_license': t.license,
                'trainee_name': t.name,
                'trainee_grade': t.grade,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            info = self.input
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            if u.authority == 3:
                raise LogicError("You have no authority")
            f = OOT.objects.create(assessTime=datetime.now(), hospital=info['hospital'],
                                   trainee=a.trainee, rater=self.request.user.id, experience=info['experience'],
                                   groupType=info['setting'], groupOther=info['setting-other'],
                                   groupName=info['group-name'], groupNumber=info['number'],
                                   groupTitle=info['group-title'], groupIntro=info['group-description'],
                                   introGrade=info['intro'], introComment=info['intro-comment'],
                                   presentGrade=info['present'], presentComment=info['present-comment'],
                                   concludeGrade=info['conclude'], concludeComment=info['conclude-comment'],
                                   overallGrade=info['overall'], goodPart=info['good-part'],
                                   developPart=info['develop-part'], agreedPart=info['agreed-part'],
                                   traineeSatisfaction=info['trainee-satisfaction'],
                                   assessorSatisfaction=info['assessor-satisfaction'],
                                   assessTimeTaken=info['assessment-time'], feedbackTimeTaken=info['feedback-time'])
            f.save()
            a.finishTime = datetime.now()
            a.isHandled = True
            a.isHandling = False
            a.rater = self.request.user.id
            a.formId = f.id
            a.save()
        else:
            raise LogicError("You haven't log in")


class CreateDOPS(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            t = UserInfo.objects.get(user_id=a.trainee)
            if a.isHandling:
                raise LogicError("Another rater is handling the apply")
            if a.isHandled:
                raise LogicError("Apply has been handled")
            if u.authority == 3:
                raise LogicError("You have no authority")
            a.isHandling = True
            a.save()
            result = {
                'user_status': u.authority,
                'rater_name': u.name,
                'rater_license': u.license,
                'trainee_license': t.license,
                'trainee_name': t.name,
                'trainee_grade': t.grade,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            info = self.input
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            if u.authority == 3:
                raise LogicError("You have no authority")
            f = DOPS.objects.create(assessTime=datetime.now(), hospital=info['hospital'],
                                    trainee=a.trainee, rater=self.request.user.id, experience=info['experience'],
                                    clinicalSetting=info['setting'], procedureName=info['procedure'],
                                    observeName=info['part'], procedureTime=info['times'],
                                    complexity=info['complexity'], descriptionGrade=info['description'],
                                    explanationGrade=info['explanation'], preparationGrade=info['preparation'],
                                    sedationGrade=info['sedation'], safetyGrade=info['safety'],
                                    performanceGrade=info['performance'], emergencyGrade=info['emergency'],
                                    documentationGrade=info['documentation'],
                                    communicationGrade=info['communication'],
                                    demonstrationGrade=info['demonstration'], overallGrade=info['overall'],
                                    goodPart=info['good-part'], developPart=info['develop-part'],
                                    agreedPart=info['agreed-part'], traineeSatisfaction=info['trainee-satisfaction'],
                                    assessorSatisfaction=info['assessor-satisfaction'],
                                    assessTimeTaken=info['assessment-time'], feedbackTimeTaken=info['feedback-time'])
            f.save()
            a.finishTime = datetime.now()
            a.isHandled = True
            a.isHandling = False
            a.rater = self.request.user.id
            a.formId = f.id
            a.save()
        else:
            raise LogicError("You haven't log in")


class CreateCEX(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            t = UserInfo.objects.get(user_id=a.trainee)
            if a.isHandling:
                raise LogicError("Another rater is handling the apply")
            if a.isHandled:
                raise LogicError("Apply has been handled")
            if u.authority == 3:
                raise LogicError("You have no authority")
            a.isHandling = True
            a.save()
            result = {
                'user_status': u.authority,
                'rater_name': u.name,
                'rater_license': u.license,
                'trainee_license': t.license,
                'trainee_name': t.name,
                'trainee_grade': t.grade,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            info = self.input
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            if u.authority == 3:
                raise LogicError("You have no authority")
            f = CEX.objects.create(assessTime=datetime.now(), hospital=info['hospital'],
                                   trainee=a.trainee, rater=self.request.user.id, experience=info['experience'],
                                   clinicalSetting=info['setting'], clinicalOther=info['setting-other'],
                                   clinicalSummary=info['summary'], clinicalFocus=info['focus'],
                                   complexity=info['complexity'], historyGrade=info['history'],
                                   examGrade=info['exam'], knowledgeGrade=info['knowledge'],
                                   managementGrade=info['management'], judgmentGrade=info['judgment'],
                                   communicationGrade=info['communication'],
                                   organisationGrade=info['timing'], overallGrade=info['overall'],
                                   goodPart=info['good-part'], developPart=info['develop-part'],
                                   agreedPart=info['agreed-part'], traineeSatisfaction=info['trainee-satisfaction'],
                                   assessorSatisfaction=info['assessor-satisfaction'],
                                   assessTimeTaken=info['assessment-time'], feedbackTimeTaken=info['feedback-time'])
            f.save()
            a.finishTime = datetime.now()
            a.isHandled = True
            a.isHandling = False
            a.rater = self.request.user.id
            a.formId = f.id
            a.save()
        else:
            raise LogicError("You haven't log in")


class CreateCBD(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            t = UserInfo.objects.get(user_id=a.trainee)
            if a.isHandling:
                raise LogicError("Another rater is handling the apply")
            if a.isHandled:
                raise LogicError("Apply has been handled")
            if u.authority == 3:
                raise LogicError("You have no authority")
            a.isHandling = True
            a.save()
            result = {
                'user_status': u.authority,
                'rater_name': u.name,
                'rater_license': u.license,
                'trainee_license': t.license,
                'trainee_name': t.name,
                'trainee_grade': t.grade,
            }
            return result
        else:
            raise LogicError("You haven't log in")

    def post(self):
        if self.request.user.is_authenticated():
            info = self.input
            self.check_input('id')
            u = UserInfo.objects.get(user_id=self.request.user.id)
            a = Apply.objects.get(id=self.input['id'])
            if u.authority == 3:
                raise LogicError("You have no authority")
            f = CBD.objects.create(assessTime=datetime.now(), hospital=info['hospital'],
                                   isReflective=info['reflected'], isRelated=info['related'],
                                   trainee=a.trainee, rater=self.request.user.id, experience=info['experience'],
                                   clinicalSetting=info['setting'], clinicalOther=info['setting-other'],
                                   clinicalSummary=info['summary'], clinicalFocus=info['focus'],
                                   complexity=info['complexity'], recordGrade=info['record'],
                                   assessmentGrade=info['assessment'], knowledgeGrade=info['knowledge'],
                                   managementGrade=info['management'], judgmentGrade=info['judgment'],
                                   communicationGrade=info['communication'], reflectiveGrade=info['reflective'],
                                   leadershipGrade=info['leadership'], overallGrade=info['overall'],
                                   goodPart=info['good-part'], developPart=info['develop-part'],
                                   agreedPart=info['agreed-part'], traineeSatisfaction=info['trainee-satisfaction'],
                                   assessorSatisfaction=info['assessor-satisfaction'],
                                   assessTimeTaken=info['assessment-time'], feedbackTimeTaken=info['feedback-time'])
            f.save()
            a.finishTime = datetime.now()
            a.isHandled = True
            a.isHandling = False
            a.rater = self.request.user.id
            a.formId = f.id
            a.save()
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
                'assessTime': f.assessTime.timestamp(),
                'hospital': f.hospital,
                'occupation': f.occupation,
                'trainee': t.name,
                'trainee_license': t.license,
                'year': t.grade,
                'environment': f.environment,
                'experience': f.experience,
                'history': f.historyGrade,
                'knowledge': f.knowledgeGrade,
                'formula': f.formulaGrade,
                'technical': f.technicalGrade,
                'record': f.recordGrade,
                'timing': f.timingGrade,
                'decision': f.decisionGrade,
                'awareness': f.awarenessGrade,
                'leadership': f.leadershipGrade,
                'patient': f.patientGrade,
                'feedback': f.feedbackGrade,
                'teaching': f.teachingGrade,
                'patientCommunication': f.patientCommunicationGrade,
                'selfCommunication': f.selfCommunicationGrade,
                'involvement': f.involvementGrade,
                'reliability': f.reliabilityGrade,
                'overall': f.overallGrade,
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
                'assessTime': f.assessTime.timestamp(),
                'hospital': f.hospital,
                'rater': r.name,
                'rater_license': r.license,
                'trainee': t.name,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'groupType': f.groupType,
                'groupOther': f.groupOther,
                'groupName': f.groupName,
                'groupNumber': f.groupNumber,
                'groupTitle': f.groupTitle,
                'groupIntro': f.groupIntro,
                'intro': f.introGrade,
                'introComment': f.introComment,
                'present': f.presentGrade,
                'presentComment': f.presentComment,
                'conclude': f.concludeGrade,
                'concludeComment': f.concludeComment,
                'overall': f.overallGrade,
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
                'assessTime': f.assessTime.timestamp(),
                'hospital': f.hospital,
                'rater': r.name,
                'rater_license': r.license,
                'trainee': t.name,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'clinicalSetting': f.clinicalSetting,
                'procedureName': f.procedureName,
                'observeName': f.observeName,
                'procedureTime': f.procedureTime,
                'complexity': f.complexity,
                'description': f.descriptionGrade,
                'explanation': f.explanationGrade,
                'preparation': f.preparationGrade,
                'sedation': f.sedationGrade,
                'safety': f.safetyGrade,
                'performance': f.performanceGrade,
                'emergency': f.emergencyGrade,
                'documentation': f.documentationGrade,
                'communication': f.communicationGrade,
                'demonstration': f.demonstrationGrade,
                'overall': f.overallGrade,
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
                'assessTime': f.assessTime.timestamp(),
                'hospital': f.hospital,
                'rater': r.name,
                'rater_license': r.license,
                'trainee': t.name,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'clinicalSetting': f.clinicalSetting,
                'clinicalOther': f.clinicalOther,
                'clinicalSummary': f.clinicalSummary,
                'clinicalFocus': f.clinicalFocus,
                'complexity': f.complexity,
                'history': f.historyGrade,
                'exam': f.examGrade,
                'knowledge': f.knowledgeGrade,
                'management': f.managementGrade,
                'judgment': f.judgmentGrade,
                'communication': f.communicationGrade,
                'organisation': f.organisationGrade,
                'overall': f.overallGrade,
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
            f = CBD.objects.get(id=self.input['id'])
            u = UserInfo.objects.get(user_id=u_id)
            r = UserInfo.objects.get(user_id=f.rater)
            t = UserInfo.objects.get(user_id=f.trainee)
            if u.authority == 3 and not f.trainee == u_id:
                raise LogicError("You have no access to it")
            elif u.authority == 2 and not t.organization == u.organization:
                raise LogicError("You have no access to it")
            result = {
                'user_status': u.authority,
                'isReflected': f.isReflective,
                'isRelated': f.isRelated,
                'assessTime': f.assessTime.timestamp(),
                'hospital': f.hospital,
                'rater': r.name,
                'rater_license': r.license,
                'trainee': t.name,
                'trainee_license': t.license,
                'year': t.grade,
                'experience': f.experience,
                'clinicalSetting': f.clinicalSetting,
                'clinicalOther': f.clinicalOther,
                'clinicalSummary': f.clinicalSummary,
                'clinicalFocus': f.clinicalFocus,
                'complexity': f.complexity,
                'record': f.recordGrade,
                'assessment': f.assessmentGrade,
                'knowledge': f.knowledgeGrade,
                'management': f.managementGrade,
                'judgment': f.judgmentGrade,
                'communication': f.communicationGrade,
                'leadership': f.leadershipGrade,
                'reflective': f.reflectiveGrade,
                'overall': f.overallGrade,
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
                info = self.input['user']
                _nu = User.objects.create_user(username=info['username'], password=info['password'])
                _nu.save()
                nu = UserInfo.objects.create(user=_nu, name=info['name'], license=info['license'],
                                             grade=info['grade'], authority=3, organization=u.organization)
                nu.save()
            elif u.authority == 1:
                info = self.input['user']
                _nu = User.objects.create_user(username=info['username'], password=info['password'])
                _nu.save()
                nu = UserInfo.objects.create(user=_nu, name=info['name'], license=info['license'],
                                             authority=2, organization=info['organization'])
                nu.save()
            else:
                raise LogicError("No such authority")
        else:
            raise LogicError("You haven't log in")
