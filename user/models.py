from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from codex.baseerror import *

# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    license = models.CharField(max_length=20, null=True)
    grade = models.IntegerField(default=-1)
    authority = models.IntegerField(default=-1)  # 1 for supervisior 2 for rater 3 for trainee
    organization = models.IntegerField(default=-1)


class Apply(models.Model):
    trainee = models.IntegerField(default=-1)
    organization = models.IntegerField(default=-1)
    isHandled = models.BooleanField(default=False)
    isHandling = models.BooleanField(default=False)
    formBaseId = models.IntegerField(default=-1)
    formId = models.IntegerField(default=-1)
    rater = models.IntegerField(default=-1)
    applyTime = models.DateTimeField(null=True)
    finishTime = models.DateTimeField(null=True)


class OOT(models.Model):
    assessTime = models.DateTimeField(null=True)
    hospital = models.IntegerField(default=-1)
    rater = models.IntegerField(default=-1)
    trainee = models.IntegerField(default=-1)
    experience = models.IntegerField(default=0)
    groupType = models.IntegerField(default=-1)  # 1 for lecture 2 for seminar 3 for ward 4 for others
    groupOther = models.CharField(null=True, max_length=20)
    groupName = models.CharField(max_length=20)
    groupNumber = models.IntegerField(default=-1)
    groupTitle = models.CharField(max_length=20)
    groupIntro = models.TextField(max_length=200)
    introGrade = models.IntegerField(default=-1)
    introComment = models.TextField(null=True, max_length=200)
    presentGrade = models.IntegerField(default=-1)
    presentComment = models.TextField(null=True, max_length=200)
    concludeGrade = models.IntegerField(default=-1)
    concludeComment = models.TextField(null=True, max_length=200)
    overallGrade = models.IntegerField(default=-1)
    goodPart = models.IntegerField(default=0)
    developPart = models.IntegerField(default=0)
    agreedPart = models.IntegerField(default=0)
    traineeSatisfaction = models.IntegerField(default=-1)
    assessorSatisfaction = models.IntegerField(default=-1)
    assessTimeTaken = models.IntegerField(default=-1)
    feedbackTimeTaken = models.IntegerField(default=-1)


class CEX(models.Model):
    assessTime = models.DateTimeField(null=True)
    hospital = models.IntegerField(default=-1)
    rater = models.IntegerField(default=-1)
    trainee = models.IntegerField(default=-1)
    experience = models.IntegerField(default=0)
    clinicalSetting = models.IntegerField(default=-1)  # 1 for ward 2 for clinic 3 for others
    clinicalOther = models.CharField(null=True, max_length=20)
    clinicalSummary = models.TextField(max_length=200)
    clinicalFocus = models.CharField(max_length=20)
    complexity = models.IntegerField(default=-1)  # 1 for low 2 for medium 3 for high
    historyGrade = models.IntegerField(default=-1)
    examGrade = models.IntegerField(default=-1)
    knowledgeGrade = models.IntegerField(default=-1)
    managementGrade = models.IntegerField(default=-1)
    judgmentGrade = models.IntegerField(default=-1)
    communicationGrade = models.IntegerField(default=-1)
    organisationGrade = models.IntegerField(default=-1)
    overallGrade = models.IntegerField(default=-1)
    goodPart = models.IntegerField(default=0)
    developPart = models.IntegerField(default=0)
    agreedPart = models.IntegerField(default=0)
    traineeSatisfaction = models.IntegerField(default=-1)
    assessorSatisfaction = models.IntegerField(default=-1)
    assessTimeTaken = models.IntegerField(default=-1)
    feedbackTimeTaken = models.IntegerField(default=-1)


