from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from user_app.decorators import allowed_users
from user_app.models import State
from user_app.forms import CreateStateForm


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def get_states(request):
    states = State.objects.filter(status=True)
    context = {
        'states': states
    }
    return render(request, "user_app/settings/states_page.html", context=context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def create_state(request):
    if request.method == "POST":
        form = CreateStateForm(request.POST)
        if form.is_valid():
            state = form.save(commit=False)
            state.save()
            return redirect('states')
    else:
        context = {
            'form': CreateStateForm(),
        }
        return render(request, 'user_app/crud/add_state.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def edit_state(request, pk):
    state = get_object_or_404(State, pk=pk)
    if request.method == 'POST':
        form = CreateStateForm(request.POST, instance=state)
        form.save()
        return redirect('states')

    else:
        form = CreateStateForm(instance=state)
        return render(request, 'user_app/crud/edit_state.html', {"state": state, 'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admins', 'Masters'])
def delete_state(request, pk):
    state = get_object_or_404(State, pk=pk)
    if request.method == "POST":
        state.delete()
        return redirect('states')
    else:
        return render(request, 'user_app/crud/delete_state.html', {'state': state})
