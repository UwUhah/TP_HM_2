class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit

    def __hash__(self):
        return hash((self.name, self.unit))


class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        self.ingredients = ingredients if ingredients is not None else []

    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        scaled_ingredients = [
            Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            for ing in self.ingredients
        ]
        return Recipe(self.title, scaled_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        lines = [self.title]
        for ing in self.ingredients:
            lines.append(f"  {ing}")
        return "\n".join(lines)


class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        scaled_ingredients = [
            Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            for ing in self.ingredients
        ]
        return DietaryRecipe(self.title, self.diet_type, scaled_ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ingredient in scaled.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        self._items = [
            (ing, rec_title)
            for ing, rec_title in self._items
            if rec_title != title
        ]

    def get_list(self):
        merged = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            merged[key] = merged.get(key, 0) + ingredient.quantity
        result = [
            Ingredient(name, quantity, unit)
            for (name, unit), quantity in merged.items()
        ]
        result.sort(key=lambda ing: ing.name)
        return result

    def __add__(self, other: "ShoppingList"):
        new_list = ShoppingList()
        new_list._items = self._items.copy() + other._items.copy()
        return new_list