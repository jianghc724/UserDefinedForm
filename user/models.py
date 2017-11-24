from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from codex.baseerror import *

# Create your models here.


'''class UserProfileManager(BaseUserManager):
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
'''


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)


class QuestionBase(models.Model):
    questionName = models.TextField(null=True)
    questionInfo = models.TextField(null=True)
    questionType = models.IntegerField(default=0) # 1 for single choice 2 for multiple choice 3 for filling 4 for rating
    choiceCount = models.IntegerField(default=0)
    choiceOne = models.CharField(max_length=50)
    choiceTwo = models.CharField(max_length=50)
    choiceThree = models.CharField(max_length=50)
    choiceFour = models.CharField(max_length=50)
    creator = models.ForeignKey(User, null=True)
    createTime = models.DateTimeField(null=True)


class SectionBase(models.Model):
    questionCount = models.IntegerField(default=0)
    questionBases = models.ManyToManyField(QuestionBase)
    creator = models.ForeignKey(User, null=True)
    createTime = models.DateTimeField(null=True)


class FormBase(models.Model):
    sectionCount = models.IntegerField(default=0)
    sectionBases = models.ManyToManyField(SectionBase)
    creator = models.ForeignKey(User, null=True)
    createTime = models.DateTimeField(null=True)


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
    questions = models.ManyToManyField(Question)
    sectionFinished = models.BooleanField(default=False)


class Form(models.Model):
    sectionCount = models.IntegerField(default=0)
    sections = models.ManyToManyField(Section)
    formFinished = models.IntegerField(default=False)
    rater = models.ForeignKey(User, null=True)
    finishTime = models.DateTimeField(null=True)

'''
class Apply(models.Model):
    form_id = models.IntegerField()
    trainee = models.ForeignKey(User)
    applyTime = models.DateTimeField()
    isHandled = models.BooleanField(default=False)
    finishTime = models.DateTimeField()
    type = models.TextField()
'''
