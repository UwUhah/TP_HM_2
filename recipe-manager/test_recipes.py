import pytest
from recipes import Ingredient, Recipe, DietaryRecipe, ShoppingList


class TestIngredient:
    def test_creation(self):
        ing = Ingredient("Мука", 500.0, "г")
        assert ing.name == "Мука"
        assert ing.quantity == 500.0
        assert ing.unit == "г"

    def test_str(self):
        ing = Ingredient("Мука", 500.0, "г")
        assert str(ing) == "Мука: 500.0 г"

    def test_eq_same_name_and_unit(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 200.0, "г")
        assert ing1 == ing2

    def test_eq_different_name(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Сахар", 500.0, "г")
        assert ing1 != ing2

    def test_eq_different_unit(self):
        ing1 = Ingredient("Мука", 500.0, "г")
        ing2 = Ingredient("Мука", 500.0, "кг")
        assert ing1 != ing2

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            Ingredient("Мука", -1, "г")

    def test_zero_quantity_raises(self):
        with pytest.raises(ValueError, match="Количество должно быть положительным"):
            Ingredient("Мука", 0, "г")


class TestRecipe:
    def test_creation(self):
        r = Recipe("Пицца")
        assert r.title == "Пицца"
        assert r.ingredients == []

    def test_creation_with_ingredients(self):
        ing = Ingredient("Мука", 500.0, "г")
        r = Recipe("Пицца", [ing])
        assert len(r.ingredients) == 1
        assert r.ingredients[0] == ing

    def test_add_ingredient_new(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        assert len(r.ingredients) == 1
        assert r.ingredients[0].quantity == 500.0

    def test_add_ingredient_duplicate_sums_quantity(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r.add_ingredient(Ingredient("Мука", 200.0, "г"))
        assert len(r.ingredients) == 1
        assert r.ingredients[0].quantity == 700.0

    def test_scale_returns_new_recipe(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        scaled = r.scale(2)
        assert scaled is not r
        assert isinstance(scaled, Recipe)

    def test_scale_multiplies_quantities(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r.add_ingredient(Ingredient("Сыр", 200.0, "г"))
        scaled = r.scale(2)
        assert scaled.ingredients[0].quantity == 1000.0
        assert scaled.ingredients[1].quantity == 400.0
        assert r.ingredients[0].quantity == 500.0

    def test_scale_ratio_zero_raises(self):
        r = Recipe("Пицца")
        with pytest.raises(ValueError):
            r.scale(0)

    def test_scale_ratio_negative_raises(self):
        r = Recipe("Пицца")
        with pytest.raises(ValueError):
            r.scale(-1)

    def test_len(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r.add_ingredient(Ingredient("Сыр", 200.0, "г"))
        assert len(r) == 2

    def test_len_empty(self):
        r = Recipe("Пицца")
        assert len(r) == 0


class TestDietaryRecipe:
    def test_creation(self):
        r = DietaryRecipe("Салат", "веган")
        assert r.title == "Салат"
        assert r.diet_type == "веган"

    def test_scale_returns_dietary(self):
        r = DietaryRecipe("Салат", "веган")
        r.add_ingredient(Ingredient("Помидор", 100.0, "г"))
        scaled = r.scale(2)
        assert isinstance(scaled, DietaryRecipe)
        assert scaled.diet_type == "веган"
        assert scaled.ingredients[0].quantity == 200.0

    def test_str(self):
        r = DietaryRecipe("Салат", "веган")
        r.add_ingredient(Ingredient("Помидор", 100.0, "г"))
        assert "[веган]" in str(r)


class TestShoppingList:
    def test_add_recipe(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        sl = ShoppingList()
        sl.add_recipe(r, 2)
        assert len(sl._items) == 1
        assert sl._items[0][0].quantity == 1000.0
        assert sl._items[0][1] == "Пицца"

    def test_add_recipe_zero_portions_raises(self):
        r = Recipe("Пицца")
        sl = ShoppingList()
        with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
            sl.add_recipe(r, 0)

    def test_add_recipe_negative_portions_raises(self):
        r = Recipe("Пицца")
        sl = ShoppingList()
        with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
            sl.add_recipe(r, -1)

    def test_remove_recipe(self):
        r1 = Recipe("Пицца")
        r1.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r2 = Recipe("Салат")
        r2.add_ingredient(Ingredient("Помидор", 100.0, "г"))
        sl = ShoppingList()
        sl.add_recipe(r1, 1)
        sl.add_recipe(r2, 1)
        assert len(sl._items) == 2
        sl.remove_recipe("Пицца")
        assert len(sl._items) == 1
        assert sl._items[0][1] == "Салат"

    def test_remove_nonexistent_recipe_does_nothing(self):
        sl = ShoppingList()
        sl.remove_recipe("Несуществующий")

    def test_get_list_sums_duplicate_ingredients(self):
        r1 = Recipe("Пицца")
        r1.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r2 = Recipe("Хлеб")
        r2.add_ingredient(Ingredient("Мука", 300.0, "г"))
        sl = ShoppingList()
        sl.add_recipe(r1, 1)
        sl.add_recipe(r2, 1)
        result = sl.get_list()
        assert len(result) == 1
        assert result[0].name == "Мука"
        assert result[0].quantity == 800.0
        assert result[0].unit == "г"

    def test_get_list_sorted_by_name(self):
        r = Recipe("Пицца")
        r.add_ingredient(Ingredient("Сыр", 200.0, "г"))
        r.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r.add_ingredient(Ingredient("Томат", 100.0, "г"))
        sl = ShoppingList()
        sl.add_recipe(r, 1)
        result = sl.get_list()
        assert result[0].name == "Мука"
        assert result[1].name == "Сыр"
        assert result[2].name == "Томат"

    def test_get_list_empty(self):
        sl = ShoppingList()
        assert sl.get_list() == []

    def test_add_combines_lists(self):
        r1 = Recipe("Пицца")
        r1.add_ingredient(Ingredient("Мука", 500.0, "г"))
        r2 = Recipe("Хлеб")
        r2.add_ingredient(Ingredient("Мука", 300.0, "г"))
        sl1 = ShoppingList()
        sl1.add_recipe(r1, 1)
        sl2 = ShoppingList()
        sl2.add_recipe(r2, 1)
        sl3 = sl1 + sl2
        result = sl3.get_list()
        assert result[0].quantity == 800.0

    def test_add_does_not_modify_originals(self):
        r1 = Recipe("Пицца")
        r1.add_ingredient(Ingredient("Мука", 500.0, "г"))
        sl1 = ShoppingList()
        sl1.add_recipe(r1, 1)
        sl2 = ShoppingList()
        sl3 = sl1 + sl2
        assert len(sl1._items) == 1
        assert len(sl2._items) == 0
        assert len(sl3._items) == 1

    def test_add_returns_new_object(self):
        sl1 = ShoppingList()
        sl2 = ShoppingList()
        sl3 = sl1 + sl2
        assert sl3 is not sl1
        assert sl3 is not sl2