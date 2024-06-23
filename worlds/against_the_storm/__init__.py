from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import Region

from .Items import AgainstTheStormItem, item_dict
from .Locations import AgainstTheStormLocation, location_dict
from .Options import AgainstTheStormOptions
from .Recipes import satisfies_recipe

class AgainstTheStormWorld(World):
    """
    Against The Storm is a roguelite city builder
    """

    game = "Against The Storm"
    options_dataclass = AgainstTheStormOptions
    options: AgainstTheStormOptions
    topology_present = True
    base_id = 9999000000
    item_name_to_id = {item: id for id, item in enumerate(item_dict.keys(), base_id)}
    location_name_to_id = {location: id for id, location in enumerate(location_dict.keys(), base_id)}

    def create_item(self, item: str) -> AgainstTheStormItem:
        return AgainstTheStormItem(item, item_dict[item][0], self.item_name_to_id[item], self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_region = Region("Main", self.player, self.multiworld)
        main_region.add_locations(self.location_name_to_id, AgainstTheStormLocation)
        self.multiworld.regions.append(main_region)

        menu_region.connect(main_region)

    def create_items(self) -> None:
        for item_key, item_value in item_dict.items():
            for count in range(item_value[1]):
                self.multiworld.itempool.append(self.create_item(item_key))
    
    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: satisfies_recipe(state, self.player,
                ['Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods', 'Ale,Training Gear,Incense,Scrolls,Wine,Tea', 'Coal,Oil,Sea Marrow', 'Amber', 'Tools', 'Purging Fire', 'Planks', 'Bricks', 'Fabric'])
        for location, logic in location_dict.items():
            print(f"Loc: {location}|{logic}") # DELETEME
            set_rule(self.multiworld.get_location(location, self.player), lambda state, logic=logic: satisfies_recipe(state, self.player, logic))
    