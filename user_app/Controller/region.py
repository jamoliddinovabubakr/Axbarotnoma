from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import Region
from user_app.forms import CreateRegionForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def get_regions(request):
    regions = Region.objects.all()
    context = {
        'regions': regions
    }
    return render(request, "user_app/settings/region_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def create_region(request):
    if request.method == "POST":
        form = CreateRegionForm(request.POST)
        if form.is_valid():
            region = form.save(commit=False)
            region.save()
            return redirect('regions')
    else:
        context = {
            'form': CreateRegionForm(),
        }
        return render(request, 'user_app/crud/add_region.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def edit_region(request, pk):
    region = get_object_or_404(Region, pk=pk)
    if request.method == 'POST':
        form = CreateRegionForm(request.POST, instance=region)
        form.save()
        return redirect('regions')

    else:
        form = CreateRegionForm(instance=region)
        return render(request, 'user_app/crud/edit_region.html', {"region": region, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['MASTER', 'ADMIN'])
def delete_region(request, pk):
    region = get_object_or_404(Region, pk=pk)
    if request.method == "POST":
        region.delete()
        return redirect('regions')
    else:
        return render(request, 'user_app/crud/delete_region.html', {'region': region})
