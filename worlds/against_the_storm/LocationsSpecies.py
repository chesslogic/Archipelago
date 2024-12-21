from random import randrange
from typing import Dict, List, Tuple
from itertools import combinations

from .Locations import ATSLocationClassification

def select_species_combinations(species_list: List[str], total_sets: int) -> List[Tuple[str, str, str]]:
    """Select species combinations ensuring relatively even distribution of species."""
    
    # Get all possible 3-species combinations
    all_combinations = list(combinations(species_list, 3))
    
    if total_sets >= len(all_combinations):
        return all_combinations
        
    # Count species occurrences for scoring combinations
    def score_combination(selected_combos: List[Tuple[str, str, str]], new_combo: Tuple[str, str, str]) -> int:
        species_counts = {species: 0 for species in species_list}
        # Count existing selections
        for combo in selected_combos:
            for species in combo:
                species_counts[species] += 1
        # Add potential new combination
        for species in new_combo:
            species_counts[species] += 1
        # Lower score is better (less variance in species distribution)
        return max(species_counts.values()) - min(species_counts.values())
    
    selected_combinations = []
    # Start with a random combination
    selected_combinations.append(all_combinations.pop(randrange(len(all_combinations))))
    
    # Select remaining combinations
    while len(selected_combinations) < total_sets:
        best_score = float('inf')
        best_combo = None
        best_index = 0
        
        # Try each remaining combination
        for i, combo in enumerate(all_combinations):
            score = score_combination(selected_combinations, combo)
            if score < best_score:
                best_score = score
                best_combo = combo
                best_index = i
                
        selected_combinations.append(best_combo)
        all_combinations.pop(best_index)
    
    return selected_combinations

def generate_species_combination_locations(selected_combinations: List[Tuple[str, str, str]]) -> Dict[str, Tuple[ATSLocationClassification, List[str]]]:
    """Generate location definitions for all selected three-species combinations."""
    
    # Define base preferences for each species
    species_preferences = {
        "Human": {
            "building": ["Planks", "Bricks"],
            "food": ["Biscuits", "Pie", "Porridge"],
            "service": ["Ale", "Incense"]
        },
        "Beaver": {
            "building": ["Planks"],
            "food": ["Biscuits", "Pickled Goods"],
            "service": ["Ale", "Scrolls", "Wine"]
        },
        "Lizard": {
            "building": ["Bricks", "Fabric"],
            "food": ["Jerky", "Pickled Goods", "Pie", "Skewers"],
            "service": ["Training Gear"]
        },
        "Harpy": {
            "building": ["Fabric"],
            "food": ["Jerky", "Paste"],
            "service": ["Scrolls", "Tea"]
        },
        "Fox": {
            "building": ["Planks", "Crystallized Dew"],
            "food": ["Pickled Goods", "Porridge", "Skewers"],
            "service": ["Incense", "Tea"]
        },
        "Frog": {
            "building": ["Bricks"],
            "food": ["Paste", "Pie", "Porridge"],
            "service": ["Training Gear", "Incense", "Wine"]
        }
    }

    locations = {}
    
    # Generate all 3-species combinations
    for combo in selected_combinations:
        related_items = getRelatedItems(combo, species_preferences)
        # Generate location name and requirements
        combo_name = " ".join(combo)
        for rep_index in range(len(locations) + 2): # 18 is the last rep level, leading to Victory
            # TODO(chesslogic): Determine which Rep level is needed for this Rep Index, some subset of 1..17
            ordinal = "st" if rep_index == 0 else "nd" if rep_index == 1 else "rd" if rep_index == 2 else "th"
            rep_name = f"{rep_index + 1}{ordinal} Reputation - {combo_name}"
            if rep_index == 18:
                rep_name = f"Victory - {combo_name}"

            needed_items = getRequiredItems(combo, related_items, rep_index)
            locations[rep_name] = (ATSLocationClassification.species_rep,needed_items)

    return locations

