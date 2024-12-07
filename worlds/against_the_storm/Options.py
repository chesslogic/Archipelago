from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, OptionSet


class RecipeShuffle(Choice):
    """Enable production building recipe shuffle. Will maintain the number of recipes available for goods and buildings. This includes glade events as well, such as the flawless buildings! Can skip Crude Workstation and/or Makeshift Post for less frustrating seeds."""
    display_name = "Recipe Shuffle"
    option_vanilla = 0
    option_exclude_crude_ws_and_ms_post = 1
    option_exclude_crude_ws = 2
    option_exclude_ms_post = 3
    option_full_shuffle = 4
    default = 0


class ShuffleDuplicates(Choice):
    """Enable shuffling duplicate items for certain items:

    Off: Disabled. Each item will only be available from one location.
    Essential: Adds two additional copies each of Amber, Pipes, Parts, Purging Fire, Packs of Provisions.
    Many: Adds just one each from the above and the following: Planks, Fiber, Bricks, Tools, and Packs of Crops."""
    display_name = "Shuffle Duplicates"
    option_off = 0
    option_essential = 1
    option_many = 2
    default = 0


class DuplicatesAcquired(Choice):
    """When you get a duplicate item, what happens to it? No effect if Shuffle Duplicates is Off.

    First: The first item you get has full impact, while later copies are ignored.
    Resources: Each additional copy you get is converted into an amount of Starting Resources corresponding to its type.
    Productive: Each additional copy you get gives you a 10% chance to double your yield (from ALL sources, after ALL
    modifiers, once embarked!). May not affect Progressive items and does not accelerate cornerstone progress."""
    display_name = "Duplicates Acquired"
    option_first = 0
    option_resources = 1
    option_productive = 2
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
    """Increase the number of tasks you need to complete at each stage of the Seal, making the final settlement MUCH
    harder.

    In vanilla, you need to complete 1 task at each of the 4 stages. This can add more tasks before each cornerstone.
    Note that you still need to complete at least 1 task at each stage after acquiring the Guardian items!"""
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

class ReputationLocationMode(Choice):
    """Select the mode for the reputation biome distribution.

    Reputation By Biome: Places locations at the reputation indices in each biome. You may need to visit each biome to
    get all sphere 0 locations. For example, you might visit "Royal Woodlands - 1st Reputation" as well as "Scarlet
    Orchard - 1st Reputation".
    Reputation Slurry: Appends each reputation location in order. Your progress is still tracked individually by biome.
    For example, you might visit "1st Reputation" and then much later "69th Reputation"."""
    display_name = "Reputation Location Mode"
    option_by_biome = 0
    option_slurry = 1
    default = 0

class ExtraTradeLocations(Range):
    """Set the number of extra goods that will be chosen as trade route locations."""
    display_name = "Extra Trade Locations"
    default = 5
    range_start = 0
    range_end = 52

class Progressive(OptionSet):
    """Enable/disable progressive sequences of items and locations. This means you will not get named items, and will
    instead get a "Progressive Item" instead, unlocking the next item in its sequence. This can make communicating with
    other players about important items  easier, although it will also reduce the potential variance between different
    seeds.

    For each enabled option below, you will receive its corresponding items in order. Duplicates of items granted by
    multiple sequences are handled by the Duplicate Item option.

    Guardian - Turns the 4 Guardian Parts into a single progressive sequence.
    Short Expedition - Amber, Pipes, Purging Fire, Packs of Provisions, Tools, Wildfire Essence, Ancient Tablets.
    Building - Planks, Fabric, Bricks, Parts.
    """
    display_name = "Progressive"
    valid_keys = {
        "Guardian",
        "Short Expedition",
        "Building",
    }

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
    reputation_location_mode: ReputationLocationMode
    extra_trade_locations: ExtraTradeLocations
    progressive: Progressive
