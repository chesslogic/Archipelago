# Against the Storm for Archipelago Setup and Usage Guide

## Required Software
* Latest release of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Currently tested/working on version 0.4.6.
* [Thunderstore Mod Manager](https://www.overwolf.com/app/thunderstore-thunderstore_mod_manager). (While a mod manager is not technically required, this guide will walk through using it to set up the mod)
* The `against_the_storm.apworld` from the latest [Against The Storm for Archipelago](https://github.com/RyanCirincione/ArchipelagoATS/releases) release.
* A legal copy of Against the Storm (working as of v1.3.4).
   * Only tested on Steam version.

## Installing the Archipelago Mod to Against the Storm
1. Open the Thunderstore Mod Manager.
2. Search for the game Against the Storm and select it. (The first time I did while modding, the game didn't appear. Just closing and reopening Thunderstore I think worked for me)
3. Click Select Profile.
    - Optional: Create a new modding profile and name, if you don't want to use the Default
4. Click the Get Mods tab.
5. Find the Against The Storm for Archipelago mod, and download it.

## Generating and Hosting a Seed
* If you are unfamiliar with Archipelago, I recommend reading through the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en) to gain an understanding of how Archipelago works and to better understand the steps below. This is *not* the kind of randomizer you might be expecting!
1. Download the `against_the_storm.apworld` and `AgainstTheStorm.yaml` files from the latest [Against The Storm for Archipelago](https://github.com/RyanCirincione/ArchipelagoATS/releases) release.
2. Put the `against_the_storm.apworld` file in the `/Archipelago/lib/worlds` folder where you installed Archipelago.
3. Edit the `AgainstTheStorm.yaml`.
    1. Don't worry too much about the `name` if you're just trying this out on your own. The slot name would be more relevant if you are playing an Archipelago Multiworld.
    2. The `deathlink` options are `off`, `death_only`, and `leave_and_death`. Again, don't worry about this if you're unfamiliar with Archipelago, the default is fine.
    3. The `recipe_shuffle` options are `vanilla`, `exclude_crude_ws`, and `full_shuffle`. The non-vanilla options will rearrange all production recipes in the game!
4. Place the edited `AgainstTheStorm.yaml` in the `/Archipelago/Players` folder.
5. Run `ArchipelagoGenerate.exe` from the `/Archipelago` folder.
6. Upload the `AP_#######.zip` file from `/Archipelago/output` to [Archipelago website](https://archipelago.gg/uploads) to host the game.

## Joining an Archipelago Game in Against The Storm
* Optional: backup your save files located in `%userprofile%\AppData\LocalLow\Eremite Games\Against the Storm`
1. Go to Thunderstore Mod Manager, open your Against the Storm profile with the Against the Storm for Archipelago mod, and click the blue Modded play button.
* Optional: from the main menu, start a separate profile in the top right if you already have data in your default profile.
* Optional: especially if you started a new profile from above, you will almost certainly want to run `meta.addAll` from the dev console, as the mod will assume you have all meta progression unlocked. The dev console is opened with \` (backtick, to the left of 1 on keyboards) by default, and at least for me only opens in the world map or settlements.
  * If you run `meta.allAll` on a fresh profile, the Training Expedition will still appear locked. This is a bug in the game's UI. Just enter and leave the Smoldering Citadel, and you should now see the Training Expedition available.
2. From the world map, open the dev console (default \` (backtick, to the left of 1 on keyboards)) and type `ap.connect <url>:<port> "<slotName>" [password]`.
    * If you uploaded `AP_#######.zip` to archipelago, then the room you generated should have the url: `archipelago.gg:#####`
    * slotName is the name from the `AgainstTheStorm.yaml`. The default was `ATSPlayer` if you didn't change it. The quotes are only necessary if the name you set has spaces.
    * password is only necessary if you added a password to your yaml.
3. In the game, start a settlement from the Training Expedition menu. (The mod should also work on any world settlements, you will just have more control over your game from the Training Expedition)
* Optional: you will probably want to use the Templates option in the top left to set up your preferred Training Expedition only once. Note: all three of these columns can scroll!
    * *Column 1*
    * Don't forget to randomize your Seed each game! Or don't, I won't stop you.
    * Also don't forget to choose your Biome and Species, if you're looking to check certain locations in particular.
    * Feel free to choose any difficulty. The order locations only go up to slot #9, so you can still reach everything from Viceroy.
    * Set your Reputation to 18. Or, again, whatever you want, I won't stop you. Mod is just balanced around the expectation of 18.
    * 4 minute Storm duration is found here under Reputation/Impatience, rather than as a Prestige modifier.
    * *Column 2*
    * Select 4 neighboring towns for a typical trade experience.
    * Determine your embarkation goods. The default here is much more brutal than the usual embarkation. Here is what I tested with, designed as a mix of the base embarkation package, and some extra basic resources:
        * 70 Wood
        * 28 Coal
        * 6 Wildfire Essence
        * 28 Parts
        * 14 Pipes
        * 42 Eggs
        * 28 Roots
        * 28 Vegetables
        * 28 Meat
        * 28 Mushrooms
        * 28 Insects
        * 28 Berries
        * 7 Planks
        * 7 Fabric
        * 7 Bricks
    * *Column 3*
    * The mod shouldn't be affected by any modifiers, so feel free to add them if you want to spice up your run.
    * Below the map modifiers is where you will find the Prestige modifiers, which should roughly be in the order you get them from climbing Prestige. (Note the missing storm duration modifier, as mentioned above)
4. Click Embark.
5. Lastly, you will probably want to be able to monitor which Locations you have checked, and which Items you have received. You can do that either from the tracker available in the room you generated on the archipelago website, or by opening the Archipelago Text Client which should have come with the Archipelago installation. Note that the website tracker can take a little while to update.
