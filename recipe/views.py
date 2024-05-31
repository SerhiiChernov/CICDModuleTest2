from django.shortcuts import render
from .models import Category


def main(request):
    categories = Category.objects.all()
    return render(request, 'main.html', context={'categories': categories})

def recipe_list(request):
    categories = Category.objects.prefetch_related('recipes').all()
    return render(request, 'recipes/recipe_list.html', {'categories': categories})