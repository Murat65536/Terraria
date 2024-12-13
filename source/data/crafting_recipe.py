from typing import TypedDict

class CraftingRecipeData(TypedDict):
    id: int
    id_str: str

CRAFTING_RECIPES: list[CraftingRecipeData] = [
    {"id": 0, "id_str": "crafting_recipe.INVALID"},
    {"id": 1, "id_str": "crafting_recipe.work_bench"},
]