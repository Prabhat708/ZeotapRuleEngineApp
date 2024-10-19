from django.urls import path
from .views import add_user, add_rule, evaluate_user, get_rules, index

urlpatterns = [
    path('', index, name='home'),
    path('get-rules/', get_rules, name='get_rules'),
    path('user/', add_user, name='add_user'),
    path('rules/', add_rule, name='add_rule'),
    path('evaluate/', evaluate_user, name='evaluate_user'),
]
