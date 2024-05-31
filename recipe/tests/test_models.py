import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_recipe.settings")
import django
django.setup()
import pytest
from django.utils import timezone
from recipe.models import Category, Recipe

@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Desserts")
    assert category.name == "Desserts"
    assert str(category) == "Desserts"

@pytest.mark.django_db
def test_recipe_creation():
    category = Category.objects.create(name="Desserts")
    recipe = Recipe.objects.create(
        title="Chocolate Cake",
        description="Delicious chocolate cake.",
        instructions="Mix ingredients and bake.",
        ingredients="Flour, Sugar, Cocoa, Butter",
        category=category
    )
    assert recipe.title == "Chocolate Cake"
    assert recipe.description == "Delicious chocolate cake."
    assert recipe.instructions == "Mix ingredients and bake."
    assert recipe.ingredients == "Flour, Sugar, Cocoa, Butter"
    assert recipe.category == category
    assert str(recipe) == "Chocolate Cake"
    assert recipe.created_at <= timezone.now()
    assert recipe.updated_at <= timezone.now()

@pytest.mark.django_db
def test_recipe_category_relation():
    category = Category.objects.create(name="Desserts")
    recipe1 = Recipe.objects.create(
        title="Chocolate Cake",
        description="Delicious chocolate cake.",
        instructions="Mix ingredients and bake.",
        ingredients="Flour, Sugar, Cocoa, Butter",
        category=category
    )
    recipe2 = Recipe.objects.create(
        title="Vanilla Ice Cream",
        description="Creamy vanilla ice cream.",
        instructions="Mix ingredients and freeze.",
        ingredients="Milk, Sugar, Vanilla",
        category=category
    )
    assert recipe1.category == category
    assert recipe2.category == category
    assert list(category.recipes.all()) == [recipe1, recipe2]

@pytest.mark.django_db
def test_category_update():
    category = Category.objects.create(name="Desserts")
    category.name = "Updated Desserts"
    category.save()
    updated_category = Category.objects.get(id=category.id)
    assert updated_category.name == "Updated Desserts"
    assert str(updated_category) == "Updated Desserts"

@pytest.mark.django_db
def test_recipe_deletion():
    category = Category.objects.create(name="Desserts")
    recipe = Recipe.objects.create(
        title="Chocolate Cake",
        description="Delicious chocolate cake.",
        instructions="Mix ingredients and bake.",
        ingredients="Flour, Sugar, Cocoa, Butter",
        category=category
    )
    recipe_id = recipe.id
    recipe.delete()
    with pytest.raises(Recipe.DoesNotExist):
        Recipe.objects.get(id=recipe_id)

@pytest.mark.django_db
def test_category_deletion_with_recipes():
    category = Category.objects.create(name="Desserts")
    recipe1 = Recipe.objects.create(
        title="Chocolate Cake",
        description="Delicious chocolate cake.",
        instructions="Mix ingredients and bake.",
        ingredients="Flour, Sugar, Cocoa, Butter",
        category=category
    )
    recipe2 = Recipe.objects.create(
        title="Vanilla Ice Cream",
        description="Creamy vanilla ice cream.",
        instructions="Mix ingredients and freeze.",
        ingredients="Milk, Sugar, Vanilla",
        category=category
    )
    category.delete()
    assert Recipe.objects.filter(category=category).count() == 0
    with pytest.raises(Category.DoesNotExist):
        Category.objects.get(id=category.id)

@pytest.mark.django_db
def test_recipe_str_method():
    category = Category.objects.create(name="Desserts")
    recipe = Recipe.objects.create(
        title="Chocolate Cake",
        description="Delicious chocolate cake.",
        instructions="Mix ingredients and bake.",
        ingredients="Flour, Sugar, Cocoa, Butter",
        category=category
    )
    assert str(recipe) == "Chocolate Cake"

@pytest.mark.django_db
def test_category_str_method():
    category = Category.objects.create(name="Desserts")
    assert str(category) == "Desserts"