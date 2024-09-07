from random import randrange, sample
import re
import logging
from typing import Any, Dict, List, Tuple
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import CollectionState, Region

from .Items import ATSItemClassification, AgainstTheStormItem, item_dict
from .Locations import ATSLocationClassification, AgainstTheStormLocation, location_dict
from .Options import AgainstTheStormOptions, RecipeShuffle
from .Recipes import satisfies_recipe, blueprint_recipes, nonitem_blueprint_recipes

class AgainstTheStormWorld(World):
    """
    Against the Storm is a roguelite city builder
    """

    game = "Against the Storm"
    options_dataclass = AgainstTheStormOptions
    options: AgainstTheStormOptions
    topology_present = True
    base_id = 9999000000
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), base_id)}

    total_location_count: int
    included_location_indices: list[int] = []
    location_pool: Dict[str, int] = {}
    production_recipes: Dict[str, List[List]] = {}
    
    def are_recipes_beatable(self, production_recipes: Dict[str, List[List]]):
        glade_blueprints = [bp for bp in nonitem_blueprint_recipes if
                            bp != "Crude Workstation" and bp != "Field Kitchen" and bp != "Makeshift Post"]

        for bp in glade_blueprints:
            for recipe in production_recipes[bp]:
                # Need to verify each of these recipes have an alternate outside glade_blueprints
                satisfied = False
                for (building, recipes) in production_recipes.items():
                    if building in glade_blueprints:
                        continue
                    for rec in recipes:
                        if rec[0] == recipe[0]:
                            satisfied = True
                            break
                    if satisfied:
                        break
                if not satisfied:
                    return False
        
        return True

    def generate_early(self):
        # There are 64 `basic` locations
        self.total_location_count = 64 + self.options.reputation_locations_per_biome.value * 6 + self.options.extra_trade_locations.value
        # There are 57 `good` items
        total_item_count = 57 + (59 if self.options.blueprint_items else 0) + (4 if self.options.seal_items else 0)
        if self.total_location_count < total_item_count:
            while self.total_location_count < total_item_count:
                self.options.reputation_locations_per_biome.value += 1
                self.total_location_count = 64 + self.options.reputation_locations_per_biome.value * 6 + self.options.extra_trade_locations.value
            logging.warning(f"[Against the Storm] Fewer locations than items detected in options, increasing \
                reputation_locations_per_biome to {self.options.reputation_locations_per_biome.value} to fit all items")
        
        self.included_location_indices.append(1)
        # This evenly spreads the option's number of locations between 2 and 17
        # Generating, for example, [10], [4, 8, 11, 15], or [2-17 sans 9]
        for i in range(self.options.reputation_locations_per_biome):
            self.included_location_indices.append(
                round(1 + (i + 1) * (17 / (self.options.reputation_locations_per_biome + 1))))

        # Recipe shuffle
        all_production = {}
        all_production.update(blueprint_recipes)
        all_production.update(nonitem_blueprint_recipes)
        if self.options.recipe_shuffle.value != "vanilla":
            while True: # Break at the bottom when `are_recipes_beatable`
                all_recipes: List[Tuple[str, int]] = []
                for blueprint, recipes in all_production.items():
                    if blueprint == "Crude Workstation" and self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws:
                        continue
                    for good, star_level in recipes.items():
                        all_recipes.append((good, star_level))
                for blueprint, recipes in all_production.items():
                    if blueprint == "Crude Workstation" and self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws:
                        self.production_recipes[blueprint] = list(map(list, recipes.items()))
                        continue
                    recipe_set: List[List] = []
                    for _ in range(len(recipes)):
                        recipe = all_recipes.pop(randrange(len(all_recipes)))
                        recipe_set.append([recipe[0], recipe[1]])
                    self.production_recipes[blueprint] = recipe_set
                # Verify all of a certain good didn't wind up in glade event buildings, as that wouldn't pass logic
                if self.are_recipes_beatable(self.production_recipes):
                    break
        else:
            self.production_recipes = { key:[[item, num] for item,num in value.items()] for key,value in all_production.items() if not isinstance(value, str) }

    def create_item(self, item: str) -> AgainstTheStormItem:
        return AgainstTheStormItem(item, item_dict.get(item)[0], self.item_name_to_id[item], self.player)

    def create_items(self) -> None:
        itempool = []
        filler_items = []
        # TODO switch on enum
        for item_key, item_value in item_dict.items():
            if item_value[1] == ATSItemClassification.filler:
                filler_items.append(item_key)
                continue
            if item_value[1] == ATSItemClassification.blueprint and not self.options.blueprint_items.value:
                continue
            if item_value[1] == ATSItemClassification.guardian_part and not self.options.seal_items.value:
                continue
            # ATSItemClassification.good
            itempool.append(item_key)
        
        # Fill remaining itempool space with filler
        while len(itempool) + len(filler_items) < self.total_location_count:
            itempool += filler_items
        itempool += sample(filler_items, self.total_location_count - len(itempool))
        
        self.multiworld.itempool += map(self.create_item, itempool)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_region = Region("Main", self.player, self.multiworld)
        # TODO just iterate over location_dict instead, since name_to_id is constructed from it
        # TODO switch on enum
        trade_locations = []
        for loc_key, loc_value in self.location_name_to_id.items():
            if location_dict[loc_key][0] == ATSLocationClassification.extra_trade:
                trade_locations.append(loc_key)
                continue
            if location_dict[loc_key][0] == ATSLocationClassification.biome_rep:
                loc_index = int(re.search(r"^(\d\d?)\w\w Reputation - .*$", loc_key).group(1))
                if loc_index in self.included_location_indices:
                    self.location_pool[loc_key] = loc_value
                continue
            if location_dict[loc_key][0] == ATSLocationClassification.basic:
                self.location_pool[loc_key] = loc_value
                continue
        trade_locations = sample(trade_locations, self.options.extra_trade_locations.value)
        for location in trade_locations:
            self.location_pool[location] = self.location_name_to_id[location]
        main_region.add_locations(self.location_pool, AgainstTheStormLocation)
        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)
    
    def can_goal(self, state: CollectionState) -> bool:
        if self.options.seal_items and not state.has_all(["Guardian Heart", "Guardian Blood", "Guardian Feathers", "Guardian Essence"], self.player):
            return False
        
        if self.options.required_seal_tasks.value > 1:
            return satisfies_recipe(state, self.player, self.production_recipes if self.options.blueprint_items.value else None,
                ['Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods', 'Ale,Training Gear,Incense,Scrolls,Wine,Tea',
                 'Coal,Oil,Sea Marrow', 'Amber', 'Tools', 'Purging Fire', 'Planks', 'Bricks', 'Fabric',
                 # Above is the baseline that ensures normal winnable conditions, below ensures every Seal task
                 'Pack of Crops', 'Pack of Provisions', 'Pack of Building Materials', 'Stone,Sea Marrow,Training Gear',
                 'Pipes', 'Parts', 'Ancient Tablet'])
        else:
            return satisfies_recipe(state, self.player, self.production_recipes if self.options.blueprint_items.value else None,
                ['Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods', 'Ale,Training Gear,Incense,Scrolls,Wine,Tea',
                 'Coal,Oil,Sea Marrow', 'Amber', 'Tools', 'Purging Fire', 'Planks', 'Bricks', 'Fabric'])
    
    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: self.can_goal(state)
        for location, loc_data in location_dict.items():
            if location not in self.location_pool.keys():
                continue
            set_rule(self.multiworld.get_location(location, self.player),
                     lambda state, logic=loc_data[1]: satisfies_recipe(state, self.player, self.production_recipes if self.options.blueprint_items.value else None, logic))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "recipe_shuffle": self.options.recipe_shuffle.value,
            "deathlink": self.options.deathlink.value,
            "blueprint_items": self.options.blueprint_items.value,
            "continue_blueprints_for_reputation": self.options.continue_blueprints_for_reputation.value,
            "seal_items": self.options.seal_items.value,
            "required_seal_tasks": self.options.required_seal_tasks.value,
            "rep_location_indices": self.included_location_indices,
            "production_recipes": self.production_recipes
        }
    