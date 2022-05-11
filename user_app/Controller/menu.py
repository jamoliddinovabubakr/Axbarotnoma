from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.models import Menu
from user_app.forms import CreateMenuForm


@login_required(login_url='login')
def get_menus(request):
    menus = Menu.objects.filter(status=True)
    context = {
        'menus': menus
    }
    return render(request, "user_app/settings/menus_page.html", context=context)


@login_required(login_url='login')
def view_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    context = {
        'menu': menu
    }
    return render(request, "user_app/crud/view_menu.html", context=context)


@login_required(login_url='login')
def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = CreateMenuForm(request.POST, instance=menu)
        form.save()
        return redirect('menus')

    else:
        form = CreateMenuForm(instance=menu)
        return render(request, 'user_app/crud/edit_menu.html', {"menu": menu, 'form': form})


@login_required(login_url='login')
def delete_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu.delete()
        return redirect('menus')
    else:
        return render(request, 'user_app/crud/delete_menu.html', {'menu': menu})
