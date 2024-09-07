
from itertools import chain
from typing import Dict
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

blueprint_recipes = {
    # 'Foragers Camp': 'Grain,Roots,Vegetables',
    # 'Herbalists Camp': 'Herbs,Berries,Mushrooms',
    # 'Trappers Camp': 'Meat,Insects,Eggs',
    # 'Foresters Hut': 'Resin,Crystallized Dew',
    # 'Herb Garden': 'Roots,Herbs',
    # 'Plantation': 'Berries,Plant Fiber',
    # 'Small Farm': 'Vegetables,Grain',
    # 'Advanced Rain Collector': {},
    'Clay Pit': {'Clay': 2, 'Reeds': 2},
    'Greenhouse': {'Mushrooms': 2, 'Herbs': 2},
    'Bakery': {'Biscuits': 2, 'Pie': 2, 'Pottery': 2},
    'Beanery': {'Porridge': 3, 'Pickled Goods': 1, 'Crystallized Dew': 1},
    'Brick Oven': {'Pie': 3, 'Coal': 1, 'Incense': 1},
    'Butcher': {'Skewers': 2, 'Jerky': 2, 'Oil': 2},
    'Cellar': {'Wine': 3, 'Pickled Goods': 1, 'Jerky': 1},
    'Cookhouse': {'Skewers': 2, 'Biscuits': 2, 'Pigment': 2},
    'Granary': {'Pack of Crops': 2, 'Pickled Goods': 2, 'Fabric': 2},
    'Grill': {'Skewers': 3, 'Copper Bars': 1, 'Ale': 1},
    'Ranch': {'Meat': 1, 'Leather': 1, 'Eggs': 1},
    'Smokehouse': {'Jerky': 3, 'Pottery': 1, 'Incense': 1},
    'Alchemists Hut': {'Crystallized Dew': 2, 'Tea': 2, 'Wine': 2},
    'Apothecary': {'Tea': 2, 'Incense': 2, 'Biscuits': 2},
    'Artisan': {'Coats': 2, 'Barrels': 2, 'Pack of Luxury Goods': 2},
    'Brewery': {'Ale': 3, 'Pickled Goods': 1, 'Pack of Crops': 1},
    'Brickyard': {'Bricks': 3, 'Pottery': 2, 'Crystallized Dew': 1},
    'Carpenter': {'Planks': 2, 'Tools': 2, 'Pack of Luxury Goods': 2},
    'Clothier': {'Coats': 3, 'Waterskins': 1, 'Scrolls': 1},
    'Cooperage': {'Barrels': 3, 'Coats': 2, 'Tea': 1},
    'Distillery': {'Wine': 2, 'Porridge': 2, 'Barrels': 2},
    'Druids Hut': {'Oil': 3, 'Incense': 1, 'Coats': 1},
    'Furnace': {'Copper Bars': 2, 'Bricks': 2, 'Pie': 2},
    'Kiln': {'Coal': 3, 'Bricks': 1, 'Jerky': 1},
    'Leatherworker': {'Waterskins': 3, 'Fabric': 2, 'Pigment': 2},
    'Lumber Mill': {'Planks': 3, 'Scrolls': 1, 'Pack of Trade Goods': 1},
    'Manufactory': {'Training Gear': 2, 'Pigment': 2, 'Pack of Provisions': 2},
    'Press': {'Oil': 3, 'Flour': 1, 'Pack of Luxury Goods': 1},
    'Provisioner': {'Flour': 2, 'Barrels': 2, 'Pack of Provisions': 2},
    'Rain Mill': {'Flour': 3, 'Scrolls': 1, 'Pack of Building Materials': 1},
    'Scribe': {'Scrolls': 3, 'Ale': 2, 'Tools': 1},
    'Smelter': {'Copper Bars': 3, 'Training Gear': 2, 'Biscuits': 1},
    'Smithy': {'Tools': 2, 'Pipes': 2, 'Pack of Trade Goods': 2},
    'Stamping Mill': {'Pottery': 3, 'Flour': 2, 'Copper Bars': 1},
    'Supplier': {'Flour': 2, 'Planks': 2, 'Waterskins': 2},
    'Teahouse': {'Tea': 3, 'Porridge': 2, 'Waterskins': 1},
    'Tinctury': {'Ale': 2, 'Wine': 2, 'Pigment': 2},
    'Tinkerer': {'Tools': 2, 'Training Gear': 2, 'Pack of Building Materials': 2},
    'Toolshop': {'Tools': 3, 'Pipes': 2, 'Barrels': 1},
    'Weaver': {'Fabric': 3, 'Training Gear': 1, 'Pack of Trade Goods': 1},
    'Workshop': {'Planks': 2, 'Fabric': 2, 'Bricks': 2, 'Pipes': 0},
}

