from multiprocessing import context
import re
from tokenize import Name
from django.contrib.auth.forms import UserCreationForm
from turtle import isvisible
from unicodedata import name
from django.shortcuts import get_object_or_404, redirect, render #biz olusturduk
from engineerapp.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from engineerapp.forms import *
from .filters import *
from django.forms import inlineformset_factory  #inline formset için 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

#burası sayfada kullanacağın fonksiyonları yazdığın sayfa
#fonksiyonlarda genelde modellerden objeleri çekersin ve en son renderda request,'görüneceği sayfa' ve çektiğin objelerle returnlersin
#methodun POST olması bu fonksiyonun linkle bir yerlere gidip gitmeyeceğiyle alakalı sanırım ?


usercreated = False

def doesitcreated(x):   #if user created we call this function with parameter 1, and it makes usercreated True
    global usercreated
    if x == 1:
        usercreated = True
    else:   #else make it false
        usercreated = False

def mainPage(request):  #home page for guests
    return render(request,'home.html',{})

@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def userhome(request):  #home page for users I split them because their navbars are different. I prevent some kind of unwanted things for doing this.
    return render(request,'userhome.html',{})


@unauthenticated_user
def registerPage(request): #UserCreationForm imported
    #form = UserCreationForm()        #that was defaulted form, to shape it as we want we create a form in forms.py
    form = UserForm()
    if request.method == "POST":    
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  #similar to other forms saving process
            username = form.cleaned_data.get('username')    #calling the username, cleaned_data is for reducing the errors.
            group = Group.objects.get(name='engineer')  #calling the engineer group
            user.groups.add(group)      #thanks to this, whenever a user is created it automatically become an engineer.
            EngModel.objects.create(
                user=user,  #there wasn't enough user_id in my database therefore I add 100 user_id manually, if it exceed that they will be an error.
                ) #this is for OneToOneField in EngModel, it creates a user for this model.
            #logeduser= authenticate(request, user)
            #login(request, logeduser)
            #return redirect('engineerapp:loginPage')
            doesitcreated(1)    #because we create user we call that function with 1
            messages.success(request, 'User ' + username + ' created successfully! ')      
            return redirect('engineerapp:loginPage')    #it redirects to the login page

    context={'form':form}
    return render(request,'register.html',context)


@unauthenticated_user
def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
            
        user = authenticate(request, username=username, password=password)  #it checks whether thee user is valid
        
        if user is not None:    #if there exist a user in database  
            login(request, user)    #it logs in, because its name is login I created that function name different from that.
            if (usercreated):   #if it's created now, first name its engineer object
                doesitcreated(0)      #because we use creation we make it false again
                return redirect('engineerapp:editEngineer')
            else:               #else redirect to the home (User) page
                return redirect('engineerapp:home')
        else:
            messages.info(request, 'username or password is incorrect!')

    context={}
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request) #it logs out.
    return redirect('engineerapp:loginPage')    #it redirects to the loginPagee, bunu navbara ekledik
    #ama user loginlemediğinde de navbarda anonymous çıkıyor ve logout oluyor bunun olmasını istemiyoruz
    #bu yüzden girebilmek için login gerekli yerler yapacağız @ ile functionın üstünde login çıkacak

@login_required(login_url='engineerapp:loginPage')  #only the user can see that page, guest cannot see this page.
@allowed_users(allowed_groups=['engineer',])    #only a user that has a group engineer can see the user page other group users cannot see this page.
def UserPage(request):   
    currEngineer = request.user.engmodel    #because there was a 1-1 relationship between user and engmodel, it calls the engineer from the user.
                                            #however, the modelname should be lower case.
    englps = currEngineer.englpmodel_set.all() 
    englpsteps = currEngineer.englpstepmodel_set.all() 
    accreditations = currEngineer.accreditationmodel_set.all()
    lpcount = englps.count()   
    lpstepcount = englpsteps.count() 
    context={'engineer':currEngineer, 'LP':englps, 'LPStep':englpsteps,'LP_count':lpcount,'LPStep_count':lpstepcount,'accreditations':accreditations}
    return render(request,'user.html',context)

