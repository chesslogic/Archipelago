from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions

class LogicDifficulty(Toggle):
    """How minimal the logic should be."""
    display_name = "Logic Difficulty"

class Deathlink(Toggle):
    """Enable death link."""
    display_name = "Death Link"

@dataclass
class AgainstTheStormOptions(PerGameCommonOptions):
    # logic_difficulty: LogicDifficulty
    deathlink: Deathlink