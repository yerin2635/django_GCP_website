from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from home.models import Post, Account
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from home.serializers import work_serializer
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .forms import RegisterForm, UserLoginForm, CreateArticle
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

model_to_dict(Post)


class UserHome(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # datas = Post.objects.filter(author=request.user.email)
            datas = Post.objects.filter(user_name_id=request.user)
            return render(request, 'index.html', {'datas': datas})
        else:
            return render(request, 'index.html')


class RegisterView(TemplateView):
    template_name = 'login/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'login/register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'login/register.html', {'form': form})


class UserLogin(TemplateView):
    template_name = 'login/login.html'

    def get(self, request, *args, **kwargs):
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'login/login.html', context)

    def post(self, request):
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(email=data['email'], password=data['password'])
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "帳號密碼輸入有誤，請重新輸入")
                return redirect('login')
        else:
            messages.error(request, "帳號或密碼未輸入，請重新輸入")
            return redirect('login')


class UserLogout(TemplateView):
    template_name = 'login/login.html'

    def get(self, request):
        logout(request)
        return redirect('login')


class UserAddArticle(TemplateView):
    template_name = 'user/add_article.html'

    def get(self, request, *args, **kwargs):
        form = CreateArticle(request.POST)
        context = {'form': form}
        return render(request, 'user/add_article.html', context)

    def post(self, request):
        form = CreateArticle(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_name_id = request.user.id
            instance.author = request.user
            instance.save()
            return redirect('home')


class GetAllData(ListView):
    def get(self, request):
        data = list(Post.objects.values())
        return JsonResponse(data, safe=False)


def get_posts_choose(request, get_id):
    try:
        # data = Post.objects.get(pk=get_id)ㄥ
        # datas = Post.objects.get(author=request.user, pk=get_id)
        datas = request.user.post_set.get(pk=get_id)

        data_dict = {
            'id': datas.id,
            'author': datas.author,
            'create_at': datas.created_at,
            'title': datas.title,
            'content': datas.content,
            'photo': datas.photo,
            'location': datas.location,
        }
        return render(request, 'user/UserLookArticle.html', data_dict)
    except Post.DoesNotExist:
        return HttpResponse("無法搜尋到資料")


@login_required(login_url="login")
@csrf_exempt
def create_posts(request):
    if request.method != "POST":
        return HttpResponse("請選擇POST進行建立")

    title = request.POST['title']
    content = request.POST['content']
    photo = request.POST['photo']
    location = request.POST['location']
    data = Post.objects.create(title=title, content=content, photo=photo, location=location)
    data.save()
    try:
        data = Post.objects.filter(pk=data.id).values()
        return JsonResponse({"posts": list(data)})
    except Post.DoesNotExist:
        return HttpResponse("建創失敗")


@login_required(login_url="login")
@csrf_exempt
def update_posts(request, mode_id):
    if request.method == "POST":
        return HttpResponse("請選擇POST進行建立")

    if Post.objects.filter(pk=mode_id):
        data = Post.objects.get(id=mode_id)
        data.title = request.POST['title']
        data.content = request.POST['content']
        data.photo = request.POST['photo']
        data.location = request.POST['location']
        data.save()
        try:
            data = Post.objects.filter(pk=mode_id).values()
            return HttpResponse(data, content_type="application/json")
        except Post.DoesNotExist:
            return HttpResponse("更改失敗")


@login_required(login_url="login")
@csrf_exempt
def delete_posts(request, data_id):
    try:
        data = Post.objects.get(pk=data_id)
        data.delete()
        return HttpResponse("刪除成功")
    except Post.DoesNotExist:
        return HttpResponse("沒有這個資料可以刪除")

# class work_view_set(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = work_serializer
#
# class get_set(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = work_serializer
#     renderer_classes = (BrowsableAPIRenderer, JSONRenderer,)
#     http_method_names = ('GET',)
