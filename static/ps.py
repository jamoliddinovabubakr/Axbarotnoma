def search_author(request):
    q = request.GET.get('author_email', None)
    is_have_author = User.objects.filter(email=q).exists()

    if is_have_author:
        data = {
            'is_have_author': 1, 'email': q
        }
    else:
        data = {
            'is_have_author': 0, 'email': q
        }
    return JsonResponse(data)


def add_exist_author(request, pk):
    print(request.POST)
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        email = request.POST.get('exist_author_email', None)
        user = User.objects.get(email=email)
        author = Author.objects.get(user=user)
        article.authors.add(author)
        return JsonResponse({'message': "Author added successfully!"})
    else:
        return JsonResponse({'message': 'Author didnt add!'})


