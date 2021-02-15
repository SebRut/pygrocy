import pytest

from pygrocy.data_models.meal_items import RecipeItem


class TestMealPlan:
    @pytest.mark.vcr
    def test_get_meal_plan_valid(self, grocy):
        meal_plan = grocy.meal_plan(get_details=False)

        assert len(meal_plan) == 8
        item = next(item for item in meal_plan if item.id == 1)
        assert item.day.day == 8
        assert item.recipe_id == 1
        assert item.recipe_servings == 1
        assert item.note is None
        assert item.recipe is None

    @pytest.mark.vcr
    def test_get_meal_plan_with_details_valid(self, grocy):
        meal_plan = grocy.meal_plan(get_details=True)

        assert len(meal_plan) == 8
        item = next(item for item in meal_plan if item.id == 1)
        assert item.day.day == 8
        assert item.recipe_id == 1
        assert item.recipe_servings == 1
        assert item.note is None
        assert isinstance(item.recipe, RecipeItem)

        recipe = item.recipe
        assert recipe.name == "Pizza"
        assert recipe.id == 1
        assert recipe.desired_servings == 1
        assert recipe.base_servings == 1
        assert recipe.description[:4] == "<h1>"
        assert recipe.picture_file_name == "pizza.jpg"
