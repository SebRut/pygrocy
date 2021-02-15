import base64
from datetime import datetime

from pygrocy.base import DataModel
from pygrocy.grocy_api_client import (
    GrocyApiClient,
    MealPlanResponse,
    RecipeDetailsResponse,
)


class RecipeItem(DataModel):
    def __init__(self, response: RecipeDetailsResponse):
        self._id = response.id
        self._name = response.name
        self._description = response.description
        self._base_servings = response.base_servings
        self._desired_servings = response.desired_servings
        self._picture_file_name = response.picture_file_name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def base_servings(self) -> int:
        return self._base_servings

    @property
    def desired_servings(self) -> int:
        return self._desired_servings

    @property
    def picture_file_name(self) -> str:
        return self._picture_file_name

    def get_picture_url_path(self, width: int = 400):
        if self.picture_file_name:
            b64name = base64.b64encode(self.picture_file_name.encode("ascii"))
            path = "files/recipepictures/" + str(b64name, "utf-8")

            return f"{path}?force_serve_as=picture&best_fit_width={width}"


class MealPlanItem(DataModel):
    def __init__(self, response: MealPlanResponse):
        self._id = response.id
        self._day = response.day
        self._recipe = None
        self._recipe_id = response.recipe_id
        self._recipe_servings = response.recipe_servings
        self._note = response.note

    @property
    def id(self) -> int:
        return self._id

    @property
    def day(self) -> datetime:
        return self._day

    @property
    def recipe_id(self) -> int:
        return self._recipe_id

    @property
    def recipe_servings(self) -> int:
        return self._recipe_servings

    @property
    def note(self) -> str:
        return self._note

    @property
    def recipe(self) -> RecipeItem:
        return self._recipe

    def get_details(self, api_client: GrocyApiClient):
        if self.recipe_id:
            recipe = api_client.get_recipe(self.recipe_id)
            if recipe:
                self._recipe = RecipeItem(recipe)
