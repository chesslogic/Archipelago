from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions

class RecipeShuffle(Choice):
    """Enable production building recipe shuffle. Will maintain the number of recipes available for goods and buildings. This includes glade events as well, such as the flawless buildings! Can skip Crude WS for less frustrating seeds."""
    display_name = "Recipe Shuffle"
    option_vanilla = 0
    option_exclude_crude_ws = 1
    option_full_shuffle = 2
    default = 0

class Deathlink(Choice):
    """Enable death link. Can send on villager leaving and/or death."""
    display_name = "Death Link"
    option_off = 0
    option_death_only = 1
    option_leave_and_death = 2
    default = 0

class BlueprintItems(Toggle):
    """Blueprints are no longer drafted through Reputation like in Vanilla. Instead, they are found as items, granting them as essential blueprints."""
    display_name = "Blueprint Items"

class ContinueBlueprintsForReputation(Toggle):
    """Continue to offer blueprint selections as rewards for reputation, even with Blueprint Items on."""
    display_name = "Continue Blueprints For Reputation"

class SealItems(Toggle):
    """Shuffle 4 Seal related items. You will not be able to complete a stage of the Seal until receiving the relevant item."""
    display_name = "Seal Items"

class RequiredSealTasks(Range):
    """Increase the number of tasks you need to complete at each stage of the Seal, making the final settlement MUCH harder."""
    display_name = "Required Seal Tasks"
    default = 1
    range_start = 1
    range_end = 3

class ReputationLocationsPerBiome(Range):
    """Set the number of locations spread between the 1st and 18th reputation in each biome. This option will be increased before generation with a warning when Blueprint Items is on to ensure enough locations."""
    display_name = "Reputation Locations Per Biome"
    default = 1
    range_start = 1
    range_end = 16

class ExtraTradeLocations(Range):
    """Set the number of goods that will be chosen as additional trade locations."""
    display_name = "Extra Trade Locations"
    default = 0
    range_start = 0
    range_end = 46

@dataclass
class AgainstTheStormOptions(PerGameCommonOptions):
    recipe_shuffle: RecipeShuffle
    deathlink: Deathlink
    blueprint_items: BlueprintItems
    continue_blueprints_for_reputation: ContinueBlueprintsForReputation
    seal_items: SealItems
    required_seal_tasks: RequiredSealTasks
    reputation_locations_per_biome: ReputationLocationsPerBiome
    extra_trade_locations: ExtraTradeLocations
