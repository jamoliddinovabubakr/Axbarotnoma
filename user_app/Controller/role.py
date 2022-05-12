from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.models import Role
from user_app.forms import CreateRoleForm


@login_required(login_url='login')
def get_roles(request):
    roles = Role.objects.filter(status=True)
    context = {
        'roles': roles
    }
    return render(request, "user_app/settings/roles_page.html", context=context)


@login_required(login_url='login')
def create_role(request):
    if request.method == "POST":
        form = CreateRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.save()
            return redirect('roles')
    else:
        context = {
            'form': CreateRoleForm(),
        }
        return render(request, 'user_app/crud/add_role.html', context)


@login_required(login_url='login')
def edit_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = CreateRoleForm(request.POST, instance=role)
        form.save()
        return redirect('roles')

    else:
        form = CreateRoleForm(instance=role)
        return render(request, 'user_app/crud/edit_role.html', {"role": role, 'form': form})


@login_required(login_url='login')
def delete_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        role.delete()
        return redirect('roles')
    else:
        return render(request, 'user_app/crud/delete_role.html', {'role': role})
