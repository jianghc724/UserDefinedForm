from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from codex.baseerror import *

# Create your models here.


class UserProfileManager(BaseUserManager):
    def create_user(self, license, name, password='Test123,.'):
        if not license:
            raise LogicError('You need a license')

        user = self.model(
            license=license,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, license, name, password='Test123,.'):
        if not license:
            raise LogicError('You need a license')

        user = self.model(
            license=license,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    name = models.CharField(max_length=20)
    license = models.CharField(max_length=20, unique=True)

    objects = UserProfileManager()  # 创建用户

    USERNAME_FIELD = 'license'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.license

    def get_short_name(self):
        # The user is identified by their email address
        return self.license

    def __str__(self):  # __unicode__ on Python 2
        return self.license

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class QuestionBase(models.Model):
    questionInfo = models.TextField()
    questionType = models.IntegerField() # 1 for single choice 2 for multiple choice 3 for filling 4 for rating
    choiceOne = models.CharField(max_length=50)
    choiceTwo = models.CharField(max_length=50)
    choiceThree = models.CharField(max_length=50)
    choiceFour = models.CharField(max_length=50)


class SectionBase(models.Model):
    questionCount = models.IntegerField(default=0)
    questionOne = models.ForeignKey(QuestionBase, related_name='question_one')
    questionTwo = models.ForeignKey(QuestionBase, related_name='question_two')
    questionThree = models.ForeignKey(QuestionBase, related_name='question_three')
    questionFour = models.ForeignKey(QuestionBase, related_name='question_four')
    questionFive = models.ForeignKey(QuestionBase, related_name='question_five')
    questionSix = models.ForeignKey(QuestionBase, related_name='question_six')
    questionSeven = models.ForeignKey(QuestionBase, related_name='question_seven')
    questionEight = models.ForeignKey(QuestionBase, related_name='question_eight')
    questionNine = models.ForeignKey(QuestionBase, related_name='question_nine')
    questionTen = models.ForeignKey(QuestionBase, related_name='question_ten')


class FormBase(models.Model):
    sectionCount = models.IntegerField(default=0)
    sectionOne = models.ForeignKey(SectionBase, related_name='section_one')
    sectionTwo = models.ForeignKey(SectionBase, related_name='section_two')
    sectionThree = models.ForeignKey(SectionBase, related_name='section_three')
    sectionFour = models.ForeignKey(SectionBase, related_name='section_four')
    sectionFive = models.ForeignKey(SectionBase, related_name='section_five')


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
    questionOne = models.ForeignKey(Question, related_name='question_one')
    questionTwo = models.ForeignKey(Question, related_name='question_two')
    questionThree = models.ForeignKey(Question, related_name='question_three')
    questionFour = models.ForeignKey(Question, related_name='question_four')
    questionFive = models.ForeignKey(Question, related_name='question_five')
    questionSix = models.ForeignKey(Question, related_name='question_six')
    questionSeven = models.ForeignKey(Question, related_name='question_seven')
    questionEight = models.ForeignKey(Question, related_name='question_eight')
    questionNine = models.ForeignKey(Question, related_name='question_nine')
    questionTen = models.ForeignKey(Question, related_name='question_ten')
    sectionFinished = models.BooleanField(default=False)


class Form(models.Model):
    sectionCount = models.IntegerField(default=0)
    sectionOne = models.ForeignKey(Section, related_name='section_one')
    sectionTwo = models.ForeignKey(Section, related_name='section_two')
    sectionThree = models.ForeignKey(Section, related_name='section_three')
    sectionFour = models.ForeignKey(Section, related_name='section_four')
    sectionFive = models.ForeignKey(Section, related_name='section_five')
    formNumber = models.IntegerField()
    formFinished = models.BooleanField(default=False)
    trainee = models.ForeignKey(UserProfile, related_name='trainee')
    rater = models.ForeignKey(UserProfile, related_name='rater')


class Apply(models.Model):
    form = models.ForeignKey(Form)
    trainee = models.ForeignKey(UserProfile)
    time = models.DateTimeField()