
from dataclasses import dataclass
from itertools import chain
from typing import Dict, List
from BaseClasses import CollectionState

from .Items import item_dict, progressive_items, items_indexed_by_progressive_source


@dataclass
class Recipe:
    product: str
    stars: int

game_recipes = {
    "Jerky": ["Insects,Meat"],
    "Porridge": ["Grain,Vegetables,Mushrooms,Herbs,Fish", "Planks"],
    "Skewers": ["Insects,Meat,Mushrooms,Jerky,Fish", "Vegetables,Roots,Berries,Eggs"],
    "Biscuits": ["Flour", "Herbs,Berries,Roots,Eggs,Salt"],
    "Pie": ["Flour", "Herbs,Meat,Insects,Berries,Fish"],
    "Pickled Goods": ["Vegetables,Mushrooms,Roots,Berries,Eggs", "Pottery,Barrels,Waterskins"],
    "Paste": ["Dye", "Eggs,Fish,Meat,Salt"],
    "Coats": ["Fabric,Leather", "Dye,Resin"],
    "Boots": ["Leather,Scales"],
    "Bricks": ["Clay,Stone"],
    "Fabric": ["Plant Fiber,Reeds,Algae"],
    "Pipes": ["Copper Bars,Crystallized Dew"],
    "Ale": ["Grain,Roots", "Barrels,Pottery,Waterskins"],
    "Incense": ["Herbs,Insects,Resin,Roots,Scales,Salt"],
    "Scrolls": ["Dye,Wine"],
    "Tea": ["Herbs,Mushrooms,Dye,Resin,Roots", "Planks", "Copper Bars,Crystallized Dew"],
    "Training Gear": ["Copper Bars,Crystallized Dew,Stone", "Planks,Reeds"],
    "Wine": ["Berries,Mushrooms,Reeds", "Barrels,Pottery,Waterskins"],
    "Crystallized Dew": ["Herbs,Insects,Resin,Vegetables,Algae", "Stone,Clay,Salt", "Planks"],
    "Barrels": ["Copper Bars,Crystallized Dew", "Planks"],
    "Copper Bars": ["Copper Ore,Scales"],
    "Flour": ["Grain,Mushrooms,Roots,Algae"],
    "Dye": ["Berries,Coal,Copper Ore,Insects,Scales"],
    "Pottery": ["Clay"],
    "Waterskins": ["Leather,Scales", "Meat,Oil,Salt"],
    "Pack of Building Materials": ["Bricks,Copper Ore,Fabric,Planks"],
    "Pack of Provisions": ["Berries,Eggs,Herbs,Insects,Meat,Fish"],
    "Pack of Crops": ["Grain,Mushrooms,Roots,Vegetables"],
    "Pack of Luxury Goods": ["Ale,Incense,Scrolls,Tea,Training Gear,Wine"],
    "Pack of Trade Goods": ["Barrels,Flour,Oil,Dye,Pottery,Waterskins"],
    "Oil": ["Grain,Meat,Vegetables,Plant Fiber,Fish"],
    "Tools": ["Copper Bars,Crystallized Dew"],
    "Purging Fire": ["Coal,Oil,Sea Marrow"]
}

