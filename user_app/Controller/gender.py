# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
#
# from user_app.decorators import allowed_users
# from user_app.models import Gender
# from user_app.forms import CreateGenderForm
#
#
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['MASTER', 'ADMIN'])
# def genders(request):
#     genderlar = Gender.objects.filter(status=True)
#     context = {
#         'genders': genderlar
#     }
#     return render(request, "user_app/settings/gender_page.html", context=context)
#
#
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['MASTER', 'ADMIN'])
# def create_gender(request):
#     if request.method == "POST":
#         form = CreateGenderForm(request.POST)
#         if form.is_valid():
#             gender = form.save(commit=False)
#             gender.save()
#             return redirect('districts')
#     else:
#         context = {
#             'form': CreateGenderForm(),
#         }
#         return render(request, 'user_app/crud/add_gender.html', context)
#
#
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['MASTER', 'ADMIN'])
# def edit_gender(request, pk):
#     gender = get_object_or_404(Gender, pk=pk)
#     if request.method == 'POST':
#         form = CreateGenderForm(request.POST, instance=gender)
#         form.save()
#         return redirect('genders')
#
#     else:
#         form = CreateGenderForm(instance=gender)
#         return render(request, 'user_app/crud/edit_gender.html', {"gender": gender, 'form': form})
#
#
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['MASTER', 'ADMIN'])
# def delete_gender(request, pk):
#     gender = get_object_or_404(Gender, pk=pk)
#     if request.method == "POST":
#         gender.delete()
#         return redirect('genders')
#     else:
#         return render(request, 'user_app/crud/delete_gender.html', {'gender': gender})