def getRelatedItems(combo: Tuple[str, str, str], species_preferences: Dict[str, Dict[str, List[str]]]) -> List[str]:
    # Get union of building materials
    buildings = set()
    foods = set()
    services = set()
    for species in combo:
        buildings.update(species_preferences[species]["building"])
        foods.update(species_preferences[species]["food"])
        services.update(species_preferences[species]["service"])
    
    # Get intersections (loved items - shared by 2+ species)
    loved_foods = set()
    loved_services = set()
    for food in foods:
        if sum(1 for species in combo if food in species_preferences[species]["food"]) >= 2:
            loved_foods.add(food)
    for service in services:
        if sum(1 for species in combo if service in species_preferences[species]["service"]) >= 2:
            loved_services.add(service)

    return {
        "buildings": buildings,
        "foods": foods,
        "services": services,
        "loved_foods": loved_foods,
        "loved_services": loved_services
    }

def getRequiredItems(combo: Tuple[str, str, str], related_items: Dict[str, List[str]], rep_index: int) -> List[str]:
    """Get the items required for the given species combination and reputation index."""
    # TODO(chesslogic): For the current reputation, decide which buildings, foods, and services are needed.
    # This means, for each GROUP where ANY are sufficient: ",".join(sorted(GROUP))
    # But we will need a number of GROUPS, starting with a Building and a Food. Later, multiple buildings, foods, and services are necessary.
    buildings_list = []
    foods_list = []
    services_list = []
    # Buildings
    if rep_index > 12:
        buildings_list += ["Planks", "Bricks", "Fabric"]
    if rep_index > 8:
        other_buildings = filter(lambda b: b != "Planks", sorted(related_items["buildings"]))
        buildings_list += ["Planks", ",".join(other_buildings)]
    if rep_index > 4:
        buildings_list += [",".join(sorted(related_items["buildings"]))]
    if rep_index > 15:
        foods_list += [",".join(sorted(related_items["loved_foods"]))]
    if rep_index > 5:
        foods_list += [",".join(sorted(related_items["foods"]))]
    if rep_index > 1:
        # Everyone has the same basic food needs
        foods_list += ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"]
    if rep_index > 15:
        # TODO(chesslogic): Some groups of species have no Loved services, if empty, add each service individually
        services_list += [",".join(sorted(related_items["loved_services"]))]
    if rep_index > 1:
        services_list += [",".join(sorted(related_items["services"]))]
    
    return []

    # Human - Planks, Bricks; Biscuits, Pie, Porridge; Ale, Incense
    # Beaver - Planks; Biscuits, Pickled Goods; Ale, Scrolls, Wine
    # Lizard - Bricks, Fabric; Jerky, Pickled Goods, Pie, Skewers; Training Gear
    # Harpy - Fabric; Jerky, Paste; Scrolls, Tea
    # Fox - Planks, Crystallized Dew; Pickled Goods, Porridge, Skewers; Incense, Tea
    # Frog - Bricks; Paste, Pie, Porridge; Training Gear, Incense, Wine

    # Food - If 2+ of the same food, we "Love" that food; we NEED a loved food for the last 3 reputation levels
    # Biscuits - Beaver, Human
    # Jerky - Lizard, Harpy
    # Porridge - Human, Fox, Frog
    # Skewers - Lizard, Fox
    # Paste - Harpy, Frog
    # Pie - Human, Lizard, Frog
    # Pickled Goods - Beaver, Fox, Lizard

    # Housing
    # Bricks - Human, Lizard, Frog
    # Fabric - Harpy, Lizard
    # Planks - Beaver, Fox, Human

    # Services - If 2+ of the same service, we "Love" that service; we NEED a Loved service for the Victory reputation level (except Human Lizard Harpy which has no Loved service)
    # Ale - Human, Beaver
    # Training Gear - Lizard, Frog
    # Incense - Human, Fox, Frog
    # Scrolls - Beaver, Harpy
    # Wine - Beaver, Frog
    # Tea - Harpy, Fox

    # Human Beaver Lizard
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Skewers, Biscuits, Pie, Pickled Goods - Loves Biscuits, Pie, Pickled Goods
    # Ale, Training Gear, Incense, Scrolls, Wine - Loves Ale
    # "1st Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, [], "Human Beaver Lizard"),
    # "2nd Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Lizard"),
    # "3rd Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Lizard"),
    # "4th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Lizard"),
    # "5th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish", "Purging Fire"], "Human Beaver Lizard"),
    # "6th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Lizard"),
    # "7th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Lizard"),
    # "8th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Lizard"),
    # "9th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Lizard"),
    # "10th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "11th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "12th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "13th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "14th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "15th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "16th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "17th Reputation - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Lizard"),
    # "Victory - Human Beaver Lizard": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale", "Purging Fire"], "Human Beaver Lizard"),
    # Human Beaver Harpy
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Biscuits, Pie, Pickled Goods, Paste - Loves Biscuits
    # Ale, Incense, Scrolls, Wine, Tea - Loves Ale, Scrolls
    # "1st Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, [], "Human Beaver Harpy"),
    # "2nd Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Harpy"),
    # "3rd Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Harpy"),
    # "4th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Harpy"),
    # "5th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish", "Purging Fire"], "Human Beaver Harpy"),
    # "6th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Harpy"),
    # "7th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Harpy"),
    # "8th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Harpy"),
    # "9th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Harpy"),
    # "10th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "11th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "12th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "13th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "14th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "15th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Jerky,Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "16th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Biscuits", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "17th Reputation - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Biscuits", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Harpy"),
    # "Victory - Human Beaver Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Biscuits", "Amber,Tools", "Ale,Scrolls", "Purging Fire"], "Human Beaver Harpy"),
    # Human Beaver Fox
    # Planks, Bricks
    # Porridge, Skewers, Biscuits, Pie, Pickled Goods - Loves Porridge, Biscuits, Pickled Goods
    # Ale, Incense, Scrolls, Wine, Tea - Loves Ale, Incense
    # "1st Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, [], "Human Beaver Fox"),
    # "2nd Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Fox"),
    # "3rd Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Fox"),
    # "4th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Fox"),
    # "5th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish", "Purging Fire"], "Human Beaver Fox"),
    # "6th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Fox"),
    # "7th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Fox"),
    # "8th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Fox"),
    # "9th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Purging Fire"], "Human Beaver Fox"),
    # "10th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "11th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "12th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "13th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools,Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "14th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "15th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Skewers,Biscuits,Pie,Pickled Goods", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "16th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pickled Goods", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "17th Reputation - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pickled Goods", "Amber,Tools", "Ale,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Beaver Fox"),
    # "Victory - Human Beaver Fox": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pickled Goods", "Amber,Tools", "Ale,Incense,Tea", "Purging Fire"], "Human Beaver Fox"),
    # Human Beaver Frog
    # Planks, Bricks
    # Porridge, Biscuits, Pie, Pickled Goods, Paste - Loves Porridge, Pie, Biscuits
    # Ale, Training Gear, Incense, Scrolls, Wine - Loves Ale, Incense, Wine
    # "1st Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, [], "Human Beaver Frog"),
    # "2nd Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Frog"),
    # "3rd Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Frog"),
    # "4th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Beaver Frog"),
    # "5th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish", "Purging Fire"], "Human Beaver Frog"),
    # "6th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Frog"),
    # "7th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks,Bricks", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Frog"),
    # "8th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Frog"),
    # "9th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Beaver Frog"),
    # "10th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "11th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "12th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "13th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "14th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "15th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "16th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "17th Reputation - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine", "Purging Fire"], "Human Beaver Frog"),
    # "Victory - Human Beaver Frog": (ATSLocationClassification.species_rep, ["Planks", "Bricks", "Fabric", "Porridge,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Incense,Wine", "Purging Fire"], "Human Beaver Frog"),
    # Human Lizard Harpy
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Skewers, Biscuits, Pie, Pickled Goods, Paste - loves Jerky, Pie
    # Ale, Training Gear, Incense, Scrolls, Wine, Tea - Does not love anything
    # "1st Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, [], "Human Lizard Harpy"),
    # "2nd Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Lizard Harpy"),
    # "3rd Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Lizard Harpy"),
    # "4th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Berries,Eggs,Insects,Meat,Mushrooms,Roots,Vegetables,Fish"], "Human Lizard Harpy"),
    # "5th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Lizard Harpy"),
    # "6th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Lizard Harpy"),
    # "7th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks,Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Lizard Harpy"),
    # "8th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Lizard Harpy"),
    # "9th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Purging Fire"], "Human Lizard Harpy"),
    # "10th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "11th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "12th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "13th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools,Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "14th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "15th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "16th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "17th Reputation - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # "Victory - Human Lizard Harpy": (ATSLocationClassification.species_rep, ["Planks", "Bricks,Fabric", "Jerky,Porridge,Skewers,Biscuits,Pie,Pickled Goods,Paste", "Amber,Tools", "Ale,Training Gear,Incense,Scrolls,Wine,Tea", "Purging Fire"], "Human Lizard Harpy"),
    # Human Lizard Fox
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Skewers, Biscuits, Pie, Pickled Goods - Loves Porridge, Pie, Skewers, Pickled Goods
    # Ale, Training Gear, Incense, Tea - Loves Incense

    # Human Lizard Frog
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Skewers, Biscuits, Pie, Pickled Goods, Paste - Loves Porridge, Pie
    # Ale, Training Gear, Incense, Wine - Loves Training Gear, Incense

    # Human Harpy Fox
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Skewers, Biscuits, Pie, Pickled Goods, Paste - Loves Porridge
    # Ale, Incense, Scrolls, Tea - Loves Incense, Tea

    # Human Harpy Frog
    # Planks, Bricks, Fabric
    # Jerky, Porridge, Biscuits, Pie, Paste - Loves Porridge, Pie, Paste
    # Ale, Training Gear, Incense, Scrolls, Wine, Tea - Loves Incense

    # Human Fox Frog
    # Planks, Bricks
    # Porridge, Skewers, Biscuits, Pie, Pickled Goods, Paste - Loves Porridge, Pie
    # Ale, Training Gear, Incense, Wine, Tea - Loves Incense

    # Beaver Lizard Harpy
    # Planks, Bricks, Fabric
    # Jerky, Biscuits, Pickled Goods, Pie, Skewers, Paste - Loves Jerky, Pickled Goods
    # Training Gear, Scrolls, Wine, Tea - Loves Scrolls

    # Beaver Lizard Fox
    # Planks, Bricks, Fabric
    # Jerky, Skewers, Biscuits, Pickled Goods, Porridge - Loves Pickled Goods, Skewers
    # Training Gear, Scrolls, Wine, Tea, Incense - Does not love anything

    # Beaver Lizard Frog
    # Planks, Bricks, Fabric
    # Jerky, Skewers, Biscuits, Pickled Goods, Pie, Paste, Porridge - Loves Pie, Pickled Goods
    # Training Gear, Scrolls, Wine - Loves Training Gear, Wine

    # Beaver Harpy Fox
    # Planks, Fabric
    # Porridge, Jerky, Biscuits, Pickled Goods, Paste, Skewers - Loves Pickled Goods
    # Scrolls, Wine, Tea - Loves Scrolls, Tea

    # Beaver Harpy Frog
    # Planks, Bricks, Fabric
    # Porridge, Jerky, Biscuits, Pickled Goods, Paste, Pie - Loves Paste
    # Ale, Training Gear, Scrolls, Incense, Wine, Tea - Loves Scrolls, Wine

    # Beaver Fox Frog
    # Planks, Bricks
    # Porridge, Skewers, Biscuits, Pickled Goods, Paste, Pie - Loves Porridge, Pickled Goods
    # Ale, Training Gear, Scrolls, Incense, Wine, Tea - Loves Incense, Wine

    # Lizard Harpy Fox
    # Planks, Bricks, Fabric
    # Porridge, Jerky, Skewers, Pickled Goods, Pie, Paste - Loves Jerky, Skewers
    # Training Gear, Scrolls, Tea - Loves Tea

    # Lizard Harpy Frog
    # Bricks, Fabric
    # Jerky, Skewers, Pickled Goods, Paste, Pie - Loves Jerky, Paste
    # Training Gear, Scrolls, Tea, Wine - Loves Training Gear

    # Lizard Fox Frog
    # Planks, Bricks, Fabric
    # Skewers, Pickled Goods, Paste, Porridge, Pie - Loves Skewers, Pie
    # Training Gear, Incense, Tea, Wine - Loves Training Gear, Incense

    # Harpy Fox Frog
    # Bricks, Fabric
    # Jerky, Paste, Porridge, Skewers, Pickled Goods, Pie - Loves Porridge, Paste
    # Training Gear, Scrolls, Tea, Incense, Wine - Loves Tea, Incense, Wine
