from unittest import TestCase, TestSuite, TestLoader, TextTestRunner
from conways_GOL import *

class InputStrategyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        input_str = "..O.....\n" \
                    "O..O....\n" \
                    "O..O....\n" \
                    ".O....O.\n" \
                    ".....O.O\n" \
                    "......O.\n"
        cls.input_strat = StringInput(input_str=input_str, live_state='O')

    def test_000_get_cols_rows(self):
        self.assertEquals(self.input_strat.get_num_cols_and_rows(), (8,6))

    def test_001_get_live_dead_defns(self):
        self.assertFalse(self.input_strat.is_live('.'))
        self.assertTrue(self.input_strat.is_live('O'))

class BoardTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input_str = "......O.\n" \
                        "OOO...O.\n" \
                        "......O.\n" \
                        "........\n" \
                        "...OO...\n" \
                        "...OO...\n"
        str_strat = StringInput(input_str=cls.input_str, live_state='O')
        cls.test_board = Board(input_strategy=str_strat)
        
    def test_100_initialize_board(self):
        output_str = self.test_board.display_board()
        self.assertEquals(self.input_str, output_str)

    def test_101_update_board(self):
        ref_str = ".O......\n" \
                  ".O...OOO\n" \
                  ".O......\n" \
                  "........\n" \
                  "...OO...\n" \
                  "...OO...\n"
        self.test_board.update_board()
        output_str = self.test_board.display_board()
        self.assertEquals(ref_str, output_str)

class NegativeTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_string = ''
        cls.input_strat = StringInput(input_str=cls.input_string, live_state='O')

    def test_200_initialize_no_input(self):
        self.assertEquals(self.input_strat.get_num_cols_and_rows(), (0,0))

    def test_201_game_with_no_input(self):
        test_board = Board(input_strategy=self.input_strat)
        output_str = test_board.display_board()
        self.assertEquals(self.input_string, output_str)

class GameTestCase(TestCase):
    def test_500_1_iteration(self):
        input_str = "..O.....\n" \
                    "O..O....\n" \
                    "O..O....\n" \
                    ".O....O.\n" \
                    ".....O.O\n" \
                    "......O.\n"
        output_str = "........\n" \
                     ".OOO....\n" \
                     "OOO.....\n" \
                     "......O.\n" \
                     ".....O.O\n" \
                     "......O.\n"

        str_input = StringInput(input_str=input_str, live_state='O')
        test_game = ConwaysGame(iterations=1, input_strategy=str_input)
        test_game.start_game()
        self.assertEquals(output_str, test_game.board.display_board())

    def test_501_2_iterations(self):
        input_str = "..O.....\n" \
                    "O..O....\n" \
                    "O..O....\n" \
                    ".O....O.\n" \
                    ".....O.O\n" \
                    "......O.\n"
        output_str = "..O.....\n" \
                     "O..O....\n" \
                     "O..O....\n" \
                     ".O....O.\n" \
                     ".....O.O\n" \
                     "......O.\n"
        str_input = StringInput(input_str=input_str, live_state='O')
        test_game = ConwaysGame(iterations=2, input_strategy=str_input)
        test_game.start_game()
        self.assertEquals(output_str, test_game.board.display_board())

if __name__ == "__main__":
    import sys, inspect
    master_suite = TestSuite(
        [TestLoader().loadTestsFromTestCase(obj)
         for name, obj in inspect.getmembers(sys.modules[__name__])
         if inspect.isclass(obj) and obj.__module__ == "__main__"]
    )
    tsr = TextTestRunner()
    tsr.run(master_suite)
