# Against The Storm

## What does randomization do to this game?
All resources are blocked from being acquired until their Item is received from Archipelago.
If blueprints are shuffled, the standard means of acquiring them by reputation draft rewards will be disabled.
Optionally, all production recipes can be shuffled.

## What Against The Storm items are randomized?
"Items" in this case are the ability to acquire the blocked resources. 
The exceptions to this are you can always gather Wood and Water, and you will always receive resources from embarkation and deconstruction.
In addition, blueprints can be shuffled as well, and will be added as essential bluperints for every settlement once received from the multiworld.

## What do Locations look like in Against the Storm?
Locations are essentially just a list of custom deeds designed to cover many aspects of the game. Here is an overview of them:

* Species
    * Earn your first Reputation through Resolve for each species
    * Bring a species to 50 Resolve for each species
    * Win a game with 20 villagers in fully upgraded housing for each species
* Biomes
    * Earn a configurable amount of Reputation for each biome
    * Achieve a victory in each biome
* Trade
    * *These work by turning in the given resources to a custom neighbor found in the trade route menu*
        * 5, 50, and 500 Amber
        * 20 of each of the packs
        * 200 of each of the waters
        * A configurable number of addition random resources
    * Reach level 1-5 standing with one/all 4 trade neighbors
* Others
    * Complete an order in each of the first 9 slots
    * Upgrade a hearth to each tier
    * Complete a Dangerous & Forbidden glade event
    * Complete a glade event of each decision type

## What is the goal of this game when randomized?
To gather the guardian parts and reforge a seal in the sealed forest. Note: you can play the sealed forest from the Training Expedition as well!

## Known Issues as of v0.5.0
* If a filler item is received while disconnected in the middle of the settlement, the filler won't be received until the start of the next settlement.
* The trade related locations, because they are handled by trade routes, proc trade route related in game effects.
* With `blueprint_items` on, the reputation blueprint reward button doesn't correctly disable if you connect during a run. When your reward changes, it should correct itself.
