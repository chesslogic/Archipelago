from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, OptionSet


class RecipeShuffle(OptionSet):
    """Enable production building recipe shuffle. This includes glade events as well, such as the flawless buildings.
    Can skip Crude Workstation and/or Makeshift Post and/or Field Kitchen for less frustrating seeds.

    Alternatively, if you only want to shuffle your essential blueprints among each other, you can do that by excepting
    them while leaving shuffle disabled. This only shuffles essential recipes; no high-star recipes are in their pool.
    
    Options: Disable, Except Crude Workstation, Except Makeshift Post, Except Field Kitchen"""
    display_name = "Recipe Shuffle"
    valid_keys = {
        "Enable",
        "Except Crude Workstation",
        "Except Makeshift Post",
        "Except Field Kitchen"
    }


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
    modifiers, once embarked!). Certain items become thematic Perks (Amber -> Bed and Breakfast).
    May not affect all Progressive items and never accelerates cornerstone progress (e.g. Spices)."""
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


class EnableReputationLocations(OptionSet):
    """Set the progressive Reputation Locations that will be enabled. Options are Biomes, Species, BiomeAndSpecies,
    HighScore, and Slurry. You may enable any number of options.

    Biomes will generate locations up to Total Biomes times Reputation Locations Per Biome (plus 1 for victory), or 144
    locations. Enabling Biomes is strongly recommended and the presumed way to play this mod.

    Species will generate locations up to Total Species Sets times Reputation Locations Per Species Set (plus 1 for
    victory), or 360 locations.

    BiomeAndSpecies will generate locations up to the Total Biomes times the Total Species times the lesser of the two
    Reputation Locations settings (plus 1 for victory), or 2880 locations. If you enable this option, consider also
    setting a moderate number of DistinctSettlements.

    HighScore will generate locations up to the Total Biomes By Top Performance times the Reputation
    Locations Per Biome (plus 1 for victory), or 144 locations.

    Slurry will generate locations up to the Reputation Slurry limit."""
    display_name = "Enable Reputation Locations"
    valid_keys = {
        "Biomes",
        "Species",
        "BiomeAndSpecies",
        "HighScore",
        "Slurry",
    }


class ReputationLocations(Range):
    """For each Enabled Reputation Location track, configures the number of locations spread between the 1st reputation
    and victory (assumed to be at 18).

    For example, a setting of 1 will put locations at the 1st, 10th, and 18th rep, while a setting of 4 will put
    locations at the 1st, 4th, 8th, 11th, 15th, and 18th rep. With the Biomes setting,

    This option will be increased before generation with a warning to ensure enough locations for items, such as with
    Blueprint Items on.

    This setting is ignored if Biome and BiomeAndSpecies are disabled in the Enable Reputation Locations option and
    the High Score Style is not Biome."""
    display_name = "Reputation Locations"
    default = 3
    range_start = 1
    range_end = 17


class TotalBiomes(Range):
    """Set the maximum number of biomes the player will be expected to visit. For example, if you set this to 8, your
    Reputation locations will be distributed between Royal Woodlands, Cursed Royal Woodlands, Coral Forest, Scarlet
    Orchard, and Marshlands, as well as the DLC biomes Coastal Grove and Ashen Thicket. You might visit "Royal Woodlands
    - 1st Reputation" as well as "Scarlet Orchard - 1st Reputation".

    You will always be expected to go to the Sealed Forest. You may need to visit each biome to get all sphere 0
    locations.

    If DLC is off, this can be no more than 6 and will be reduced if necessary.

    This setting is ignored if Biome and BiomeAndSpecies are disabled in the Enable Reputation Locations option."""
    display_name = "Total Biomes"
    default = 8
    range_start = 1
    range_end = 8


class TotalSpeciesSets(Range):
    """Set the maximum number of Species sets the player will be expected to visit. For example, if you set this to 3,
    your Reputation locations might be distributed between "Human Beaver Lizard", "Harpy Fox Frog", and "Harpy Beaver
    Lizard". You might visit "Human Beaver Lizard - 1st Reputation" as well as "Harpy Fox Frog  - 1st Reputation".

    If DLC is off, this can be no more than 15 and will be reduced if necessary.

    This setting is ignored if Species and BiomeAndSpecies are disabled in the Enable Reputation Locations option."""
    display_name = "Total Species Sets"
    default = 4
    range_start = 1
    range_end = 20


class DistinctSettlements(Range):
    """Set the maximum number of distinct settlements the player will be expected to visit. For example, if you set
    Total Biomes to 5 and this setting to 20, you may be expected to visit each biome with 4 different Species
    configurations. You might visit "Human Beaver Lizard on Marshlands - 1st Reputation" as well as "Harpy Fox Frog on
    Royal Woodlands - 1st Reputation".

    Setting this lower may put more onerous expectations on your expedition configuration (such as
    specific combinations of biome and Species), while setting this higher may reduce the number of Reputation locations
    per settlement (and therefore your checks-per-minute).

    This option has a maximum of Total Biomes times Total Species Sets. If DLC is off, this can be no more than 90 and
    will be reduced if necessary.

    This setting is ignored if BiomeAndSpecies is disabled in the Enable Reputation Locations option."""
    display_name = "Distinct Settlements"
    default = 6
    range_start = 2
    range_end = 160


class HighScoreStyle(Choice):
    """Set the Top Performance tracking style, which identifies how the player competes with past high scores. When you
    achieve a new personal best among settlements of the type you specify, you will achieve a location.

    Options are: "Settlement", "Biome", "Species", and "BiomeAndSpecies". Settlement allows a new personal best in each
    settlement. Even if you use the exact same settings 5 times in a row, you would achieve a new high score placement.
    The remainder are tied to their option, so Top Biome means you would need to change biomes to progress on 2nd Place.

    For example, you might visit "Gold Biome - 1st Reputation", then leave the settlement, and at your next biome
    acquire "2nd Biome - 1st Reputation" followed by "Gold Biome - 2nd Reputation". Note that you would then continue to
    acquire "Gold Biome" locations in your new biome, while leaving to resume the previous biome would at first grant
    "2nd Biome" locations."""
    display_name = "High Score Style"
    option_settlement = 0
    option_biome = 1
    option_species = 2
    option_biome_and_species = 3
    default = 1


class TotalHighScorePlaces(Range):
    """Set the maximum number of places in the high score table the player will be expected to visit, e.g. "1st
    Reputation - 3rd Place". Uses the same maximum Reputation Locations as the corresponding setting, based on High
    Score Style."""
    display_name = "Total High Score Places"
    default = 1
    range_start = 1
    range_end = 6


class ReputationLocationSlurry(Range):
    """Adds a number of locations up to some N reputation. Progress through this slurry is still tracked individually by
    the other conditions you've enabled, such as by biome, meaning you must still revisit individual biomes.

    For example, you might visit "1st Reputation" and then much later "69th Reputation". If you reach 5 reputation in
    the Royal Woodlands, and another 5 in the Coral Forest, and then return to the Royal Woodlands, you would need to
    reach 6 Reputation to reach your next location, "11th Reputation".

    If any Enabled Reputation Location could have generated a Location, whether that Reputation index was populated by
    Reputation Locations, it will also be counted in the slurry. For example, if you only have "1st Reputation -
    Marshlands" and "Victory - Marshlands", Reputation Slurry could still access up to 18 locations in the Marshlands.

    If this is the only Enabled Reputation Location, it will determine the above behaviour using the High Score Style
    setting."""
    display_name = "Reputation Location Slurry"
    default = 0
    range_start = 0
    range_end = 136


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

    Archaeology - Locations. Turns the 3 fully reconstructed Archaeology Sites into a single progressive sequence. You
    will have to reconstruct all 3 Sites, potentially across different settlements, to get all 3 items.

    Short Expedition - Amber, Pipes, Purging Fire, Packs of Provisions, Tools, Parts, Wildfire Essence, Ancient Tablets.

    Buildings - Planks, Fabric, Bricks, Parts.

    Trade - Amber, Packs of Provisions, Packs of Building Materials, Packs of Crops, Packs of Trade Goods,
    Packs of Luxury Goods.

    Metallurgy - Copper Bars, Scales, Copper Ore, Pipes, Tools, Parts.

    Fishing - Fish, Algae, Scales, Packs of Crops, Fishing Hut.
    """
    display_name = "Progressive"
    valid_keys = {
        "Guardian",
        "Archaeology",
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


class Traps(OptionSet):
    """Enable specific traps. This will remove any other traps."""
    display_name = "Traps"
    valid_keys = {
        "Impatience",
    }


class TrapReplacementRate(Range):
    """Set the percentage of traps in the pool. 100 will replace all filler with traps."""
    display_name = "Trap Replacement Rate"
    default = 100
    range_start = 0
    range_end = 100


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
    enable_reputation_locations: EnableReputationLocations
    reputation_locations: ReputationLocations
    total_biomes: TotalBiomes
    total_species_sets: TotalSpeciesSets
    distinct_settlements: DistinctSettlements
    high_score_style: HighScoreStyle
    total_high_score_places: TotalHighScorePlaces
    reputation_location_slurry: ReputationLocationSlurry
    extra_trade_locations: ExtraTradeLocations
    progressive: ProgressiveGeneral
    progressive_complex_food: ProgressiveComplexFood
    traps: Traps
    trap_replacement_rate: TrapReplacementRate
