from random import randrange, sample
import re
import logging
from typing import Any, Dict
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import ItemClassification, Region

from .Items import ATSClassification, AgainstTheStormItem, item_dict
from .Locations import AgainstTheStormLocation, location_dict
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
    production_recipes: Dict[str, Dict[str, int]] = {}

    def generate_early(self):
        if self.options.blueprint_items.value and self.options.reputation_locations_per_biome.value < 11:
            logging.warning(f"Option blueprint_items detected, with reputation_locations_per_biome set to \
                {self.options.reputation_locations_per_biome.value}, increasing reputation_locations_per_biome to 11")
            self.options.reputation_locations_per_biome.value = max(self.options.reputation_locations_per_biome.value, 11)
        self.total_location_count = 60 + self.options.reputation_locations_per_biome.value * 5

        self.included_location_indices.append(1)
        for i in range(self.options.reputation_locations_per_biome):
            # This evil evenly spreads the option's number of locations between 2 and 17
            # Generating, for example, [10], [4, 8, 11, 15], or [2-17 sans 9]
            self.included_location_indices.append(
                round(1 + (i + 1) * (17 / (self.options.reputation_locations_per_biome + 1))))

        # Recipe shuffle
        all_production = {}
        all_production.update(blueprint_recipes)
        all_production.update(nonitem_blueprint_recipes)
        if self.options.recipe_shuffle.value != "vanilla":
            all_recipes = []
            for blueprint, recipes in all_production.items():
                if blueprint == "Crude Workstation" and self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws:
                    continue
                for good, star_level in recipes.items():
                    all_recipes.append((good, star_level))
            for blueprint, recipes in all_production.items():
                if blueprint == "Crude Workstation" and self.options.recipe_shuffle.value == RecipeShuffle.option_exclude_crude_ws:
                    self.production_recipes[blueprint] = list(map(list, recipes.items()))
                    continue
                recipe_set = []
                for _ in range(len(recipes)):
                    recipe = all_recipes.pop(randrange(len(all_recipes)))
                    recipe_set.append([recipe[0], recipe[1]])
                self.production_recipes[blueprint] = recipe_set
        else:
            self.production_recipes = { key:[[item, num] for item,num in value.items()] for key,value in all_production.items() if not isinstance(value, str) }

    def create_item(self, item: str) -> AgainstTheStormItem:
        return AgainstTheStormItem(item, item_dict.get(item)[0], self.item_name_to_id[item], self.player)

    def create_items(self) -> None:
        itempool = []
        filler_items = []
        for item_key, item_value in item_dict.items():
            if item_value[1] == ATSClassification.filler:
                filler_items.append(item_key)
                continue
            if item_value[1] == ATSClassification.blueprint and not self.options.blueprint_items.value:
                continue
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
        for loc_key, loc_value in self.location_name_to_id.items():
            search_result = re.search(r"^(\d\d?)\w\w Reputation - .*$", loc_key)
            if search_result is None:
                self.location_pool[loc_key] = loc_value
            else:
                loc_index = int(search_result.group(1))
                if loc_index in self.included_location_indices:
                    self.location_pool[loc_key] = loc_value
        main_region.add_locations(self.location_pool, AgainstTheStormLocation)
        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)
    
    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: satisfies_recipe(state, self.player,self.production_recipes if self.options.blueprint_items.value else None,
                ['Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods', 'Ale,Training Gear,Incense,Scrolls,Wine,Tea',
                 'Coal,Oil,Sea Marrow', 'Amber', 'Tools', 'Purging Fire', 'Planks', 'Bricks', 'Fabric'])
        for location, logic in location_dict.items():
            if location not in self.location_pool.keys():
                continue
            set_rule(self.multiworld.get_location(location, self.player),
                     lambda state, logic=logic: satisfies_recipe(state, self.player, self.production_recipes if self.options.blueprint_items.value else None, logic))

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "deathlink": self.options.deathlink.value,
            "recipe_shuffle": self.options.recipe_shuffle.value,
            "blueprint_items": self.options.blueprint_items.value,
            "rep_location_indices": self.included_location_indices,
            "production_recipes": self.production_recipes
        }
    