```markdown
# Система управления рецептами

Консольное приложение для создания рецептов блюд, масштабирования порций и автоматической генерации объединённого списка покупок.

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/ваш-логин/recipe-manager.git
   cd recipe-manager
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Использование

Для запуска тестов выполните:
```bash
pytest
```

Для подробного вывода:
```bash
pytest -v
```

## Структура проекта

- `recipes.py` — классы Ingredient, Recipe, DietaryRecipe, ShoppingList
- `test_recipes.py` — unit-тесты для всех классов
- `requirements.txt` — зависимости проекта

## Автор

Логинов Давид, группа ББИ2503
```