#önce logine bakar sonra allowed usera bakar o yüzden bu sırayla
#@login_required(login_url='engineerapp:loginPage')  #login olmadan girememek için yoksa anonymoususer çıkar, bunu her girebildiğimiz urle yapacağız
@send_userpage  #that function defines in decorators, basically it redirects engineer group user to the user-page, it allows the admin to view that page
def home(request):
    engineers=EngModel.objects.all() #it's getting all engineers
    engineerLp = EngLPModel.objects.all()  #it's getting all engineer learning paths
    engineerLPSteps = EngLPStepModel.objects.all() #it's getting all engineers learning path steps
    accs = AccreditationModel.objects.all()
    context = {"data":engineers,"EngLP":engineerLp,"EngLPSteps":engineerLPSteps, "accs":accs} #give them a name to use those in html file
    return render(request,'index.html',context)



@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def engineer(request, pk):  #request and pk parameters we used pk as the engineers id
    currEngineer = EngModel.objects.get(engineer_id = pk) #find the current engineer whose id is equal to pk
    englps = currEngineer.englpmodel_set.all() #that's a special function which gets all learningpaths of the currentEngineer
    englpsteps = currEngineer.englpstepmodel_set.all() #it's like the englps
    lpcount = englps.count()    #it counts the englps
    lpstepcount = englpsteps.count() #it counts the englpsteps
    LearningPathFilter = LPFilter(request.GET, queryset=englps)     #it defined in filter.py 
    #request.GET is necessary for this function, querysetse bu tüm objelerin 
    #filter is defined which function(page) that will be used, you specify which fields to be filtered in filter.py
    englps = LearningPathFilter.qs  #thanks to this only the filtered datas can be shown in page.

    context = {'engineer':currEngineer, 'LP':englps, 'LPStep':englpsteps,'LP_count':lpcount,'LPStep_count':lpstepcount,
     'LPFilt':LearningPathFilter}
    return render(request, 'engineer.html', context)

            
#@login_required(login_url='engineerapp:loginPage')
#@allowed_users(allowed_groups=['admin',]) 
def showlearningpaths(request): #it shows the learning paths and learning path steps
    lp=LPModel.objects.all()
    lps = LPStepsModel.objects.all()
    context = {"LPvalues":lp, "LPSteps":lps}
    return render(request, 'LP.html', context )

def notuserlp(request): #it shows the learning paths and learning path steps
    lp=LPModel.objects.all()
    lps = LPStepsModel.objects.all()
    context = {"LPvalues":lp, "LPSteps":lps}
    return render(request, 'notuserLP.html', context )

#@login_required(login_url='engineerapp:loginPage')
#@allowed_users(allowed_groups=['admin',]) 
def showLPsteps(request):
    showall=LPStepsModel.objects.all()
    return render(request, 'LPSteps.html', {"LPSteps":showall} )

def notuserLPsteps(request):
    showall=LPStepsModel.objects.all()
    return render(request, 'notuserLPS.html', {"LPSteps":showall} )

@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def insertEngineer(request):    #that function is for creating an engineer, I didn't make it with forms because I didn't learn it when I create this func.
    if request.method=="POST":     #I keep this because it's a good remainder for me to creating an object without form.
        if request.POST.get('name') :    # if it has a name
            saverecord=EngModel()   
            saverecord.name=request.POST.get('name')    #gets the name
            saverecord.save()    #and save it successfully!
            return redirect('/') #whenever an engineer created it returns to the home page
    return render(request,'insert.html',{})

@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def updateEngineer(request,engineer_id):    #it's for admin, we will delete it once we finish the project
    updateEng = EngModel.objects.get(engineer_id=engineer_id)
    form = EngForms(instance=updateEng) 
    currUser = request.user
    if request.method == "POST":
        form = EngForms(request.POST,instance=updateEng) 
        if form.is_valid(): 
            form.save()
            return redirect('/')
    context = {"engineer":updateEng, "user":currUser, "form":form}
    return render(request,'editengineer.html',context) 

