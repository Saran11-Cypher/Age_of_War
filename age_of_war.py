import streamlit as st
import time
from itertools import permutations

# Class advantage rules
CLASS_ADVANTAGE = {
    "Militia": ["Spearmen", "LightCavalry"],
    "Spearmen": ["LightCavalry", "HeavyCavalry"],
    "LightCavalry": ["FootArcher", "CavalryArcher"],
    "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
    "CavalryArcher": ["Spearmen", "HeavyCavalry"],
    "FootArcher": ["Militia", "CavalryArcher"],
}

PLATOON_CLASSES = {
    "Militia": "🛡️ Militia",
    "Spearmen": "⚔️ Spearmen",
    "LightCavalry": "🐎 Light Cavalry",
    "HeavyCavalry": "🐴 Heavy Cavalry",
    "CavalryArcher": "🏹 Cavalry Archer",
    "FootArcher": "🏹 Foot Archer",
}

class Platoon:
    def __init__(self, unit_class: str, soldiers: int):
        self.unit_class = unit_class
        self.soldiers = soldiers

    def has_advantage_over(self, opponent):
        return opponent.unit_class in CLASS_ADVANTAGE.get(self.unit_class, [])

    def effective_strength_against(self, opponent):
        multiplier = 2 if self.has_advantage_over(opponent) else 1
        return self.soldiers * multiplier

    def __str__(self):
        return f"{self.unit_class}#{self.soldiers}"

class Army:
    def __init__(self, platoons):
        self.platoons = platoons

    def count_wins_against(self, opponent_army, verbose=False):
        wins = 0
        battle_results = []
        for idx, (self_platoon, enemy_platoon) in enumerate(zip(self.platoons, opponent_army.platoons), 1):
            my_strength = self_platoon.effective_strength_against(enemy_platoon)
            enemy_strength = enemy_platoon.effective_strength_against(self_platoon)

            if my_strength > enemy_strength:
                outcome = "WIN"
                wins += 1
            elif my_strength == enemy_strength:
                outcome = "DRAW"
            else:
                outcome = "LOSS"

            if verbose:
                battle_results.append(
                    f"Battle {idx}: {self_platoon} vs {enemy_platoon} => {outcome} "
                    f"(You: {my_strength} vs Enemy: {enemy_strength})"
                )
        return wins, battle_results

    def __str__(self):
        return ";".join(str(platoon) for platoon in self.platoons)

def get_army_input(label, container):
    all_platoons = []
    for cls, emoji_name in PLATOON_CLASSES.items():
        count = container.number_input(f"{emoji_name} ({label})", min_value=0, value=0, step=10, key=f"{label}_{cls}")
        all_platoons.append(Platoon(cls, count))

    non_zero = [p for p in all_platoons if p.soldiers > 0]
    if len(non_zero) < 5:
        container.warning("Please assign non-zero soldiers to at least 5 platoon types.")
        return None
    return sorted(non_zero, key=lambda x: -x.soldiers)[:5]

def find_winning_arrangement(your_army, enemy_army):
    for perm in permutations(your_army):
        temp_army = Army(list(perm))
        wins, _ = temp_army.count_wins_against(enemy_army)
        if wins >= 3:
            return temp_army
    return None

# Streamlit Layout
st.set_page_config(page_title="Age of War", layout="wide")
st.title("⚔️ Age of War – Visual Battle Simulator")

col1, col2 = st.columns(2)

with st.form("battle_form"):
    with col1:
        your_army = get_army_input("Your Army", st)
    with col2:
        enemy_army = get_army_input("Enemy Army", st)
    submitted = st.form_submit_button("Let the battle begins...")

if submitted and your_army and enemy_army:
    enemy_obj = Army(enemy_army)
    winning_army = find_winning_arrangement(your_army, enemy_obj)

    if winning_army:
        st.success("Winning arrangement found:")
        st.code(str(winning_army))

        st.markdown("### ⚔️ Simulating Battle...")
        placeholder = st.empty()
        win_count, logs = winning_army.count_wins_against(enemy_obj, verbose=True)
        progress = st.progress(0)

        for i, log in enumerate(logs):
            time.sleep(1)
            placeholder.markdown(f"#### {log}")
            progress.progress((i + 1) / len(logs))

        progress.empty()

        st.markdown("---")
        if win_count >= 3:
            st.success(f"You won the war! (Total Wins: {win_count})")
            st.balloons()
        else:
            st.error(f"Enemy won the war. (Total Wins: {win_count})")
    else:
        st.error("There is no chance of winning")