blueprint_recipes = {
    # "Foragers Camp": "Grain,Roots,Vegetables",
    # "Herbalists Camp": "Herbs,Berries,Mushrooms",
    # "Trappers Camp": "Meat,Insects,Eggs",
    # "Fishing Hut": "Algae,Fish,Scales",
    # "Foresters Hut": "Resin,Crystallized Dew",
    # "Herb Garden": "Roots,Herbs",
    # "Plantation": "Berries,Plant Fiber",
    # "Small Farm": "Vegetables,Grain",
    # "Advanced Rain Collector": "",
    "Clay Pit": [Recipe("Clay", 2), Recipe("Reeds", 2)],
    "Greenhouse": [Recipe("Mushrooms", 2), Recipe("Herbs", 2)],
    "Bakery": [Recipe("Biscuits", 2), Recipe("Pie", 2), Recipe("Pottery", 2)],
    "Beanery": [Recipe("Porridge", 3), Recipe("Pickled Goods", 1), Recipe("Crystallized Dew", 1)],
    "Brick Oven": [Recipe("Biscuits", 3), Recipe("Incense", 2), Recipe("Coal", 1)],
    "Butcher": [Recipe("Skewers", 2), Recipe("Jerky", 2), Recipe("Oil", 2)],
    "Cellar": [Recipe("Wine", 3), Recipe("Pickled Goods", 2), Recipe("Pack of Provisions", 1)],
    "Cookhouse": [Recipe("Skewers", 2), Recipe("Biscuits", 2), Recipe("Porridge", 2)],
    "Granary": [Recipe("Pack of Crops", 2), Recipe("Pickled Goods", 2), Recipe("Fabric", 2)],
    "Grill": [Recipe("Skewers", 3), Recipe("Paste", 2), Recipe("Copper Bars", 1)],
    "Ranch": [Recipe("Meat", 1), Recipe("Leather", 1), Recipe("Eggs", 1)],
    "Smokehouse": [Recipe("Jerky", 3), Recipe("Pottery", 1), Recipe("Incense", 1)],
    "Alchemist\'s Hut": [Recipe("Crystallized Dew", 2), Recipe("Tea", 2), Recipe("Wine", 2)],
    "Apothecary": [Recipe("Tea", 2), Recipe("Dye", 2), Recipe("Jerky", 2)],
    "Artisan": [Recipe("Coats", 2), Recipe("Barrels", 2), Recipe("Scrolls", 2)],
    "Brewery": [Recipe("Ale", 3), Recipe("Porridge", 2), Recipe("Pack of Crops", 1)],
    "Brickyard": [Recipe("Bricks", 3), Recipe("Pottery", 2), Recipe("Crystallized Dew", 1)],
    "Carpenter": [Recipe("Planks", 2), Recipe("Tools", 2), Recipe("Pack of Luxury Goods", 2)],
    "Clothier": [Recipe("Coats", 3), Recipe("Pack of Building Materials", 2), Recipe("Waterskins", 1)],
    "Cooperage": [Recipe("Barrels", 3), Recipe("Coats", 2), Recipe("Pack of Luxury Goods", 1)],
    "Distillery": [Recipe("Pickled Goods", 2), Recipe("Ale", 2), Recipe("Incense", 2)],
    "Druid\'s Hut": [Recipe("Oil", 3), Recipe("Tea", 2), Recipe("Coats", 1)],
    "Furnace": [Recipe("Copper Bars", 2), Recipe("Skewers", 2), Recipe("Pie", 2)],
    "Kiln": [Recipe("Coal", 3), Recipe("Bricks", 1), Recipe("Jerky", 1)],
    "Leatherworker": [Recipe("Waterskins", 3), Recipe("Boots", 2), Recipe("Training Gear", 1)],
    "Lumber Mill": [Recipe("Planks", 3), Recipe("Scrolls", 1), Recipe("Pack of Trade Goods", 1)],
    "Manufactory": [Recipe("Fabric", 2), Recipe("Dye", 2), Recipe("Barrels", 2)],
    "Press": [Recipe("Oil", 3), Recipe("Flour", 1), Recipe("Paste", 1)],
    "Provisioner": [Recipe("Flour", 2), Recipe("Barrels", 2), Recipe("Pack of Provisions", 2)],
    "Rain Mill": [Recipe("Flour", 3), Recipe("Scrolls", 1), Recipe("Paste", 1)],
    "Scribe": [Recipe("Scrolls", 3), Recipe("Pack of Trade Goods", 2), Recipe("Ale", 1)],
    "Smelter": [Recipe("Copper Bars", 3), Recipe("Training Gear", 2), Recipe("Pie", 1)],
    "Smithy": [Recipe("Tools", 2), Recipe("Pipes", 2), Recipe("Pack of Trade Goods", 2)],
    "Stamping Mill": [Recipe("Bricks", 2), Recipe("Flour", 2), Recipe("Copper Bars", 2)],
    "Supplier": [Recipe("Flour", 2), Recipe("Planks", 2), Recipe("Waterskins", 2)],
    "Teahouse": [Recipe("Tea", 3), Recipe("Incense", 2), Recipe("Waterskins", 1)],
    "Tinctury": [Recipe("Dye", 3), Recipe("Ale", 2), Recipe("Wine", 2)],
    "Tinkerer": [Recipe("Tools", 2), Recipe("Training Gear", 2), Recipe("Pottery", 2)],
    "Toolshop": [Recipe("Tools", 3), Recipe("Pipes", 2), Recipe("Boots", 2)],
    "Weaver": [Recipe("Fabric", 3), Recipe("Training Gear", 1), Recipe("Boots", 1)],
    "Workshop": [Recipe("Planks", 2), Recipe("Fabric", 2), Recipe("Bricks", 2), Recipe("Pipes", 0)],
}

service_blueprints = {
    "Bath House": ["Tea"],
    "Clan Hall": ["Training Gear"],
    "Explorers Lodge": ["Training Gear", "Scrolls"],
    "Forum": ["Training Gear", "Wine"],
    "Guild House": ["Wine", "Scrolls"],
    "Market": ["Ale", "Tea"],
    "Monastery": ["Incense", "Ale"],
    "Tavern": ["Wine", "Ale"],
    "Tea Doctor": ["Tea", "Incense"],
    "Temple": ["Incense", "Scrolls"],
}

