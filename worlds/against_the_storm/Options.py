from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, OptionSet


class RecipeShuffle(Choice):
    """Enable production building recipe shuffle. This includes glade events as well, such as the flawless buildings. Can skip Crude Workstation and/or Makeshift Post for less frustrating seeds.
    
    Options: vanilla, exclude_crude_ws_and_ms_post, exclude_crude_ws, exclude_ms_post, full_shuffle"""
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
    """When you get a duplicate item, what happens to it? No effect if Shuffle Duplicates is Off and no two Progressive
    series are active.

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
    """Enable death link. Can send on villager leaving and/or death.
    
    Options: off, death_only, leave_and_death"""
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
    """Shuffle 4 special Seal related items. You will not be able to complete a stage of the Seal until receiving the relevant item."""
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


class TotalBiomes(Range):
    """Set the maximum number of biomes the player will be expected to visit. For example, if you set this to 8, your
    Reputation locations will be distributed between Royal Woodlands, Cursed Royal Woodlands, Coral Forest, Scarlet
    Orchard, and Marshlands, as well as the DLC biomes Coastal Grove and Ashen Thicket. You may need to visit each biome
    to get all sphere 0 locations.

    In addition, you will always be expected to go to the Sealed Forest.

    If DLC is off, this can be no more than 6 and will be reduced if necessary."""
    display_name = "Total Biomes"
    default = 8
    range_start = 1
    range_end = 8


class ReputationLocationsPerBiome(Range):
    """Set the number of locations spread between the 1st reputation and victory (assumed to be at 18) in each biome.
    
    For example, a setting of 1 will put locations at the 1st, 10th, and 18th rep, while a setting of 4 will put
    locations at the 1st, 4th, 8th, 11th, 15th, and 18th rep. You might visit "Royal Woodlands - 1st Reputation" as well
    as "Scarlet Orchard - 1st Reputation".
    
    This option will be increased before generation with a warning to ensure enough locations for items, such as with
    Blueprint Items on."""
    display_name = "Reputation Locations Per Biome"
    default = 3
    range_start = 1
    range_end = 17


class ReputationLocationSlurry(Range):
    """Adds a number of locations up to some N reputation. Progress through this slurry is still tracked individually by
    biome, meaning you must still revisit individual biomes.

    For example, you might visit "1st Reputation" and then much later "69th Reputation". If you reach 5 reputation in
    the Royal Woodlands, and another 5 in the Coral Forest, and then return to the Royal Woodlands, you would need to
    reach 6 Reputation to reach your next location, "11th Reputation".

    If DLC is off, this can be no more than 102 and will be reduced if necessary."""
    display_name = "Reputation Location Slurry"
    default = 0
    range_start = 0
    range_end = 136


class TotalBiomesByTopPerformance(Range):
    """Set the maximum number of biomes the player will be expected to visit for high score purposes.

    For example, you might visit "Gold Biome - 1st Reputation", then leave the settlement, and at your next biome
    acquire "2nd Biome - 1st Reputation" followed by "Gold Biome - 2nd Reputation". Note that you would then continue to
    acquire "Gold Biome" locations in your new biome, while leaving to resume the previous biome would at first grant
    "2nd Biome" locations.

    If DLC is off, this can be no more than 6 and will be reduced if necessary."""
    display_name = "Total Biomes By Top Performance"
    default = 0
    range_start = 0
    range_end = 8


class ReputationLocationsPerBiomeByTopPerformance(Range):
    """As Reputation Locations Per Biome, but your progress in each is tracked agnostic to biome name. Disabled if Total
    Biomes By Top Performance is 0."""
    display_name = "Reputation Locations Per Biome By Top Performance"
    default = 3
    range_start = 1
    range_end = 17


class ExtraTradeLocations(Range):
    """Set the number of extra goods that will be chosen as trade route locations."""
    display_name = "Extra Trade Locations"
    default = 5
    range_start = 0
    range_end = 52


class ProgressiveGeneral(OptionSet):
    """Enable/disable progressive sequences of items and locations. This removes the corresponding named items. You will
    instead get a "Progressive Item", unlocking the next item in its sequence. For each enabled option below, you will
    receive its corresponding items in order. Duplicates of items granted by multiple sequences are handled by the
    Duplicate Item option.

    Guardian - Turns the 4 Guardian Parts into a single progressive sequence.

    Short Expedition - Amber, Pipes, Purging Fire, Packs of Provisions, Tools, Parts, Wildfire Essence, Ancient Tablets.

    Buildings - Planks, Fabric, Bricks, Parts.

    Trade - Amber, Packs of Provisions, Packs of Trade Goods, Packs of Building Materials, Packs of Luxury Goods,
    Packs of Crops.

    Metallurgy - Copper Bars, Scales, Copper Ore, Pipes, Tools, Parts.

    Fishing - Fish, Algae, Scales, Packs of Crops, Fishing Hut.
    """
    display_name = "Progressive"
    valid_keys = {
        "Guardian",
        "Short Expedition",
        "Building",
        "Trade",
        "Metallurgy",
        "Fishing",
    }


class ProgressiveComplexFood(Choice):
    """
    Similar to the general Progressive setting, but specific to Complex Food. This will always generate a "Progressive
    Complex Food" item, which will unlock the next Complex Food item in its sequence. This can make it easier to
    communicate with other players about important items.

    Off - Disabled. Your Complex Foods will be available as fixed items.

    Random - Puts the 7 Complex Food items into a single progressive sequence. The order is random within your seed!
    This simply guarantees that you'll find the complex food that your seed expects you to use for early Reputation.

    Cheap - Porridge, Jerky, Pie, Skewers, Paste, Pickled Goods, Biscuits. Wait, biscuits are expensive...?
    """
    display_name = "Progressive Complex Food"
    option_off = 0
    option_random = 1
    option_cheap = 2
    default = 0


@dataclass
class AgainstTheStormOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    recipe_shuffle: RecipeShuffle
    shuffle_duplicates: ShuffleDuplicates
    duplicates_acquired: DuplicatesAcquired
    deathlink: Deathlink
    blueprint_items: BlueprintItems
    continue_blueprints_for_reputation: ContinueBlueprintsForReputation
    seal_items: SealItems
    required_seal_tasks: RequiredSealTasks
    enable_dlc: EnableDLC
    grove_expedition_locations: GroveExpeditionLocations
    total_biomes: TotalBiomes
    reputation_locations_per_biome: ReputationLocationsPerBiome
    reputation_location_slurry: ReputationLocationSlurry
    total_biomes_by_top_performance: TotalBiomesByTopPerformance
    reputation_locations_per_biome_by_top_performance: ReputationLocationsPerBiomeByTopPerformance
    extra_trade_locations: ExtraTradeLocations
    progressive: ProgressiveGeneral
    progressive_complex_food: ProgressiveComplexFood