def editEngineer(request):  #this is for users, it customizes engineer object of the users.
    currEngineer = request.user.engmodel
    currUser = request.user
    UserQS = User.objects.filter(id = currUser.id)
    form = EngForms(instance=currEngineer,initial={'user':currUser})
    form.fields['user'].queryset = UserQS
    if request.method == "POST":
        form = EngForms(request.POST, instance=currEngineer, initial={'user':currUser})
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"engineer":currEngineer, "user":currUser, "form":form}
    return render(request,'editengineer.html',context) 
    #return HttpResponse('user id: ' + str(userid))


@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def deleteEngineer(request,engineer_id):
    deletedEngineer = EngModel.objects.get(engineer_id=engineer_id)
    if request.method == "POST":
        deletedEngineer.delete()
        return redirect('/')
    context = {'item':deletedEngineer}
    return render(request, 'delete.html', context)

@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def createEngLP(request,pk):   #its functions are similar to createEngLPS so I explained most of them in there.
    #LPformset = inlineformset_factory(EngModel,EngLPModel,EngLPForms,fields=('learningpath',),extra = 1)
    #it creates a form set with given parameters , <ParentModelName>, <ModelName> <FormName> , <fields to seen>, <how many form created>
    
    currEng = EngModel.objects.get(engineer_id = pk)
    EngQS = EngModel.objects.filter(engineer_id = pk)
    selectedlp = currEng.englpmodel_set.all()   #queryset of learning paths that selected by current engineer.
    all_lp = LPModel.objects.all()
    selectablelp = []
    for lp in all_lp:
        if (str(lp) not in str(selectedlp)):
            selectablelp.append(lp)
    qsselectable = LPModel.objects.filter(description__in = selectablelp)
    form = EngLPForms(initial={'engineer':currEng})
    form.fields['learningpath'].queryset = qsselectable
    form.fields['engineer'].queryset = EngQS
    #formset = LPformset(queryset=EngLPModel.objects.none(),instance=currEng)
    #to see only the empty forms we have a queryset parameter , the second one is to know currEnginer
    if request.method == "POST":
        #formset = LPformset(request.POST, instance=currEng) #to save it with an instance
        form = EngLPForms(request.POST,initial={'engineer':currEng})
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER')) #that function means refresh the page, it returns to the same page

    context = {'form':form, 'engineer':currEng}
    return render(request, 'engLP.html',context)

@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def deleteEngLP(request,pk):
    currEngLP = EngLPModel.objects.get(englp_id = pk)   #current Engineer Learning Path
    currLP = currEngLP.learningpath     #current Learning Path of the Engineer Learning Path
    LPsteps = currLP.englpstepmodel_set.all()  #Steps of Learning Path in EngLPStep Model if it was LPStep Model, then it deletes every Step of Learning Path from database
    if request.method == "POST":
        currEngLP.delete()
        for lps in LPsteps: #whenever deleting a engineer's learning path, it deletes its steps as well.
            lps.delete()
        return redirect('/')    
    context = {'item':currEngLP}
    return render(request,'deleteEngLP.html',context)


