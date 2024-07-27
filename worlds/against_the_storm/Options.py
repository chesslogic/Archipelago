from dataclasses import dataclass
from Options import Choice, Toggle, Range, PerGameCommonOptions

class RecipeShuffle(Choice):
    """Enable production building recipe shuffle. Can skip Crude WS for less frustrating seeds."""
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

class ReputationLocationsPerBiome(Range):
    """Set the number of locations spread between the 1st and 18th reputation in each biome. This option will be capped to a minimum of 11 when Blueprint Items is on to ensure enough locations."""
    display_name = "Reputation Locations Per Biome"
    default = 1
    range_start = 1
    range_end = 16

@dataclass
class AgainstTheStormOptions(PerGameCommonOptions):
    recipe_shuffle: RecipeShuffle
    deathlink: Deathlink
    blueprint_items: BlueprintItems
    reputation_locations_per_biome: ReputationLocationsPerBiome
