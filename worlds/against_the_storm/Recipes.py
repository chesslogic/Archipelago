
from itertools import chain
from typing import Dict
from BaseClasses import CollectionState

from .Items import item_dict

game_recipes = {
    'Jerky': ['Insects,Meat'],
    'Porridge': ['Grain,Vegetables,Mushrooms,Herbs,Fish', 'Planks'],
    'Skewers': ['Insects,Meat,Mushrooms,Jerky,Fish', 'Vegetables,Roots,Berries,Eggs'],
    'Biscuits': ['Flour', 'Herbs,Berries,Roots,Eggs,Salt'],
    'Pie': ['Flour', 'Herbs,Meat,Insects,Berries,Fish'],
    'Pickled Goods': ['Vegetables,Mushrooms,Roots,Berries,Eggs', 'Pottery,Barrels,Waterskins'],
    'Paste': ['Dye,Salt', 'Eggs,Fish,Meat'],
    'Coats': ['Fabric,Leather', 'Dye,Resin'],
    'Boots': ['Leather,Scales'],
    'Bricks': ['Clay,Stone'],
    'Fabric': ['Plant Fiber,Reeds,Algae'],
    'Pipes': ['Copper Bars,Crystallized Dew'],
    'Ale': ['Grain,Roots', 'Barrels,Pottery,Waterskins'],
    'Incense': ['Herbs,Insects,Resin,Roots,Scales,Salt'],
    'Scrolls': ['Dye,Wine'],
    'Tea': ['Herbs,Mushrooms,Dye,Resin,Roots', 'Planks', 'Copper Bars,Crystallized Dew'],
    'Training Gear': ['Copper Bars,Crystallized Dew,Stone', 'Planks,Reeds'],
    'Wine': ['Berries,Mushrooms,Reeds', 'Barrels,Pottery,Waterskins'],
    'Crystallized Dew': ['Herbs,Insects,Resin,Vegetables,Algae', 'Stone,Clay,Salt', 'Planks'],
    'Barrels': ['Copper Bars,Crystallized Dew', 'Planks'],
    'Copper Bars': ['Copper Ore,Scales'],
    'Flour': ['Grain,Mushrooms,Roots,Algae'],
    'Dye': ['Berries,Coal,Copper Ore,Insects,Scales'],
    'Pottery': ['Clay'],
    'Waterskins': ['Leather,Scales', 'Meat,Oil,Salt'],
    'Pack of Building Materials': ['Bricks,Copper Ore,Fabric,Planks'],
    'Pack of Provisions': ['Berries,Eggs,Herbs,Insects,Meat,Fish'],
    'Pack of Crops': ['Grain,Mushrooms,Roots,Vegetables'],
    'Pack of Luxury Goods': ['Ale,Incense,Scrolls,Tea,Training Gear,Wine'],
    'Pack of Trade Goods': ['Barrels,Flour,Oil,Dye,Pottery,Waterskins'],
    'Oil': ['Grain,Meat,Vegetables,Plant Fiber,Fish'],
    'Tools': ['Copper Bars,Crystallized Dew'],
    'Purging Fire': ['Coal,Oil,Sea Marrow']
}

