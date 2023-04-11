from django.shortcuts import render, redirect, get_object_or_404
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
from django.db.models import Q

model_to_dict(Post)


class UserHome(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # datas = Post.objects.filter(author=request.user.email)
            # datas = Post.objects.filter(user_name_id=request.user) 只尋找目前登入的使用者
            datas = Post.objects.all()
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
        # 全部都可以看
        datas = Post.objects.get(pk=get_id)
        # 限定登入的作者才可以看
        # datas = Post.objects.get(author=request.user, pk=get_id)
        # datas = request.user.post_set.get(pk=get_id)

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
    data = Post.objects.create(
        title=title, content=content, photo=photo, location=location)
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
        response = HttpResponse(
            '<script>alert("刪除成功"); window.location.href="/home";</script>')
        return response
    except Post.DoesNotExist:
        return HttpResponse("沒有這個資料可以刪除")


@login_required(login_url="login")
@csrf_exempt
def edit_test(request, get_id):
    try:
        datas = Post.objects.get(pk=get_id)
        data_dict = {
            'id': datas.id,
            'author': datas.author,
            'create_at': datas.created_at,
            'title': datas.title,
            'content': datas.content,
            'photo': datas.photo,
            'location': datas.location,
        }
        return render(request, 'user/edit_article.html', data_dict)
    except Post.DoesNotExist:
        return HttpResponse("無法搜尋到資料")


@login_required(login_url="login")
@csrf_exempt
def save_data(request, mode_id):

    if request.method == "POST":
        # 取得 POST 資料並進行驗證
        title = request.POST.get('title')
        content = request.POST.get('content')
        photo = request.POST.get('photo')
        location = request.POST.get('location')
        if not title or not content:
            return HttpResponse("請填寫標題和內容")

        # 取得 Post 物件並更新資料
        data = get_object_or_404(Post, id=mode_id)
        data.title = title
        data.content = content
        data.photo = photo
        data.location = location
        data.save()

        new_id = data.id
        response = HttpResponse(
            '<script>alert("儲存成功"); window.location.href="/user/{}";</script>'.format(new_id))
        return response
    else:
        return HttpResponse("請選擇 POST 進行建立")


@login_required(login_url="login")
@csrf_exempt
def search(request):
    keyword = request.GET.get('query') # 讀取 URL 中的搜尋關鍵字
    if keyword: # 如果有搜尋關鍵字
        datas = Post.objects.filter(Q(title__icontains=keyword) | Q(author__icontains=keyword))
        if datas: # 如果找到搜尋結果
            # 使用 Q 物件進行 OR 邏輯的模糊搜尋，可以搜尋 title 或 author 中包含關鍵字的文章
            return render(request, 'index.html', {'datas': datas})
        else: # 如果找不到搜尋結果
            # 在 index.html 模板中顯示錯誤訊息
            return render(request, 'index.html', {'error_message': '找不到相符的內容'})
    else:
        # 在 index.html 模板中顯示錯誤訊息
        return render(request, 'index.html', {'error_message': '請輸入要搜尋的文章或作者'})


# class work_view_set(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = work_serializer
#
# class get_set(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = work_serializer
#     renderer_classes = (BrowsableAPIRenderer, JSONRenderer,)
#     http_method_names = ('GET',)