class DOPS(models.Model):
    assessTime = models.DateTimeField(null=True)
    hospital = models.IntegerField(default=-1)
    rater = models.IntegerField(default=-1)
    trainee = models.IntegerField(default=-1)
    experience = models.IntegerField(default=0)
    clinicalSetting = models.IntegerField(default=-1)  # 1 for operating room 2 for emergency room 3 for ward 4 for clinic 5 for others
    procedureName = models.CharField(max_length=20)
    observeName = models.CharField(max_length=20)
    procedureTime = models.IntegerField(default=-1)
    complexity = models.IntegerField(default=-1)  # 1 for low 2 for medium 3 for high
    descriptionGrade = models.IntegerField(default=-1)
    explanationGrade = models.IntegerField(default=-1)
    preparationGrade = models.IntegerField(default=-1)
    sedationGrade = models.IntegerField(default=-1)
    safetyGrade = models.IntegerField(default=-1)
    performanceGrade = models.IntegerField(default=-1)
    emergencyGrade = models.IntegerField(default=-1)
    documentationGrade = models.IntegerField(default=-1)
    communicationGrade = models.IntegerField(default=-1)
    demonstrationGrade = models.IntegerField(default=-1)
    overallGrade = models.IntegerField(default=-1)
    goodPart = models.IntegerField(default=0)
    developPart = models.IntegerField(default=0)
    agreedPart = models.IntegerField(default=0)
    traineeSatisfaction = models.IntegerField(default=-1)
    assessorSatisfaction = models.IntegerField(default=-1)
    assessTimeTaken = models.IntegerField(default=-1)
    feedbackTimeTaken = models.IntegerField(default=-1)


class CBD(models.Model):
    isReflective = models.BooleanField(default=False)
    isRelated = models.BooleanField(default=False)
    assessTime = models.DateTimeField(null=True)
    hospital = models.IntegerField(default=-1)
    rater = models.IntegerField(default=-1)
    trainee = models.IntegerField(default=-1)
    experience = models.IntegerField(default=0)
    clinicalSetting = models.IntegerField(default=-1)  # 1 for ward 2 for clinic 3 for others
    clinicalOther = models.CharField(null=True, max_length=20)
    clinicalSummary = models.TextField(max_length=200)
    clinicalFocus = models.CharField(max_length=20)
    complexity = models.IntegerField(default=-1)  # 1 for low 2 for medium 3 for high
    recordGrade = models.IntegerField(default=-1)
    assessmentGrade = models.IntegerField(default=-1)
    knowledgeGrade = models.IntegerField(default=-1)
    managementGrade = models.IntegerField(default=-1)
    judgmentGrade = models.IntegerField(default=-1)
    communicationGrade = models.IntegerField(default=-1)
    leadershipGrade = models.IntegerField(default=-1)
    reflectiveGrade = models.IntegerField(default=-1)
    overallGrade = models.IntegerField(default=-1)
    goodPart = models.IntegerField(default=0)
    developPart = models.IntegerField(default=0)
    agreedPart = models.IntegerField(default=0)
    traineeSatisfaction = models.IntegerField(default=-1)
    assessorSatisfaction = models.IntegerField(default=-1)
    assessTimeTaken = models.IntegerField(default=-1)
    feedbackTimeTaken = models.IntegerField(default=-1)


class PAT(models.Model):
    assessTime = models.DateTimeField(null=True)
    hospital = models.IntegerField(default=-1)
    rater = models.IntegerField(default=-1)
    trainee = models.IntegerField(default=-1)
    occupation = models.CharField(max_length=20)
    environment = models.CharField(max_length=20)
    experience = models.BooleanField(default=0)
    historyGrade = models.IntegerField(default=-1)
    knowledgeGrade = models.IntegerField(default=-1)
    formulaGrade = models.IntegerField(default=-1)
    technicalGrade = models.IntegerField(default=-1)
    recordGrade = models.IntegerField(default=-1)
    timingGrade = models.IntegerField(default=-1)
    decisionGrade = models.IntegerField(default=-1)
    awarenessGrade = models.IntegerField(default=-1)
    leadershipGrade = models.IntegerField(default=-1)
    patientGrade = models.IntegerField(default=-1)
    feedbackGrade = models.IntegerField(default=-1)
    teachingGrade = models.IntegerField(default=-1)
    patientCommunicationGrade = models.IntegerField(default=-1)
    selfCommunicationGrade = models.IntegerField(default=-1)
    involvementGrade = models.IntegerField(default=-1)
    reliabilityGrade = models.IntegerField(default=-1)
    overallGrade = models.IntegerField(default=-1)
    goodPart = models.TextField(null=True)
    developPart = models.TextField(null=True)
    probityPart = models.TextField(null=True)
    assessorSatisfaction = models.IntegerField(default=-1)
    assessTimeTaken = models.IntegerField(default=-1)