nonitem_blueprint_recipes = {
    "Crude Workstation": [Recipe("Planks", 0), Recipe("Fabric", 0), Recipe("Bricks", 0), Recipe("Pipes", 0)],
    "Field Kitchen": [Recipe("Skewers", 0), Recipe("Paste", 0), Recipe("Biscuits", 0), Recipe("Pickled Goods", 0)],
    "Makeshift Post": [Recipe("Pack of Crops", 0), Recipe("Pack of Provisions", 0), Recipe("Pack of Building Materials", 0)],

    "Flawless Cellar": [Recipe("Wine", 3), Recipe("Pickled Goods", 3), Recipe("Pack of Provisions", 3)],
    "Flawless Brewery": [Recipe("Ale", 3), Recipe("Porridge", 3), Recipe("Pack of Crops", 3)],
    "Flawless Cooperage": [Recipe("Barrels", 3), Recipe("Coats", 3), Recipe("Pack of Luxury Goods", 3)],
    "Flawless Druids Hut": [Recipe("Oil", 3), Recipe("Tea", 3), Recipe("Coats", 3)],
    "Flawless Leatherworker": [Recipe("Waterskins", 3), Recipe("Boots", 3), Recipe("Training Gear", 3)],
    "Flawless Rain Mill": [Recipe("Flour", 3), Recipe("Scrolls", 3), Recipe("Paste", 3)],
    "Flawless Smelter": [Recipe("Copper Bars", 3), Recipe("Training Gear", 3), Recipe("Pie", 3)],

    "Finesmith": [Recipe("Amber", 3), Recipe("Tools", 3)],
    "Rainpunk Foundry": [Recipe("Parts", 3), Recipe("Wildfire Essence", 3)],
}

essential_blueprints = [
    "Crude Workstation", "Field Kitchen", "Makeshift Post"
]

def has_blueprint_for(state: CollectionState, player: int, blueprint_map: Dict[str, List[Recipe]] | None, good: str) -> bool:
    # blueprint_items are off, meaning we don't need to worry about access to a building that can craft this good
    if blueprint_map == None:
        return True

    # These goods can be obtained through means that don't require a blueprint item
    if good in ["Berries", "Eggs", "Insects", "Meat", "Mushrooms", "Roots", "Vegetables", "Clay", "Copper Ore", "Grain",
                "Herbs", "Leather", "Plant Fiber", "Reeds", "Resin", "Stone", "Amber", "Purging Fire", "Sea Marrow",
                "Parts", "Ancient Tablet", "Algae", "Fish", "Scales"]:
        return True
    
    # We should check if we have a service building for service goods,
    # as most checks for them are locations about consuming them
    if good in ["Ale", "Incense", "Scrolls", "Tea", "Training Gear", "Wine"]:
        if not any(good in service_blueprints[bp] and state.has(bp, player) for bp in service_blueprints.keys()):
            return False

    # Find a blueprint that has the item in the blueprint_map, which will have options like recipe_shuffle baked in
    return any(any(good == recipe.product for recipe in blueprint_map[bp]) and
               (bp in essential_blueprints or state.has(bp, player)) for bp in blueprint_map.keys())


def satisfies_recipe(state: CollectionState, player: int, blueprint_map: Dict[str, List[Recipe]] | None, recipe: list[str], debug = False) -> bool:
    # recipe is of the form ["A,B,C", "D,E"] meaning (A or B or C) and (D or E)
    for item_set in recipe:
        # Break when we can craft one of the items in the column, satisfying it. If we can't satisfy the column, then we can't satisfy `recipe`
        for item in item_set.split(","):
            if debug:
                print(item, state.has(item, player), has_blueprint_for(state, player, blueprint_map, item))
            
            if not item in item_dict.keys():
                print(f"[ATS] WARNING: Logical requirement for unknown item: {item}")
            # We only truly "state.has" an item if we have the production chain that can craft it
            if state.has(item, player) and has_blueprint_for(state, player, blueprint_map, item) and \
               (item not in game_recipes or satisfies_recipe(state, player, blueprint_map, game_recipes[item], debug)):
                break
        else:
            return False
    if debug:
        print(recipe, "satisfied")
    return True


def has_product(state: CollectionState, player: int, product: str) -> bool:
    current_progressive_items = {}  # TODO(chesslogic): calculate products from progressive items
    for item in progressive_items:
        current_progressive_items[item] = state.count(item, player)
    granted_progressive_items = {}
    for origin in items_indexed_by_progressive_source[product]:
        if origin[1] in current_progressive_items and origin[0] <= current_progressive_items[origin[1]]:
            granted_progressive_items[product] = current_progressive_items[product]
    return state.has(product, player) or product in granted_progressive_items
