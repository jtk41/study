from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, Achivments, UserAchivment, Order
from .forms import GameForm, AchivmentsForm, UserAchivmentForm, OrderForm

def games_page(request):
    return render(request, "index.html")

@login_required
def game_create(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = GameForm()
    
    return render(request, "game_form.html", {
        "form": form,
        "title": "Добавить игру"
    })

@login_required
def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)

    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = GameForm(instance=game)
    
    return render(request, "game_form.html", {
        "form": form,
        "game": game,
        "title": "Редактировать игру"
    })

@login_required
def achivment_create(request):
    if request.method == "POST":
        form = AchivmentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = AchivmentsForm()
    
    return render(request, "achivment_form.html", {
        "form": form,
        "title": "Добавить достижение"
    })

@login_required
def achivment_update(request, pk):
    achivment = get_object_or_404(Achivments, pk=pk)

    if request.method == "POST":
        form = AchivmentsForm(request.POST, instance=achivment)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = AchivmentsForm(instance=achivment)
    
    return render(request, "achivment_form.html", {
        "form": form,
        "achivment": achivment,
        "title": "Редактировать достижение"
    })

@login_required
def user_achivment_create(request):
    if request.method == "POST":
        form = UserAchivmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = UserAchivmentForm()
    
    return render(request, "user_achivment_form.html", {
        "form": form,
        "title": "Добавить связь пользователь-достижение"
    })

@login_required
def user_achivment_update(request, pk):
    user_achivment = get_object_or_404(UserAchivment, pk=pk)

    if request.method == "POST":
        form = UserAchivmentForm(request.POST, instance=user_achivment)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = UserAchivmentForm(instance=user_achivment)
    
    return render(request, "user_achivment_form.html", {
        "form": form,
        "user_achivment": user_achivment,
        "title": "Редактировать связь пользователь-достижение"
    })

@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = OrderForm()
    
    return render(request, "order_form.html", {
        "form": form,
        "title": "Добавить заказ"
    })

@login_required
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('games_page')
    else:
        form = OrderForm(instance=order)
    
    return render(request, "order_form.html", {
        "form": form,
        "order": order,
        "title": "Редактировать заказ"
    })