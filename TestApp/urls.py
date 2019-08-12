from django.urls import path
from .views import adicionarProduto, atualizarProduto, deletarProduto, criarMenu

urlpatterns = [
    path('', criarMenu, name='criarMenu'),
    path('add', adicionarProduto, name='adicionarProduto'),
    path('update/<int:id>/', atualizarProduto, name='atualizarProduto'),
    path('delete/<int:id>/', deletarProduto, name='deletarProduto'),

    ]