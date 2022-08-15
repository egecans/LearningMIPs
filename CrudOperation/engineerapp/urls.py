from django.urls import path
from . import views

#bir appteysen appin adını giriyorsun, eğer ana appin altında bir appse de her hrefte önce app adı : <url name> kullanıyorsun
app_name = 'engineerapp'

#viewsta yazdığın fonksiyonlar için url düzenliyorsun
#sayfaya gidip bu fonksiyonları kullandığında pathin ilk parametresine gönderiyor bulunduğun adresten
#eğer herkes için aynıysa normal url yapıyorsun ama objeden objeye değişiyorsa /<int <views parametre adı> > yapıp dynamic url oluşturuyorsun
#3. parametre ise hrefte çağırdığında url pathini yazma diye unique bir isim koyuyorsun, htmlde hrefte {% %} arasına o isimle çağırabiliyorsun
#ve bu sayede dynamicleşiyor, bir şeyleri değiştirsen de url kısmında ismi aynı olduğundan her kullandığın templeteı da değiştirmene gerek kalmıyor
urlpatterns = [
    path('',views.home,name="home"), #name sayesinde bir şeyler değişse de templateta değiştirmene gerek kalmıyor daha dynamic oluyor
    path('engineer/<int:pk>',views.engineer,name='engineer'),
    path('insertEngineer/',views.insertEngineer,name='insertEngineer'), #ilki yukarıdaki linkin adı
    #<int: ya da <str dynamic yapıyor urli kişiye özgü oluyor yani edit/1 edit/2 gibi
    path('update/<int:engineer_id>',views.updateEngineer,name="updateEngineer"),
    path('delete/<int:engineer_id>',views.deleteEngineer,name="delete"),
    path('showLPs/',views.showlearningpaths, name="showlearningpaths"),  #yukarıdaki linkte yazan şey localhost .../showLPs/ gibi ilk parametre 
    path('showLPSteps/',views.showLPsteps, name="showLPsteps"), 
    path('createEngineerLearningPath/<str:pk>',views.createEngLP,name='createEngLP'),
    path('deleteEngineerLearningPath/<str:pk>',views.deleteEngLP,name='deleteEngLP'), 
    #{% url %} li kullanıyorsan name'i ile href =" "... diyorsan ilk parametreyle çağırıyorsun
    path('deleteEngineerLearningPathStep/<str:pk>',views.deleteEngLPStep,name='deleteEngLPStep'),

    path('register/',views.registerPage,name='registerPage'),
    path('login/',views.loginPage,name='loginPage'),
    path('logout/',views.logoutUser,name='logout'),
    path('user/',views.UserPage,name='user-page') ,
    path('createEngLPS/<str:pk>/<str:lpk>',views.createEngLPS,name='createEngLPS'),
    path('home/',views.mainPage,name="mainPage"),
    path('edit/', views.editEngineer, name="editEngineer"),
    path('accreditation/<str:pk>/<str:lpk>',views.createAcc, name="createAccreditation"),
    path('deleteAccreditation/<str:pk>',views.deleteAcc,name="deleteAcc"),
    path('LearningPaths',views.notuserlp,name="notuserlp"),
    path('LearningPathSteps',views.notuserLPsteps,name="notuserLPsteps"),
    path('Home/',views.userhome,name="userhome"),
]