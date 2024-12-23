import unittest
from typing import Dict, List
from BaseClasses import MultiWorld, CollectionState
from Options import DefaultOnToggle, Accessibility, ItemSet
from .. import CMWorld
from ..Items import progression_items, useful_items, filler_items
from ..Options import (CMOptions, MinorPieceLimitByType, MajorPieceLimitByType, 
                      QueenPieceLimitByType, QueenPieceLimit, PocketLimitByPocket,
                      Goal, Difficulty, EnableTactics, PieceLocations, PieceTypes,
                      FairyChessPieces, FairyChessPiecesConfigure, FairyChessArmy, FairyChessPawns)
from ..ItemPool import CMItemPool


class TestItemPool(unittest.TestCase):
    def setUp(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "ChecksMate"
        self.world = CMWorld(self.multiworld, 1)

        # Initialize options with proper option classes
        progression_balancing = DefaultOnToggle(True)
        accessibility = Accessibility(Accessibility.option_full)
        local_items = ItemSet({})
        non_local_items = ItemSet({})
        goal = Goal(Goal.option_single)
        difficulty = Difficulty(Difficulty.option_daily)
        enable_tactics = EnableTactics(EnableTactics.option_all)
        piece_locations = PieceLocations(PieceLocations.option_chaos)
        piece_types = PieceTypes(PieceTypes.option_stable)
        fairy_chess_pieces = FairyChessPieces(FairyChessPieces.option_full)
        fairy_chess_pieces_configure = FairyChessPiecesConfigure(FairyChessPiecesConfigure.default)
        fairy_chess_army = FairyChessArmy(FairyChessArmy.option_stable)
        fairy_chess_pawns = FairyChessPawns(FairyChessPawns.option_vanilla)

        # Create numeric options with proper value attributes
        class NumericOption:
            def __init__(self, value):
                self.value = value

        self.world.options = CMOptions(
            progression_balancing,
            accessibility,
            local_items,
            non_local_items,
            [],  # start_inventory
            [],  # start_hints
            [],  # start_location_hints
            set(),  # exclude_locations
            set(),  # priority_locations
            [],  # item_links
            goal,
            difficulty,
            enable_tactics,
            piece_locations,
            piece_types,
            NumericOption(0),  # early_material
            NumericOption(5),  # max_engine_penalties
            NumericOption(12),  # max_pocket
            NumericOption(3),  # max_kings
            NumericOption(2),  # fairy_kings
            fairy_chess_pieces,
            fairy_chess_pieces_configure,
            fairy_chess_army,
            fairy_chess_pawns,
            NumericOption(MinorPieceLimitByType.range_end),
            NumericOption(MajorPieceLimitByType.range_end),
            NumericOption(QueenPieceLimitByType.range_end),
            NumericOption(QueenPieceLimit.range_end),
            NumericOption(PocketLimitByPocket.range_end),
            {},  # locked_items
            False  # death_link
        )
        
        self.item_pool = CMItemPool(self.world)
        self.item_pool.initialize_item_tracking()

    def test_material_requirements(self):
        """Test that material requirements are calculated correctly for both board sizes"""
        min_mat, max_mat = self.item_pool.calculate_material_requirements(super_sized=False)
        self.assertGreater(max_mat, min_mat)
        
        min_mat_super, max_mat_super = self.item_pool.calculate_material_requirements(super_sized=True)
        self.assertGreater(min_mat_super, min_mat)
        self.assertGreater(max_mat_super, max_mat)

    def test_progression_item_pool_preparation(self):
        """Test that the progression item pool is prepared with correct frequencies"""
        pool = self.item_pool.prepare_progression_item_pool()
        
        # Check Victory is removed
        self.assertNotIn("Victory", pool)

    def test_option_limits(self):
        """Test that option limits are correctly applied"""
        self.item_pool.handle_option_limits()
        
        # Check king limits
        self.assertLessEqual(
            self.item_pool.items_used[self.world.player]["Progressive Consul"],
            3 - self.world.options.max_kings.value
        )
        
        # Check fairy king limits
        self.assertLessEqual(
            self.item_pool.items_used[self.world.player]["Progressive King Promotion"],
            2 - self.world.options.fairy_kings.value
        )
        
        # Check engine penalty limits
        self.assertLessEqual(
            self.item_pool.items_used[self.world.player]["Progressive Engine ELO Lobotomy"],
            5 - self.world.options.max_engine_penalties.value
        )

    def test_max_items_calculation(self):
        """Test that max items are calculated correctly based on options"""
        base_max = self.item_pool.get_max_items(super_sized=False)
        super_max = self.item_pool.get_max_items(super_sized=True)
        self.assertGreater(super_max, base_max)
        
        # Test with tactics disabled
        self.world.options.enable_tactics = EnableTactics(EnableTactics.option_none)
        no_tactics_max = self.item_pool.get_max_items(super_sized=False)
        self.assertLess(no_tactics_max, base_max)

    def test_item_consumption_tracking(self):
        """Test that item consumption is tracked correctly"""
        test_item = next(iter(progression_items.keys()))
        initial_quantity = progression_items[test_item].quantity
        
        self.item_pool.consume_item(test_item, {})
        
        self.assertEqual(self.item_pool.items_used[self.world.player][test_item], 1)
        self.assertEqual(
            self.item_pool.items_remaining[self.world.player][test_item],
            initial_quantity - 1
        )

    def test_progression_item_creation(self):
        """Test that progression items are created within material limits"""
        min_mat, max_mat = 3900, 4000
        max_items = 100
        items = self.item_pool.create_progression_items(
            max_items=max_items,
            min_material=min_mat,
            max_material=max_mat,
            locked_items={}
        )
        
        total_material = sum(progression_items[item.name].material for item in items)
        self.assertGreaterEqual(total_material, min_mat)
        self.assertLessEqual(total_material, max_mat)
        
        # Also verify we don't exceed max_items
        self.assertLessEqual(len(items), max_items)

    def test_filler_item_creation_respects_pocket(self):
        """Test that filler items respect pocket requirements"""
        max_items = 100
        # Test without pocket
        items_no_pocket = self.item_pool.create_filler_items(has_pocket=False, max_items=max_items)
        self.assertTrue(all("Pocket" not in item.name for item in items_no_pocket))
        
        # Test with pocket
        items_with_pocket = self.item_pool.create_filler_items(has_pocket=True, max_items=max_items)
        has_pocket_items = any("Pocket" in item.name for item in items_with_pocket)
        self.assertTrue(has_pocket_items)

    def test_filler_item_creation_with_pocket(self):
        """Test that filler item creation handles pocket gems as fallback"""
        max_items = 100
        user_location_count = 5  # Simulate some existing locations
        locked_items = {"Progressive Major Piece": 2}  # Simulate some locked items
        
        # Test with pocket
        items_with_pocket = self.item_pool.create_filler_items(
            has_pocket=True,
            max_items=max_items,
            user_location_count=user_location_count,
            locked_items=locked_items
        )
        total_count = len(items_with_pocket) + user_location_count + sum(locked_items.values())
        self.assertLessEqual(total_count, max_items)
        
    def test_filler_item_creation_no_pocket(self):
        """Test that filler item creation handles no pocket gems"""
        max_items = 100
        user_location_count = 5  # Simulate some existing locations
        locked_items = {"Progressive Major Piece": 2}  # Simulate some locked items
        
        # Test without pocket
        items_no_pocket = self.item_pool.create_filler_items(
            has_pocket=False, max_items=max_items,
            user_location_count=user_location_count,
            locked_items=locked_items
        )
        total_count = len(items_no_pocket) + user_location_count + sum(locked_items.values())
        self.assertLessEqual(total_count, max_items)

    def test_excluded_items_handling(self):
        """Test that excluded items are handled correctly"""
        excluded = {"Progressive Pawn": 2, "Progressive Minor Piece": 1}
        starter_items = self.item_pool.handle_excluded_items(excluded)
        
        self.assertEqual(len(starter_items), 3)  # 2 pawns + 1 minor piece
        self.assertEqual(self.item_pool.items_used[self.world.player]["Progressive Pawn"], 2)
        self.assertEqual(self.item_pool.items_used[self.world.player]["Progressive Minor Piece"], 1)


if __name__ == '__main__':
    unittest.main() 