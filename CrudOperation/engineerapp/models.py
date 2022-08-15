import imp
from operator import mod
from pyexpat import model
from sys import implementation
from unicodedata import name
from django.db import models    #biz olusturduk
from django.forms import CharField
from django.contrib.auth.models import User

#model databaselerle alakalı dbn yoksa django kendi yapıyor sanırım varsa da bağlanıp oradan table seçiyorsun
#modelde bir şey değiştirince makemigrations, classı changeleyince migrate sanırım
#migrate table ı database e ekliyor ?
class EngModel(models.Model):   
    engineer_id = models.AutoField(primary_key=True)    #id primary key olduğundan kendi vercek böyle girdi
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    class Meta:
        db_table="engineers"
        ordering = ("engineer_id","name")
    def __str__(self):  #çağrıldığında MIP object değil ismiyle gözüksün diye 
        return self.name

class MIPModel(models.Model):
    mip_id = models.AutoField(primary_key=True)
    mip_name = models.CharField(max_length=150)
    class Meta:
        db_table="mips"
    def __str__(self):  #çağrıldığında MIP object değil ismiyle gözüksün diye 
        return self.mip_name

class AccreditationModel(models.Model):
    acc_id = models.AutoField(primary_key=True)
    engineer = models.ForeignKey(EngModel, null=True, on_delete = models.CASCADE)
    mip = models.ForeignKey(MIPModel, null=True, on_delete = models.CASCADE)
    class Meta:
        db_table = "engineer_acccreditations"
    def __str__(self):  #çağrıldığında MIP object değil ismiyle gözüksün diye 
        return self.mip.mip_name

class LPModel(models.Model):
    learningpath_id = models.AutoField(primary_key=True)
    #ilki aldığı Model, sonuncuya kadar aradakiler attribute null=True girmeyi unutsa da kabul et demek
    #sonuncuysa parentı silindiğinde ne olsun demek,    models.SET_NULL da diyebilirsin boş kalır böylece parentı
    #CASCADE ise parent silinince childı da sil demek
    mip = models.ForeignKey(MIPModel, blank=True, null=True, on_delete=models.CASCADE)  #ismi mip çünkü mipten mip_id alıyor sonra 
    #learningpaths.mip_id_id does not exist hatası veriyor

    description = models.CharField(max_length=150)
    class Meta:
        db_table="learningpaths"
        ordering = ("learningpath_id","description")

    def __str__(self):      #sonra bunu çağırdığımızda ismi gözükecek object olarak gözükmeyecek.
        return self.description

class LPStepsModel(models.Model):
    lp_step_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    learningpath = models.ForeignKey(LPModel, null=True, on_delete=models.CASCADE) #null true vardı girmesen de kabul blank true boş girebilirsin demek
    class Meta:
        db_table="learningpathsteps"
        ordering = ("learningpath_id", "lp_step_id")
    def __str__(self):
        return self.name

class EngLPModel(models.Model):
    engineer = models.ForeignKey(EngModel, null=True, on_delete = models.CASCADE)
    learningpath = models.ForeignKey(LPModel, null=True, on_delete=models.CASCADE)
    englp_id = models.AutoField(primary_key=True)
    class Meta:
        db_table = "engineer_learning_paths"
        #ordering = ("engineer","learningpath")
    def __str__(self):
        return self.learningpath.description

class EngLPStepModel(models.Model):
    englpstep_id = models.AutoField(primary_key=True)
    engineer = models.ForeignKey(EngModel, null=True, on_delete = models.CASCADE)
    lp_step = models.ForeignKey(LPStepsModel, null=True,  on_delete=models.CASCADE)
    completed = models.BooleanField(db_index=True ,default=True)   #default true because if we add that step we should complete it necessarily.
    learningpath = models.ForeignKey(LPModel, null=True, on_delete=models.CASCADE)
    class Meta:
        db_table = "lpstepcompletions"
        #ordering = ("engineer","lp_step")
    def __str__(self):
        return self.lp_step.name
