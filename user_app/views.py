from user_app.Controller.user import *
from user_app.Controller.register import *
from user_app.Controller.menu import *
from user_app.Controller.gender import *
from user_app.Controller.role import *
from user_app.Controller.state import *
from user_app.Controller.region import *
from user_app.Controller.district import *
from user_app.Controller.notification import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'USER', 'BOSH MUHARRIR', 'MASUL KOTIB', 'TAHLILCHI'])
# @admin_only
def profile_page(request):
    context = {}
    return render(request, "user_app/cabinet_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN', 'USER', 'BOSH MUHARRIR', 'MASUL KOTIB', 'TAHLILCHI'])
def profile(request):
    context = {

    }
    return render(request, "user_app/profile_page.html", context=context)


@login_required(login_url='login')
def handler404(request, exception):
    return render(request, 'user_app/error_404.html')
