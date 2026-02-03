from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Game, Achivments, UserAchivment, Order
from .forms import (
    GameForm, AchivmentsForm, UserAchivmentForm, 
    OrderForm, GameSearchForm, UserAchivmentStatusForm
)

# ========== Game Views ==========
def game_list(request):
    """Список всех игр с поиском и фильтрацией"""
    games = Game.objects.all()
    search_form = GameSearchForm(request.GET)
    
    if search_form.is_valid():
        name = search_form.cleaned_data.get('name')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        
        if name:
            games = games.filter(name__icontains=name)
        if min_price:
            games = games.filter(price__gte=min_price)
        if max_price:
            games = games.filter(price__lte=max_price)
    
    # Пагинация
    paginator = Paginator(games, 10)  # 10 игр на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'games_count': games.count(),
    }
    return render(request, 'games/game_list.html', context)

def game_detail(request, pk):
    """Детальная информация об игре"""
    game = get_object_or_404(Game, pk=pk)
    achievements = game.achivments.all()  # Используем related_name из модели
    context = {
        'game': game,
        'achievements': achievements,
    }
    return render(request, 'games/game_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def game_create(request):
    """Создание новой игры (только для персонала)"""
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save()
            messages.success(request, f'Игра "{game.name}" успешно создана!')
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm()
    
    context = {'form': form}
    return render(request, 'games/game_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def game_update(request, pk):
    """Редактирование игры (только для персонала)"""
    game = get_object_or_404(Game, pk=pk)
    
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, f'Игра "{game.name}" успешно обновлена!')
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm(instance=game)
    
    context = {'form': form, 'game': game}
    return render(request, 'games/game_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def game_delete(request, pk):
    """Удаление игры (только для персонала)"""
    game = get_object_or_404(Game, pk=pk)
    
    if request.method == 'POST':
        game_name = game.name
        game.delete()
        messages.success(request, f'Игра "{game_name}" успешно удалена!')
        return redirect('game_list')
    
    context = {'game': game}
    return render(request, 'games/game_confirm_delete.html', context)

# ========== Achievements Views ==========
@login_required
def achievement_list(request, game_id=None):
    """Список достижений"""
    achievements = Achivments.objects.all()
    
    if game_id:
        game = get_object_or_404(Game, pk=game_id)
        achievements = achievements.filter(game_name=game)
        context = {'achievements': achievements, 'game': game}
    else:
        context = {'achievements': achievements}
    
    return render(request, 'games/achievement_list.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def achievement_create(request, game_id=None):
    """Создание достижения (только для персонала)"""
    if game_id:
        game = get_object_or_404(Game, pk=game_id)
        initial = {'game_name': game}
    else:
        initial = {}
    
    if request.method == 'POST':
        form = AchivmentsForm(request.POST)
        if form.is_valid():
            achievement = form.save()
            messages.success(request, f'Достижение "{achievement.name_achivments}" создано!')
            return redirect('achievement_list')
    else:
        form = AchivmentsForm(initial=initial)
    
    context = {'form': form}
    return render(request, 'games/achievement_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def achievement_update(request, pk):
    """Редактирование достижения (только для персонала)"""
    achievement = get_object_or_404(Achivments, pk=pk)
    
    if request.method == 'POST':
        form = AchivmentsForm(request.POST, instance=achievement)
        if form.is_valid():
            form.save()
            messages.success(request, f'Достижение обновлено!')
            return redirect('achievement_list')
    else:
        form = AchivmentsForm(instance=achievement)
    
    context = {'form': form, 'achievement': achievement}
    return render(request, 'games/achievement_form.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def achievement_delete(request, pk):
    """Удаление достижения (только для персонала)"""
    achievement = get_object_or_404(Achivments, pk=pk)
    
    if request.method == 'POST':
        achievement_name = achievement.name_achivments
        achievement.delete()
        messages.success(request, f'Достижение "{achievement_name}" удалено!')
        return redirect('achievement_list')
    
    context = {'achievement': achievement}
    return render(request, 'games/achievement_confirm_delete.html', context)

# ========== User Achievements Views ==========
@login_required
def user_achievement_list(request):
    """Список достижений текущего пользователя"""
    user_achievements = UserAchivment.objects.filter(user_id=request.user)
    
    # Статистика
    total = user_achievements.count()
    completed = user_achievements.filter(status='done').count()
    progress = (completed / total * 100) if total > 0 else 0
    
    context = {
        'user_achievements': user_achievements,
        'total': total,
        'completed': completed,
        'progress': round(progress, 2),
    }
    return render(request, 'games/user_achievement_list.html', context)

@login_required
def user_achievement_detail(request, pk):
    """Детальная информация о достижении пользователя"""
    user_achievement = get_object_or_404(
        UserAchivment, pk=pk, user_id=request.user
    )
    
    if request.method == 'POST':
        form = UserAchivmentStatusForm(request.POST, instance=user_achievement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус обновлен!')
            return redirect('user_achievement_detail', pk=pk)
    else:
        form = UserAchivmentStatusForm(instance=user_achievement)
    
    context = {
        'user_achievement': user_achievement,
        'form': form,
    }
    return render(request, 'games/user_achievement_detail.html', context)

@login_required
def user_achievement_create(request, achievement_id=None):
    """Добавление достижения пользователю"""
    if achievement_id:
        achievement = get_object_or_404(Achivments, pk=achievement_id)
        initial = {'achivment_id': achievement}
    else:
        initial = {}
    
    if request.method == 'POST':
        form = UserAchivmentForm(request.POST)
        if form.is_valid():
            user_achievement = form.save(commit=False)
            user_achievement.user_id = request.user  # Автоматически назначаем текущего пользователя
            user_achievement.save()
            messages.success(request, 'Достижение добавлено!')
            return redirect('user_achievement_list')
    else:
        form = UserAchivmentForm(initial=initial)
    
    context = {'form': form}
    return render(request, 'games/user_achievement_form.html', context)

@login_required
def user_achievement_delete(request, pk):
    """Удаление достижения пользователя"""
    user_achievement = get_object_or_404(
        UserAchivment, pk=pk, user_id=request.user
    )
    
    if request.method == 'POST':
        user_achievement.delete()
        messages.success(request, 'Достижение удалено из вашего профиля!')
        return redirect('user_achievement_list')
    
    context = {'user_achievement': user_achievement}
    return render(request, 'games/user_achievement_confirm_delete.html', context)

# ========== Order Views ==========
@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user_id=request.user).select_related('game_id')
    
    context = {
        'orders': orders,
        'total_spent': sum(order.price for order in orders),
    }
    return render(request, 'games/order_list.html', context)

@login_required
def order_detail(request, pk):
    """Детальная информация о заказе"""
    order = get_object_or_404(Order, pk=pk, user_id=request.user)
    
    context = {'order': order}
    return render(request, 'games/order_detail.html', context)

@login_required
def order_create(request, game_id=None):
    """Создание заказа"""
    if game_id:
        game = get_object_or_404(Game, pk=game_id)
        initial = {'game_id': game, 'price': game.price}
    else:
        initial = {}
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user  # Автоматически назначаем текущего пользователя
            order.save()
            messages.success(request, f'Заказ #{order.id} успешно создан!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm(initial=initial)
    
    context = {'form': form}
    return render(request, 'games/order_form.html', context)

@login_required
def order_delete(request, pk):
    """Отмена заказа"""
    order = get_object_or_404(Order, pk=pk, user_id=request.user)
    
    if request.method == 'POST':
        order_id = order.id
        order.delete()
        messages.success(request, f'Заказ #{order_id} отменен!')
        return redirect('order_list')
    
    context = {'order': order}
    return render(request, 'games/order_confirm_delete.html', context)

# ========== Admin Views ==========
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user_achievements(request, user_id=None):
    """Админ: просмотр достижений пользователей"""
    if user_id:
        user = get_object_or_404(User, pk=user_id)
        user_achievements = UserAchivment.objects.filter(user_id=user)
        context = {'user_achievements': user_achievements, 'selected_user': user}
    else:
        user_achievements = UserAchivment.objects.all()
        context = {'user_achievements': user_achievements}
    
    return render(request, 'games/admin_user_achievements.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):
    """Админ: просмотр всех заказов"""
    orders = Order.objects.all().select_related('user_id', 'game_id')
    
    # Фильтрация по пользователю
    user_id = request.GET.get('user_id')
    if user_id:
        orders = orders.filter(user_id=user_id)
    
    context = {
        'orders': orders,
        'total_revenue': sum(order.price for order in orders),
        'users': User.objects.all(),  # Для фильтра
    }
    return render(request, 'games/admin_orders.html', context)

# ========== Dashboard Views ==========
@login_required
def dashboard(request):
    """Панель управления пользователя"""
    user = request.user
    
    # Статистика пользователя
    orders = Order.objects.filter(user_id=user)
    user_achievements = UserAchivment.objects.filter(user_id=user)
    
    context = {
        'user': user,
        'total_orders': orders.count(),
        'total_spent': sum(order.price for order in orders),
        'total_achievements': user_achievements.count(),
        'completed_achievements': user_achievements.filter(status='done').count(),
        'recent_orders': orders.order_by('-id')[:5],
        'recent_achievements': user_achievements.order_by('-id')[:5],
    }
    return render(request, 'games/dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Панель управления администратора"""
    # Общая статистика
    total_games = Game.objects.count()
    total_achievements = Achivments.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_revenue = sum(order.price for order in Order.objects.all())
    
    # Последние действия
    recent_games = Game.objects.order_by('-id')[:5]
    recent_orders = Order.objects.select_related('user_id', 'game_id').order_by('-id')[:5]
    
    context = {
        'total_games': total_games,
        'total_achievements': total_achievements,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_revenue': total_revenue,
        'recent_games': recent_games,
        'recent_orders': recent_orders,
    }
    return render(request, 'games/admin_dashboard.html', context)

# ========== Utility Functions ==========
@login_required
def buy_game(request, game_id):
    """Быстрая покупка игры (создание заказа)"""
    game = get_object_or_404(Game, pk=game_id)
    
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            game_id=game,
            user_id=request.user,
            price=game.price
        )
        messages.success(request, f'Вы успешно купили игру "{game.name}"!')
        return redirect('order_detail', pk=order.pk)
    
    context = {'game': game}
    return render(request, 'games/buy_game.html', context)

@login_required
def unlock_achievement(request, achievement_id):
    """Быстрая разблокировка достижения"""
    achievement = get_object_or_404(Achivments, pk=achievement_id)
    
    # Проверяем, есть ли уже это достижение у пользователя
    existing = UserAchivment.objects.filter(
        user_id=request.user,
        achivment_id=achievement
    ).exists()
    
    if not existing and request.method == 'POST':
        UserAchivment.objects.create(
            user_id=request.user,
            achivment_id=achievement,
            status='new'
        )
        messages.success(request, f'Достижение "{achievement.name_achivments}" разблокировано!')
        return redirect('user_achievement_list')
    
    context = {
        'achievement': achievement,
        'already_unlocked': existing,
    }
    return render(request, 'games/unlock_achievement.html', context)

# ========== API-like JSON Views ==========
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def api_games(request):
    """API для получения списка игр (JSON)"""
    games = Game.objects.all()
    data = [{
        'id': game.id,
        'name': game.name,
        'price': game.price,
        'description': game.description,
    } for game in games]
    return JsonResponse({'games': data})

@require_http_methods(["GET"])
def api_user_achievements(request, user_id):
    """API для получения достижений пользователя (JSON)"""
    if request.user.is_authenticated and (request.user.is_staff or request.user.id == user_id):
        user_achievements = UserAchivment.objects.filter(user_id=user_id)
        data = [{
            'id': ua.id,
            'achievement_name': ua.achivment_id.name_achivments,
            'achievement_description': ua.achivment_id.description,
            'status': ua.status,
        } for ua in user_achievements]
        return JsonResponse({'achievements': data})
    return JsonResponse({'error': 'Access denied'}, status=403)