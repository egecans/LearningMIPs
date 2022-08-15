from tokenize import group
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

#bu classta içinde conditionlar var mesela functionın onları her birine tek tek yazmayıp üzerine @ ile bunu çağırıyorsun ve o işi yapıyor
#mesela burada amaç eğer user girdiyse tekrar login ya da register page e gitmesini istemiyoruz logout olmadan o yüzden bunları o view func üstünde çağırcaz
#view_func çağırdığın function adı, wrapperda ise normalde viewun içinde yapmasını istediğin condition
#bu fonksiyondan önce biz de viewsda aynısını yapıyorduk.
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('engineerapp:home')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

#adminde gruplar açtık, burada functionını yazdık eğer grup alloweddaysa belirlenen sayfaları görür, değilse göremez.
#grubun ne olduğunuysa viewfunctionda giriyoruz, burada boş bırakıyoruz böylece daha dynamic oluyor yapı.
def allowed_users(allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():    #eğer userın bir grubu varsa
                group = request.user.groups.all()[0].name   #ilk grubun ismine göre değerlendiriyoruz

            if group in allowed_groups: #eğer istenen gruptaysa view functionı çalıştırıyoruz, 
                return view_func(request, *args, **kwargs)
            else:                       #değilse bu sayfayı göremezsiniz diyoruz.
                return HttpResponse('You are not authorized to view this page! Please sign up first! You can go to home Page from navbar and click to the Join Us!')
        return wrapper_func #bu da bir içe girer ve en içtekini çalıştırır
    return decorator    #en dıştaki bir içe


#dynamic olmasına gerek yok, gruplarım belli diyorsan bu fonksiyon da aynı işe yarar.
def send_userpage(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():    #eğer userın bir grubu varsa
            group = request.user.groups.all()[0].name   #ilk grubun ismine göre değerlendiriyoruz

        if group == 'engineer':
            return redirect('engineerapp:user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            #messages.info(request, 'You are not a participant of a valid group! Please sign into engineer or admin group!')
            return redirect('engineerapp:mainPage')    #logout edip login page'e gönderir mesajla birlikte.


    return wrapper_func