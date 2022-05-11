from user_app.Controller.user import *
from user_app.Controller.register import *
from user_app.Controller.menu import *
from user_app.Controller.gender import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Users'])
# @admin_only
def profile_page(request):
    context = {

    }
    return render(request, "user_app/cabinet_page.html", context=context)


@login_required(login_url='login')
def profile(request):
    context = {

    }
    return render(request, "user_app/profile_page.html", context=context)


@login_required(login_url='login')
def roles(request):
    roles = Role.objects.filter(status=True)
    context = {
        'roles': roles
    }
    return render(request, "user_app/settings/roles_page.html", context=context)


@login_required(login_url='login')
def districts(request):
    districts = District.objects.all()
    context = {
        'districts': districts
    }
    return render(request, "user_app/settings/district_page.html", context=context)


@login_required(login_url='login')
def regions(request):
    regions = Region.objects.all()
    context = {
        'regions': regions
    }
    return render(request, "user_app/settings/region_page.html", context=context)


@login_required(login_url='login')
def handler404(request, exception):
    return render(request, 'user_app/error_404.html')