@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def createEngLPS(request,pk,lpk):
    currEng = EngModel.objects.get(engineer_id = pk)
    EngQS = EngModel.objects.filter(engineer_id = pk)  #a query set that only contains current engineer, in that way we can choose only currentEngineer in form
    currLP = LPModel.objects.get(learningpath_id = lpk)
    LPQS = LPModel.objects.filter(learningpath_id = lpk)
    lpsteps = currLP.lpstepsmodel_set.all() #lpstep model queryset that contains it's all steps
    lps = currLP.englpstepmodel_set.all()   #englpstep model queryset that contains all child of learning path, it's needed for contrasting.
    selectedlps = currEng.englpstepmodel_set.all()
    selectablelps = []
    for steps in lpsteps:
        if (str(steps) in str(selectedlps)):    #because type was not str, it doesn't operate correctly so I check whether it contains str type of steps
            pass
        else:
            selectablelps.append(steps)
    qsselectable = LPStepsModel.objects.filter(name__in = selectablelps)    #it's a function that convert list to queryset
    remain_lps = len(selectablelps)  #it gives the number of remaining steps
    mess = ""
    if (remain_lps > 1):
        mess = "There are " + str(remain_lps) + " steps to complete the learning path!"
    elif (remain_lps == 1):
        mess = "There are " + str(remain_lps) + " step to complete the learning path!"
    else:
        mess = "Congratulations, you complete the learning path! Please wait to be approved by the advisor."
    #Model = key's model in list, <...>__in is field of that key in the model.
    form = EngLPStepForms(initial={'engineer':currEng, 'learningpath':currLP})
    #form.fields['lp_step'].choices = [(lps, lps) for lps in lpsteps]   #that causes a valid choose problem.
    #form.fields modifies the fields, thanks to this only the relevant lp_steps can be choosen
    form.fields['lp_step'].queryset = qsselectable  #it only contains options that hasn't been selected yet.
    form.fields['engineer'].queryset = EngQS    #similar to upper one.
    form.fields['learningpath'].queryset = LPQS
    if request.method == "POST":
        form = EngLPStepForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    
    context = {'form':form, 'engineer':currEng, 'learningpath':currLP, 'lp_step':lpsteps, "message": mess}
    return render(request, 'EngLPStep.html',context)


@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin','engineer']) 
def deleteEngLPStep(request,pk):
    currLP = EngLPStepModel.objects.get(englpstep_id = pk)  
    if request.method == "POST":
        currLP.delete()
        return redirect('/')    
    context = {'item':currLP}
    return render(request,'deleteEngLPStep.html',context)


@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin',]) 
def createAcc(request,pk,lpk):
    currEng = EngModel.objects.get(engineer_id = pk)
    EngQS = EngModel.objects.filter(engineer_id = pk)  
    currLP = LPModel.objects.get(learningpath_id = lpk)
    currMIP = currLP.mip
    MIPQS = MIPModel.objects.filter(mip_id = currMIP.mip_id)
    lpsteps = currLP.lpstepsmodel_set.all() #lpstep model queryset that contains it's all steps
    selectedlps = currEng.englpstepmodel_set.all()
    selectablelps = []
    for steps in lpsteps:
        if (str(steps) not in str(selectedlps)): 
            selectablelps.append(steps)
    
    remain_lps = len(selectablelps)
    mess = ""
    if (remain_lps > 1):
        mess = "There are " + str(remain_lps) + " steps to complete " + str(currLP.description) + ". No need to give accreditation to " + str(currEng.name)
    elif (remain_lps == 1):
        mess = "There are " + str(remain_lps) + " step to complete " + str(currLP.description) + ". No need to give accreditation to " + str(currEng.name)
    else:
        mess = str(currEng.name) +" completed " + str(currLP.description) + ". Please give " + str(currEng.name) +" accreditation"
    form = AccForm(initial={'engineer':currEng, 'mip':currMIP})
    form.fields['engineer'].queryset = EngQS    #similar to upper one.
    form.fields['mip'].queryset = MIPQS
    if request.method == "POST":
        form = AccForm(request.POST ,initial={'engineer':currEng, 'mip':currMIP})
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))
    
    context = {'form':form, 'engineer':currEng, "message": mess}
    return render(request, 'accreditation.html',context)

@login_required(login_url='engineerapp:loginPage')
@allowed_users(allowed_groups=['admin',]) 
def deleteAcc(request,pk):
    currAcc = AccreditationModel.objects.get(acc_id = pk)   #current Engineer Learning Path
    if request.method == "POST":
        currAcc.delete()
        return redirect('/')    
    context = {'acc':currAcc}
    return render(request,'deleteAcc.html',context)