blueprint_recipes = {
    # 'Foragers Camp': 'Grain,Roots,Vegetables',
    # 'Herbalists Camp': 'Herbs,Berries,Mushrooms',
    # 'Trappers Camp': 'Meat,Insects,Eggs',
    # 'Fishing Hut': 'Algae,Fish,Scales',
    # 'Foresters Hut': 'Resin,Crystallized Dew',
    # 'Herb Garden': 'Roots,Herbs',
    # 'Plantation': 'Berries,Plant Fiber',
    # 'Small Farm': 'Vegetables,Grain',
    # 'Advanced Rain Collector': {},
    'Clay Pit': {'Clay': 2, 'Reeds': 2},
    'Greenhouse': {'Mushrooms': 2, 'Herbs': 2},
    'Bakery': {'Biscuits': 2, 'Pie': 2, 'Pottery': 2},
    'Beanery': {'Porridge': 3, 'Pickled Goods': 1, 'Crystallized Dew': 1},
    'Brick Oven': {'Biscuits': 3, 'Incense': 2, 'Coal': 1},
    'Butcher': {'Skewers': 2, 'Jerky': 2, 'Oil': 2},
    'Cellar': {'Wine': 3, 'Pickled Goods': 2, 'Pack of Provisions': 1},
    'Cookhouse': {'Skewers': 2, 'Biscuits': 2, 'Porridge': 2},
    'Granary': {'Pack of Crops': 2, 'Pickled Goods': 2, 'Fabric': 2},
    'Grill': {'Skewers': 3, 'Paste': 2, 'Copper Bars': 1},
    'Ranch': {'Meat': 1, 'Leather': 1, 'Eggs': 1},
    'Smokehouse': {'Jerky': 3, 'Pottery': 1, 'Incense': 1},
    'Alchemist\'s Hut': {'Crystallized Dew': 2, 'Tea': 2, 'Wine': 2},
    'Apothecary': {'Tea': 2, 'Dye': 2, 'Jerky': 2},
    'Artisan': {'Coats': 2, 'Barrels': 2, 'Scrolls': 2},
    'Brewery': {'Ale': 3, 'Porridge': 2, 'Pack of Crops': 1},
    'Brickyard': {'Bricks': 3, 'Pottery': 2, 'Crystallized Dew': 1},
    'Carpenter': {'Planks': 2, 'Tools': 2, 'Pack of Luxury Goods': 2},
    'Clothier': {'Coats': 3, 'Pack of Building Materials': 2, 'Waterskins': 1},
    'Cooperage': {'Barrels': 3, 'Coats': 2, 'Pack of Luxury Goods': 1},
    'Distillery': {'Pickled Goods': 2, 'Ale': 2, 'Incense': 2},
    'Druid\'s Hut': {'Oil': 3, 'Tea': 2, 'Coats': 1},
    'Furnace': {'Copper Bars': 2, 'Skewers': 2, 'Pie': 2},
    'Kiln': {'Coal': 3, 'Bricks': 1, 'Jerky': 1},
    'Leatherworker': {'Waterskins': 3, 'Boots': 2, 'Training Gear': 1},
    'Lumber Mill': {'Planks': 3, 'Scrolls': 1, 'Pack of Trade Goods': 1},
    'Manufactory': {'Fabric': 2, 'Dye': 2, 'Barrels': 2},
    'Press': {'Oil': 3, 'Flour': 1, 'Paste': 1},
    'Provisioner': {'Flour': 2, 'Barrels': 2, 'Pack of Provisions': 2},
    'Rain Mill': {'Flour': 3, 'Scrolls': 1, 'Paste': 1},
    'Scribe': {'Scrolls': 3, 'Pack of Trade Goods': 2, 'Ale': 1},
    'Smelter': {'Copper Bars': 3, 'Training Gear': 2, 'Pie': 1},
    'Smithy': {'Tools': 2, 'Pipes': 2, 'Pack of Trade Goods': 2},
    'Stamping Mill': {'Bricks': 2, 'Flour': 2, 'Copper Bars': 2},
    'Supplier': {'Flour': 2, 'Planks': 2, 'Waterskins': 2},
    'Teahouse': {'Tea': 3, 'Incense': 2, 'Waterskins': 1},
    'Tinctury': {'Dye': 3, 'Ale': 2, 'Wine': 2},
    'Tinkerer': {'Tools': 2, 'Training Gear': 2, 'Pottery': 2},
    'Toolshop': {'Tools': 3, 'Pipes': 2, 'Boots': 2},
    'Weaver': {'Fabric': 3, 'Training Gear': 1, 'Boots': 1},
    'Workshop': {'Planks': 2, 'Fabric': 2, 'Bricks': 2, 'Pipes': 0},
}

service_blueprints = {
    'Bath House': {'Tea': -1},
    'Clan Hall': {'Training Gear': -1},
    'Explorers Lodge': {'Training Gear': -1, 'Scrolls': -1},
    'Forum': {'Training Gear': -1, 'Wine': -1},
    'Guild House': {'Wine': -1, 'Scrolls': -1},
    'Market': {'Ale': -1, 'Tea': -1},
    'Monastery': {'Incense': -1, 'Ale': -1},
    'Tavern': {'Wine': -1, 'Ale': -1},
    'Tea Doctor': {'Tea': -1, 'Incense': -1},
    'Temple': {'Incense': -1, 'Scrolls': -1},
}

nonitem_blueprint_recipes = {
    'Crude Workstation': {'Planks': 0, 'Fabric': 0, 'Bricks': 0, 'Pipes': 0},
    'Field Kitchen': {'Skewers': 0, 'Paste': 0, 'Biscuits': 0, 'Pickled Goods': 0},
    'Makeshift Post': {'Pack of Crops': 0, 'Pack of Provisions': 0, 'Pack of Building Materials': 0},

    'Flawless Cellar': {'Wine': 3, 'Pickled Goods': 3, 'Pack of Provisions': 3},
    'Flawless Brewery': {'Ale': 3, 'Porridge': 3, 'Pack of Crops': 3},
    'Flawless Cooperage': {'Barrels': 3, 'Coats': 3, 'Pack of Luxury Goods': 3},
    'Flawless Druids Hut': {'Oil': 3, 'Tea': 3, 'Coats': 3},
    'Flawless Leatherworker': {'Waterskins': 3, 'Boots': 3, 'Training Gear': 3},
    'Flawless Rain Mill': {'Flour': 3, 'Scrolls': 3, 'Paste': 3},
    'Flawless Smelter': {'Copper Bars': 3, 'Training Gear': 3, 'Pie': 3},

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
                "Parts", "Ancient Tablet", "Algae", "Fish", "Scales"]:
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
                print(item, state.has(item, player), has_blueprint_for(state, player, blueprint_map, item))
            
            if not item in item_dict.keys():
                print(f"[ATS] WARNING: Logical requirement for unknown item: {item}")
            # We only truly "state.has" an item if we have the production chain that can craft it
            if state.has(item, player) and has_blueprint_for(state, player, blueprint_map, item) and (item not in game_recipes or satisfies_recipe(state, player, blueprint_map, game_recipes[item], debug)):
                break
        else:
            return False
    if debug:
        print(recipe, "satisfied")
    return True
