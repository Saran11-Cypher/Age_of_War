
### Age of War – Streamlit App Code Explanation

####  This file provides a detailed, line-by-line breakdown of the `Age of War` Streamlit application.

---

## Imports

```python
import streamlit as st
import time
from itertools import permutations
```

- `streamlit`: Used to create the interactive UI
- `time`: For simulating battle animations with delay
- `permutations`: Used to try all possible arrangements of platoons

---

## Class Advantage Rules

```python
CLASS_ADVANTAGE = {
    ...
}
```

<p>A dictionary that defines which platoon class has advantage over which others. This affects battle strength calculation. so that It can be helpful when we test the battle strength of each platoons as well as we can able to determine the winning possiblity</p>

---

## Platoons

```python
PLATOON_CLASSES = {
    ...
}
```

##### Maps internal class names to user-friendly names with emojis for UI display so that we can understand what each troop is exactly meant for and we can decide how many troops we can deployed in that.

---

## 🔷 Platoon Class

```python
class Platoon:
```

Represents a single platoon unit with:
- `unit_class`: type (e.g., "Militia")
- `soldiers`: number of troops

### Methods:
- `has_advantage_over`: Checks if this platoon counters another
- `effective_strength_against`: Returns strength (doubled if advantaged)
- `__str__`: String representation like `Militia#50`

---

###  Army Class

```python
class Army:
```

<h4>Holds a list of 5 platoons.</h4>

### Methods:
- `count_wins_against`: Compares this army vs another, returns:
  - Total battles won
  - Battle logs if `verbose=True`
- `__str__`: Returns semicolon-separated list of all platoons

---

## get_army_input()

```python
def get_army_input(label, container):
```

Renders UI for user to enter soldier counts for all 6 classes.
- Stores only classes with > 0 soldiers
- Warns if fewer than 5 valid entries
- Returns top 5 strongest platoons (by soldier count)

---

## find_winning_arrangement()

```python
def find_winning_arrangement(your_army, enemy_army):
```

- Tries all 120 permutations of your platoons
- Returns the first arrangement that wins ≥ 3 battles
- Else, returns `None`

---

## Streamlit UI for console application to enhance the UI.

```python
st.set_page_config(...)
st.title(...)
col1, col2 = st.columns(2)
```

- Sets app title and layout
- Creates side-by-side input forms for your army and enemy army

---

### Form Section

```python
with st.form("battle_form"):
```

- Contains both army input sections
- Has a submit button: **"Let the battle begins..."**

---

### Battle Simulation Section

```python
if submitted and your_army and enemy_army:
```

- Runs when form is submitted and both armies are valid
- Finds the winning arrangement
- Shows progress bar
- Displays each battle result with a delay
- Shows outcome (win/loss)

---

## Visual Effects

```python
st.success(), st.error(), st.balloons()
```

- Shows outcome visually
- Balloons 🎈 are launched if user wins

---

## Summary

This app lets users:
- Build two armies (selecting soldier counts)
- Simulate a battle
- View results with animation
- Understand which platoon wins against which

---
---
---




# Age of War - Unit Test Suite (HTML Report)

This test suite validates the behavior of the `Age of War` simulation using Python's `unittest` module and generates an HTML test report using `HtmlTestRunner`.

---

## Test Case Breakdown

### 1. `test_platoon_advantage_militia_vs_spearmen`
- **Purpose**: Checks that **Militia** has an advantage over **Spearmen**.
- **Expected**: `has_advantage_over()` should return `True`.

---

### 2. `test_effective_strength_when_advantaged`
- **Purpose**: Ensures that a platoon with advantage gets **double strength**.
- **Example**: Militia(50) vs Spearmen → `effective_strength = 100`.

---

### 3. `test_effective_strength_when_no_advantage`
- **Purpose**: Verifies that strength remains **unchanged** when there is **no advantage**.
- **Example**: Militia(50) vs FootArcher → `effective_strength = 50`.

---

### 4. `test_counting_battle_wins_between_armies`
- **Purpose**: Checks that the function `count_wins_against()` returns a value in the expected range of **0 to 5**.
- **Reason**: Each army has 5 platoons → Max 5 battles → Valid win count: 0–5.

---

### 5. `test_find_valid_winning_army_arrangement`
- **Purpose**: Ensures `find_winning_arrangement()` finds **at least one winning arrangement** against a weaker enemy configuration.
- **Expected**: Should return a non-`None` result.

---

## Report Location
- All results will be saved in the folder:
  ```
  desired location that we can choose here
  ```
- The file generated will be:
  ```
  AgeOfWarReport.html
  ```

## How to Run This
Use the command below:
```
python test_age_of_war.py
```

> Ensure the `HtmlTestRunner` package is installed before running.