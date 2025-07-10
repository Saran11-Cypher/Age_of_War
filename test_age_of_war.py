import unittest, HtmlTestRunner, os, webbrowser
from age_of_war import Platoon, Army, find_winning_arrangement

class TestAgeOfWar(unittest.TestCase):

    def test_platoon_advantage_militia_vs_spearmen(self):
        """Militia should have advantage over Spearmen (double strength)"""
        militia = Platoon("Militia", 50)
        spearmen = Platoon("Spearmen", 40)
        self.assertTrue(militia.has_advantage_over(spearmen), "Militia should counter Spearmen")

    def test_effective_strength_when_advantaged(self):
        """Platoon with advantage should get doubled strength"""
        militia = Platoon("Militia", 50)
        spearmen = Platoon("Spearmen", 40)
        expected_strength = 100
        actual_strength = militia.effective_strength_against(spearmen)
        self.assertEqual(actual_strength, expected_strength, f"Expected {expected_strength}, got {actual_strength}")

    def test_effective_strength_when_no_advantage(self):
        """Platoon without advantage should use base strength"""
        militia = Platoon("Militia", 50)
        archer = Platoon("FootArcher", 30)
        expected_strength = 50
        actual_strength = militia.effective_strength_against(archer)
        self.assertEqual(actual_strength, expected_strength, "No advantage → strength should be unchanged")

    def test_counting_battle_wins_between_armies(self):
        """Validate that Army.count_wins_against works within range"""
        army1 = Army([
            Platoon("Militia", 60),
            Platoon("Spearmen", 30),
            Platoon("LightCavalry", 100),
            Platoon("FootArcher", 20),
            Platoon("HeavyCavalry", 50)
        ])
        army2 = Army([
            Platoon("Spearmen", 40),
            Platoon("LightCavalry", 20),
            Platoon("FootArcher", 90),
            Platoon("HeavyCavalry", 50),
            Platoon("CavalryArcher", 80)
        ])
        wins, _ = army1.count_wins_against(army2)
        self.assertTrue(0 <= wins <= 5, f"Win count must be between 0 and 5, got {wins}")

    def test_find_valid_winning_army_arrangement(self):
        """Ensure at least one winning arrangement can be found"""
        your_input = [
            Platoon("Militia", 60),
            Platoon("Spearmen", 30),
            Platoon("LightCavalry", 100),
            Platoon("FootArcher", 20),
            Platoon("HeavyCavalry", 50)
        ]
        enemy_input = [
            Platoon("Spearmen", 10),
            Platoon("LightCavalry", 20),
            Platoon("FootArcher", 90),
            Platoon("HeavyCavalry", 50),
            Platoon("CavalryArcher", 80)
        ]
        enemy_army = Army(enemy_input)
        result = find_winning_arrangement(your_input, enemy_army)
        self.assertIsNotNone(result, "Should find at least one winning order of platoons")

# Run and generate HTML report
if __name__ == '__main__':
    output_path = r"(give the desired path as you choose to save)"
    os.makedirs(output_path, exist_ok=True)

    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(
            output=output_path,
            report_name="AgeOfWarReport",
            report_title="Age of War - Unit Test Report",
            combine_reports=True
        )
    )