service_blueprints = {
    'Bath House': {'Tea': -1},
    'Clan Hall': {'Training Gear': -1, 'Incense': -1},
    'Explorers Lodge': {'Training Gear': -1, 'Scrolls': -1},
    'Forum': {'Ale': -1, 'Scrolls': -1},
    'Guild House': {'Wine': -1},
    'Market': {'Wine': -1, 'Tea': -1},
    'Monastery': {'Incense': -1, 'Ale': -1},
    'Tavern': {'Wine': -1, 'Ale': -1},
    'Tea Doctor': {'Tea': -1, 'Training Gear': -1},
    'Temple': {'Incense': -1, 'Scrolls': -1},
}

nonitem_blueprint_recipes = {
    'Crude Workstation': {'Planks': 0, 'Fabric': 0, 'Bricks': 0, 'Pipes': 0},
    'Field Kitchen': {'Jerky': 0, 'Porridge': 0, 'Biscuits': 0, 'Pickled Goods': 0},
    'Makeshift Post': {'Pack of Crops': 0, 'Pack of Provisions': 0, 'Pack of Building Materials': 0},

    'Flawless Cellar': {'Wine': 3, 'Pickled Goods': 3, 'Jerky': 3},
    'Flawless Brewery': {'Ale': 3, 'Pickled Goods': 3, 'Pack of Crops': 3},
    'Flawless Cooperage': {'Barrels': 3, 'Coats': 3, 'Tea': 3},
    'Flawless Druids Hut': {'Oil': 3, 'Incense': 3, 'Coats': 3},
    'Flawless Leatherworker': {'Waterskins': 3, 'Fabric': 3, 'Pigment': 3},
    'Flawless Rain Mill': {'Flour': 3, 'Scrolls': 3, 'Pack of Building Materials': 3},
    'Flawless Smelter': {'Copper Bars': 3, 'Training Gear': 3, 'Biscuits': 3},

    'Finesmith': {'Amber': 3, 'Tools': 3},
    'Rainpunk Foundry': {'Parts': 3, 'Wildfire Essence': 3},
}

def has_blueprint_for(state: CollectionState, player: int, blueprint_map: Dict[str, Dict[str, int]] | None, good: str) -> bool:
    # blueprint_items are off, meaning we don't need to worry about access to a building that craft this good
    if blueprint_map == None:
        return True

    # These goods can be obtained through means that don't require a blueprint item
    if good in ["Berries", "Eggs", "Insects", "Meat", "Mushrooms", "Roots", "Vegetables", "Clay", "Copper Ore", "Grain",
                "Herbs", "Leather", "Plant Fiber", "Reeds", "Resin", "Stone", "Amber", "Purging Fire", "Sea Marrow",
                "Parts", "Ancient Tablet"]:
        return True
    
    # We should check if we have a service building for service goods, as most checks for them are locations about consuming them
    if good in ["Ale", "Incense", "Scrolls", "Tea", "Training Gear", "Wine"]:
        if len([bp for bp in service_blueprints.keys() if good in service_blueprints[bp] and (bp in ["Crude Workstation", "Field Kitchen", "Makeshift Post"] or state.has(bp, player))]) == 0:
            return False

    # Find a blueprint that has the item in the blueprint_map, which will have options like recipe_shuffle baked in
    return len([bp for bp in blueprint_map.keys() if good in chain.from_iterable(blueprint_map[bp]) and (bp in ["Crude Workstation", "Field Kitchen", "Makeshift Post"] or state.has(bp, player))]) > 0

def satisfies_recipe(state: CollectionState, player: int, blueprint_map: Dict[str, Dict[str, int]] | None, recipe: list[str], debug = False) -> bool:
    # recipe is of the form ["A,B,C", "D,E"] meaning (A or B or C) and (D or E)
    for item_set in recipe:
        # Break when we can craft one of the items in the column, satisfying it. If we can't satisfy the column, then we can't satisfy `recipe`
        for item in item_set.split(","):
            if debug:
                print(item, has_blueprint_for(state, player, blueprint_map, item))
            
            if not item in item_dict.keys():
                print(f"[ATS] WARNING: Logical requirement for unknown item: {item}")
            # We only truly "state.has" an item if we have the production chain that can craft it
            if state.has(item, player) and has_blueprint_for(state, player, blueprint_map, item) and (item not in game_recipes or satisfies_recipe(state, player, blueprint_map, game_recipes[item]), debug):
                break
        else:
            return False
    return True
