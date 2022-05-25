from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import District
from user_app.forms import CreateDistrictForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_districts(request):
    districts = District.objects.all()
    context = {
        'districts': districts
    }
    return render(request, "user_app/settings/district_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def create_district(request):
    if request.method == "POST":
        form = CreateDistrictForm(request.POST)
        if form.is_valid():
            district = form.save(commit=False)
            district.save()
            return redirect('districts')
    else:
        context = {
            'form': CreateDistrictForm(),
        }
        return render(request, 'user_app/crud/add_district.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def edit_district(request, pk):
    district = get_object_or_404(District, pk=pk)
    if request.method == 'POST':
        form = CreateDistrictForm(request.POST, instance=district)
        form.save()
        return redirect('districts')

    else:
        form = CreateDistrictForm(instance=district)
        return render(request, 'user_app/crud/edit_district.html', {"district": district, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_district(request, pk):
    district = get_object_or_404(District, pk=pk)
    if request.method == "POST":
        district.delete()
        return redirect('districts')
    else:
        return render(request, 'user_app/crud/delete_district.html', {'district': district})
