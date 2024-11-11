from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import Game, Buyer, Post
from django.core.paginator import Paginator
# Create your views here.

#~~~~~~~~~~~~~~~ПАГИНАЦИЯ~~~~~~~~~~~~~~~~~~
def postForum(request):
    posts = Post.objects.all().order_by('-created_at')
    items_per_page = request.GET.get('items_per_page', 3)  # Значение по умолчанию - 3
    try:
        items_per_page = int(items_per_page)
    except ValueError:
        items_per_page = 3
    paginator = Paginator(posts, items_per_page)  # сколько на странице влезет постов
    page_number = request.GET.get('page')  # вытаскиваем страницу на которой находится пользователь
    page_obj = paginator.get_page(page_number)  #  полкчает номер страницы

    return render(request, 'forum.html',
                  {'page_obj': page_obj, 'items_per_page': items_per_page})


#~~~~~~~~~~~~~~~ОТОБРАЖЕНИЕ СТРАНИЦ~~~~~~~~~~~~~~~~~~
def webpage_homepage(request):
    context = {

    }
    return render(request, "homepage.html", context)

def webpage_store(request):
    games = Game.objects.all()
    context = {
        'games': games,
    }
    return render(request, "store.html", context)

def webpage_cart(request):
    return render(request, "cart.html")

#~~~~~~~~~~~~~~~РЕГИСТРАЦИЯ НА ДЖАНГО~~~~~~~~~~~~~~~~~~
def sign_up_by_django(request):
    info = {}
    form = UserRegister()

    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            # Обработка данных формы
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            else:
                # Ставим флаг для проверки есть ли пользователь
                user_exists = False
                for buyer in Buyer.objects.all():
                    if buyer.name == username:
                        user_exists = True
                        break  # Выходим из цикла, если нашли совпадение

                if user_exists:
                    info['error'] = 'Пользователь уже существует'
                else:
                    # Создаем нового покупателя
                    Buyer.objects.create(name=username, balance=0.0, age=age)  # баланс можно установить по умолчанию
                    info['message'] = f"Приветствуем, {username}!"
        else:
            info['error'] = 'Пожалуйста, исправьте ошибки в форме.'

    info['form'] = form
    return render(request, 'registration_page.html', info)