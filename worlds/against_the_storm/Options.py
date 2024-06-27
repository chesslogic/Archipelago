from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions

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

@dataclass
class AgainstTheStormOptions(PerGameCommonOptions):
    recipe_shuffle: RecipeShuffle
    deathlink: Deathlink