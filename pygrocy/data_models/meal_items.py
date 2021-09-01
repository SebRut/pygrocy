import base64
from datetime import datetime
from enum import Enum

from pygrocy.base import DataModel
from pygrocy.grocy_api_client import (
    GrocyApiClient,
    MealPlanResponse,
    MealPlanSectionResponse,
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


class MealPlanSection(DataModel):
    def __init__(self, response: MealPlanSectionResponse):
        self._id = response.id
        self._name = response.name
        self._sort_number = response.sort_number
        self._row_created_timestamp = response.row_created_timestamp

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def sort_number(self) -> int:
        return self._sort_number

    @property
    def row_created_timestamp(self) -> datetime:
        return self._row_created_timestamp


class MealPlanItemType(str, Enum):
    NOTE = "note"
    PRODUCT = "product"
    RECIPE = "recipe"


class MealPlanItem(DataModel):
    def __init__(self, response: MealPlanResponse):
        self._id = response.id
        self._day = response.day
        self._recipe = None
        self._recipe_id = response.recipe_id
        self._recipe_servings = response.recipe_servings
        self._note = response.note
        self._section_id = response.section_id
        self._type = MealPlanItemType(response.type)
        self._product_id = response.product_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def day(self) -> datetime.date:
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

    @property
    def section_id(self) -> int:
        return self._section_id

    @property
    def section(self) -> MealPlanSection:
        return self._section

    @property
    def type(self) -> MealPlanItemType:
        return self._type

    @property
    def product_id(self) -> int:
        return self._product_id

    def get_details(self, api_client: GrocyApiClient):
        if self.recipe_id:
            recipe = api_client.get_recipe(self.recipe_id)
            if recipe:
                self._recipe = RecipeItem(recipe)
        if self.section_id:
            section = api_client.get_meal_plan_section(self.section_id)
            if section:
                self._section = MealPlanSection(section)
