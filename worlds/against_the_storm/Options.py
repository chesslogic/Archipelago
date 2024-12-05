from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool

class RecipeShuffle(Choice):
    """Enable production building recipe shuffle. Will maintain the number of recipes available for goods and buildings. This includes glade events as well, such as the flawless buildings! Can skip Crude Workstation and/or Makeshift Post for less frustrating seeds."""
    display_name = "Recipe Shuffle"
    option_vanilla = 0
    option_exclude_crude_ws_and_ms_post = 1
    option_exclude_crude_ws = 2
    option_exclude_ms_post = 3
    option_full_shuffle = 4
    default = 0

class Deathlink(Choice):
    """Enable death link. Can send on villager leaving and/or death."""
    display_name = "Death Link"
    option_off = 0
    option_death_only = 1
    option_leave_and_death = 2
    default = 0

class BlueprintItems(Toggle):
    """Blueprints are no longer drafted through Reputation like in Vanilla. Instead, they are found as items, granting them as essential blueprints. This will make the start of a multiworld quite a bit harder, but the end quite a bit easier."""
    display_name = "Blueprint Items"

class ContinueBlueprintsForReputation(Toggle):
    """Continue to offer blueprint selections as rewards for reputation, even with Blueprint Items on."""
    display_name = "Continue Blueprints For Reputation"

class SealItems(DefaultOnToggle):
    """Shuffle 4 Seal related items. You will not be able to complete a stage of the Seal until receiving the relevant item."""
    display_name = "Seal Items"

class RequiredSealTasks(Range):
    """Increase the number of tasks you need to complete at each stage of the Seal, making the final settlement MUCH harder."""
    display_name = "Required Seal Tasks"
    default = 1
    range_start = 1
    range_end = 3
    
class EnableDLC(Toggle):
    """Enable DLC related locations, such as Frog resolve and Coastal Grove reputation."""
    display_name = "Enable DLC"
    
class GroveExpeditionLocations(Range):
    """Number of locations to place in the Coastal Grove's Strider Port. Will be ignored if DLC is off."""
    display_name = "Coastal Grove Expedition Locations"
    default = 4
    range_start = 0
    range_end = 20

class ReputationLocationsPerBiome(Range):
    """Set the number of locations spread between the 1st and 18th reputation in each biome. For example, a setting of 1
    will put locations at the 1st, 10th, and 18th rep, while a setting of 4 will put locations at the 1st, 4th,
    8th, 11th, 15th, and 18th rep.
    This option will be increased before generation with a warning when Blueprint Items is on to ensure enough locations."""
    display_name = "Reputation Locations Per Biome"
    default = 3
    range_start = 1
    range_end = 16

class ExtraTradeLocations(Range):
    """Set the number of extra goods that will be chosen as trade route locations."""
    display_name = "Extra Trade Locations"
    default = 5
    range_start = 0
    range_end = 52

@dataclass
class AgainstTheStormOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    recipe_shuffle: RecipeShuffle
    deathlink: Deathlink
    blueprint_items: BlueprintItems
    continue_blueprints_for_reputation: ContinueBlueprintsForReputation
    seal_items: SealItems
    required_seal_tasks: RequiredSealTasks
    enable_dlc: EnableDLC
    grove_expedition_locations: GroveExpeditionLocations
    reputation_locations_per_biome: ReputationLocationsPerBiome
    extra_trade_locations: ExtraTradeLocations
