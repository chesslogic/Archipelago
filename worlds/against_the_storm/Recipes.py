
from BaseClasses import CollectionState

from .Items import item_dict

game_recipes = {
    'Jerky': ['Insects,Meat'],
    'Porridge': ['Grain,Vegetables,Mushrooms,Herbs', 'Planks'],
    'Skewers': ['Insects,Meat,Mushrooms,Jerky', 'Vegetables,Roots,Berries,Eggs'],
    'Biscuits': ['Flour', 'Herbs,Berries,Roots'],
    'Pie': ['Flour', 'Herbs,Meat,Insects,Eggs,Berries'],
    'Pickled Goods': ['Vegetables,Mushrooms,Roots,Berries,Eggs', 'Pottery,Barrels,Waterskins'],
    'Coats': ['Fabric'],
    'Bricks': ['Clay,Stone'],
    'Fabric': ['Leather,Plant Fiber,Reeds'],
    'Pipes': ['Copper Bars,Crystallized Dew'],
    'Ale': ['Grain,Roots', 'Barrels,Pottery,Waterskins'],
    'Incense': ['Herbs,Insects,Resin,Roots'],
    'Scrolls': ['Pigment,Wine'],
    'Tea': ['Herbs,Mushrooms,Pigment,Resin,Roots', 'Planks', 'Copper Bars,Crystallized Dew'],
    'Training Gear': ['Copper Bars,Crystallized Dew,Stone', 'Planks,Reeds'],
    'Wine': ['Berries,Mushrooms,Reeds', 'Barrels,Pottery,Waterskins'],
    'Crystallized Dew': ['Herbs,Insects,Resin,Vegetables', 'Stone,Clay', 'Planks'],
    'Barrels': ['Copper Bars,Crystallized Dew', 'Planks'],
    'Copper Bars': ['Copper Ore'],
    'Flour': ['Grain,Mushrooms,Roots'],
    'Pigment': ['Berries,Coal,Copper Ore,Insects'],
    'Pottery': ['Clay'],
    'Waterskins': ['Leather', 'Meat,Oil'],
    'Pack of Building Materials': ['Bricks,Copper Ore,Fabric,Planks'],
    'Pack of Provisions': ['Berries,Eggs,Herbs,Insects,Meat'],
    'Pack of Crops': ['Grain,Mushrooms,Roots,Vegetables'],
    'Pack of Luxury Goods': ['Ale,Incense,Scrolls,Tea,Training Gear,Wine'],
    'Pack of Trade Goods': ['Barrels,Flour,Oil,Pigment,Pottery,Waterskins'],
    'Oil': ['Grain,Meat,Vegetables,Plant Fiber'],
    'Tools': ['Copper Bars,Crystallized Dew'],
    'Purging Fire': ['Coal,Oil,Sea Marrow']
}

def satisfies_recipe(state: CollectionState, player: int, recipe: list[str]) -> bool:
    # recipe is of the form ["A,B,C", "D,E"] meaning (A or B or C) and (D or E)
    for item_set in recipe:
        # Break when we can craft one of the items in the column, "accepting" it. If we can't satisfy the column, then we can't satisfy `recipe`
        for item in item_set.split(","):
            if not item in item_dict.keys():
                print(f"[ATS] WARNING: Logical requirement for unknown item: {item}")
            # We only truly "state.has" an item if we have the production chain that can craft it
            if state.has(item, player) and (not item in game_recipes.keys() or satisfies_recipe(state, player, game_recipes[item])):
                break
        else:
            return False
    return True
