from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)


class QuestionBase(models.Model):
    questionInfo = models.TextField()
    questionType = models.IntegerField() # 1 for single choice 2 for multiple choice 3 for filling 4 for rating
    choiceOne = models.CharField(max_length=50)
    choiceTwo = models.CharField(max_length=50)
    choiceThree = models.CharField(max_length=50)
    choiceFour = models.CharField(max_length=50)


class SectionBase(models.Model):
    questionCount = models.IntegerField(default=0)
    questionOne = models.ForeignKey(QuestionBase)
    questionTwo = models.ForeignKey(QuestionBase)
    questionThree = models.ForeignKey(QuestionBase)
    questionFour = models.ForeignKey(QuestionBase)
    questionFive = models.ForeignKey(QuestionBase)
    questionSix = models.ForeignKey(QuestionBase)
    questionSeven = models.ForeignKey(QuestionBase)
    questionEight = models.ForeignKey(QuestionBase)
    questionNine = models.ForeignKey(QuestionBase)
    questionTen = models.ForeignKey(QuestionBase)


class FormBase(models.Model):
    sectionCount = models.IntegerField(default=0)
    sectionOne = models.ForeignKey(SectionBase)
    sectionTwo = models.ForeignKey(SectionBase)
    sectionThree = models.ForeignKey(SectionBase)
    sectionFour = models.ForeignKey(SectionBase)
    sectionFive = models.ForeignKey(SectionBase)


class Question(models.Model):
    question = models.ForeignKey(QuestionBase)
    questionFinished = models.BooleanField(default=False)
    result = models.TextField()
    isChoiceOne = models.BooleanField(default=False)
    isChoiceTwo = models.BooleanField(default=False)
    isChoiceThree = models.BooleanField(default=False)
    isChoiceFour = models.BooleanField(default=False)


class Section(models.Model):
    questionCount = models.IntegerField(default=0)
    questionOne = models.ForeignKey(Question)
    questionTwo = models.ForeignKey(Question)
    questionThree = models.ForeignKey(Question)
    questionFour = models.ForeignKey(Question)
    questionFive = models.ForeignKey(Question)
    questionSix = models.ForeignKey(Question)
    questionSeven = models.ForeignKey(Question)
    questionEight = models.ForeignKey(Question)
    questionNine = models.ForeignKey(Question)
    questionTen = models.ForeignKey(Question)
    sectionFinished = models.BooleanField(default=False)


class Form(models.Model):
    sectionCount = models.IntegerField(default=0)
    sectionOne = models.ForeignKey(Section)
    sectionTwo = models.ForeignKey(Section)
    sectionThree = models.ForeignKey(Section)
    sectionFour = models.ForeignKey(Section)
    sectionFive = models.ForeignKey(Section)
    formNumber = models.IntegerField()
    formFinished = models.BooleanField(default=False)
    trainee = models.ForeignKey(User)
    rater = models.ForeignKey(User)