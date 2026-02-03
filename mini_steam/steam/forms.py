from django import forms
from django.contrib.auth.models import User
from .models import Game, Achivments, UserAchivment, Order

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AchivmentsForm(forms.ModelForm):
    class Meta:
        model = Achivments
        fields = ['game_name', 'name_achivments', 'description']
        widgets = {
            'game_name': forms.Select(attrs={'class': 'form-control'}),
            'name_achivments': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserAchivmentForm(forms.ModelForm):
    class Meta:
        model = UserAchivment
        fields = ['user_id', 'achivment_id', 'status']
        widgets = {
            'user_id': forms.Select(attrs={'class': 'form-control'}),
            'achivment_id': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['game_id', 'user_id', 'price']
        widgets = {
            'game_id': forms.Select(attrs={'class': 'form-control'}),
            'user_id': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)