# 🎰 Poker Step-by-Step Analyzer

**Advanced 3-player Texas Hold'em analyzer with progressive stage-by-stage analysis. Enter your cards and board cards progressively to see how win probabilities and AI recommendations change at each stage.**

## Try this at [pokerhandpredictor](https://pokerhandpredictor.streamlit.app/)
---

## 📖 Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [How It Works](#how-it-works)
5. [Prediction Methodology](#prediction-methodology)
6. [What Predictions Are Based On](#what-predictions-are-based-on)
7. [Game Flow](#game-flow)
8. [Card Reference](#card-reference)
9. [AI Decision Logic](#ai-decision-logic)
10. [Understanding the Analysis](#understanding-the-analysis)
11. [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Progressive Stage Analysis
- **Step-by-step gameplay** - Enter hole cards → Flop → Turn → River
- **Real-time analysis** - Get probabilities and recommendations after each card
- **Hidden opponents** - AI opponents get random cards (realistic poker)
- **Auto-regeneration** - If AI cards conflict with your board, they're automatically regenerated

### Comprehensive Analysis
- **Win probabilities** - 3-player pot probabilities at each stage
- **Hand strength** - Your equity vs random opponent hands
- **Board texture** - Analysis of dry/wet/coordinated boards
- **AI recommendations** - Action suggestions with confidence scores
- **Monte Carlo simulation** - 3,000+ iterations for accurate probabilities

### Interactive UI
- **Visual metrics** - Color-coded probabilities and recommendations
- **Expandable sections** - Detailed analysis for each stage
- **Final showdown** - Opponent cards revealed with winner determination
- **Restart button** - Play another hand instantly

---

## 🚀 Installation

### Requirements
- Python 3.8+
- Streamlit
- itertools (built-in)
- Counter from collections (built-in)

### Setup

```bash
# 1. Install Streamlit
pip install streamlit

# 2. Navigate to your project directory
cd /path/to/poker_analyzer

# 3. Run the app
streamlit run poker.py
```

The app will open at `http://localhost:8501`

---

## 🎯 Quick Start

### Basic Workflow

```
1. Enter your 2 hole cards
   Example: "AH KD"
   
2. View Pre-Flop Analysis
   - Win probability: ~42% (1 of 3 players)
   - Hand strength: ~68% (vs random hands)
   - AI recommendation: RAISE 95%
   
3. Enter 3 flop cards
   Example: "2H 3D 4C"
   
4. View Flop Analysis
   - Board texture: DRY
   - Updated probabilities
   - New recommendations
   
5. Enter turn card
   Example: "5S"
   
6. View Turn Analysis
   - Updated equity
   
7. Enter river card
   Example: "7H"
   
8. Final Showdown
   - All opponent cards revealed
   - Best hands determined
   - Winner declared
```

---

## 🔬 How It Works

### System Architecture

```
┌─────────────────────────────────────┐
│     User Input                      │
│  Your Cards + Board Cards           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│     Validation Layer                │
│  - Card format check                │
│  - Duplicate detection              │
│  - AI card regeneration if needed   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│     Analysis Engine                 │
│  - Hand strength calculation        │
│  - Board texture analysis           │
│  - Win probability simulation       │
│  - AI decision engine               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│     Output                          │
│  - Probabilities (3 players)        │
│  - Recommendations (3 players)      │
│  - Hand strength percentages        │
│  - Confidence scores                │
└─────────────────────────────────────┘
```

### Data Flow

```
Your Input: 2S 9S
    ↓
Flop: 6C 3H 4S
    ↓
Check: Are there duplicates?
    NO → Continue
    YES → Regenerate AI cards automatically
    ↓
Generate 2 random unknown AI opponent cards
    ↓
Run 3,000 Monte Carlo simulations
    ↓
Calculate probabilities and hand strength
    ↓
Apply AI decision logic
    ↓
Display results
```

---

## 📊 Prediction Methodology

### Win Probability Calculation

**Method: Monte Carlo Simulation**

```
For 3,000 iterations:
  1. Take current known cards (your cards + board cards)
  2. Randomly select cards to complete the board to 5 cards
  3. For each player:
     - Find best 5-card hand from their 2 cards + 5 board cards
     - Compare hand strengths
  4. Determine winner
  5. Track wins for each player

Final: (Player Wins / 3,000) * 100 = Win Probability %
```

**Why Monte Carlo?**
- Accounts for all possible remaining card combinations
- Fast enough for real-time calculations
- Statistically accurate (converges with more iterations)
- Handles 3-player dynamics naturally

**Example Calculation:**

```
Your cards: AH KD
Board: 2H 3C 4S
AI 1: ?? (hidden)
AI 2: ?? (hidden)

Simulation:
- Remaining cards: 46 (52 - 6 known)
- Iterations: 3,000
- Each iteration:
  * Random turn card: one of 46
  * Random river card: one of remaining 45
  * Evaluate best 5-card hands for all 3 players
  * Determine winner

Result: You win 1,247 / 3,000 = 41.6% of the time
```

### Hand Strength Calculation

**Method: Single Opponent Comparison**

```
For 300 iterations:
  1. Generate random opponent 2-card hand (from remaining cards)
  2. Randomly complete the board to 5 cards
  3. Compare your best 5-card hand vs opponent's best hand
  4. Count wins
  5. Repeat with different random opponents

Final: (Wins / 300) * 100 = Hand Strength %
```

**Why Different from Win Probability?**
- Win probability: 3-player pot dynamics
- Hand strength: Your equity vs a single unknown hand
- Helps understand "how strong is my hand on average?"

**Example:**

```
Pre-flop with AH KD:
- Hand strength: ~68%
- Meaning: If we went to showdown, AK beats a random hand 68% of the time
- This is a premium pre-flop hand

At river with AK 2 3 4 board:
- Hand strength: ~41%
- Meaning: You made high card, only beats random hands 41% of the time
- This is a weak river hand
```

### Hand Evaluation Algorithm

**Algorithm: Exhaustive 5-Card Combination Search**

```python
Best hand from 7 cards = Best among all C(7,5) = 21 possible 5-card combinations

Steps:
1. Generate all 21 possible 5-card combinations from your 7 cards
2. Evaluate each combination (rank calculation below)
3. Return the highest-ranked combination

Time: O(21 * evaluation_time) - Very fast
Accuracy: 100% (exhaustive search)
```

**Hand Ranking Logic:**

```
Check in order (highest to lowest):
  1. Royal Flush     (A-K-Q-J-T, same suit)
  2. Straight Flush  (5 consecutive, same suit)
  3. Four of a Kind   (4 cards same rank)
  4. Full House      (3 of a kind + pair)
  5. Flush           (5 cards, same suit)
  6. Straight        (5 consecutive ranks)
  7. Three of a Kind (3 cards same rank)
  8. Two Pair        (2 different pairs)
  9. One Pair        (2 cards same rank)
  10. High Card      (no combinations)

Each rank has tiebreaker logic:
- Pair: Compare pair value, then kickers
- Two Pair: Compare pairs, then kicker
- Etc.

Result: Comparable tuple for ranking
```

---

## 🎲 What Predictions Are Based On

### 1. **Card Information Available**

Your hand predicts based on:

```
KNOWN CARDS:
✓ Your 2 hole cards (100% known)
✓ Community cards on board (100% known)
✓ AI opponent cards (UNKNOWN - randomized)

UNKNOWN CARDS:
✗ Future board cards (until you enter them)
✗ AI opponent's exact cards (realistic - you don't know in real poker)
✗ Card order (doesn't matter - all 5 cards dealt at once in analysis)
```

### 2. **Statistical Assumptions**

Predictions assume:

```
✓ All remaining cards equally likely
✓ Opponents play optimally (rough approximation)
✓ No folding/betting dynamics (simplified model)
✓ 3-player pot goes to showdown
✓ Random opponent card distribution
```

### 3. **Game Stage Matters**

Prediction changes with each stage:

```
PRE-FLOP (0 board cards):
- Most uncertain
- Hand strength ~35-50% range
- Depends heavily on starting hand quality

FLOP (3 board cards):
- Major clarification
- Hand strength changes significantly
- Board texture matters

TURN (4 board cards):
- Near final decision
- Only 1 card remaining

RIVER (5 board cards):
- Certain outcome
- All information revealed
```

### 4. **Board Texture Analysis**

Affects AI recommendations:

```
DRY BOARD (e.g., K-7-2):
- Few draws available
- Made hands hold strong
- Safe for value betting

COORDINATED BOARD (e.g., J-T-9):
- Some draw possibilities
- Mix of made hands and draws

WET BOARD (e.g., K♥-J♥-9♥):
- Many flush draws
- Many straight draws
- High variance
- Dangerous for marginal hands
```

### 5. **Monte Carlo Simulation Parameters**

Accuracy improves with iterations:

```
Current: 3,000 iterations
- Win probability: ±1-2% variance
- Fast enough for real-time
- Good balance of speed vs accuracy

More iterations = More accurate but slower
Fewer iterations = Faster but less accurate

Variance example:
- Run 1: You win 42.1%
- Run 2: You win 41.9%
- Run 3: You win 42.3%
(Normal variation with 3,000 iterations)
```

---

## 🎯 Game Flow

### Stage 1: Your Hole Cards

```
Input: AH KD (Ace of Hearts, King of Diamonds)

Processing:
✓ Validate card format
✓ Check no duplicates
✓ Generate 2 random AI cards (hidden from you)

Output: Cards accepted, ready for pre-flop analysis
```

### Stage 2: Pre-Flop Analysis

```
Your position: Pre-flop (no community cards)

Analysis shown:
- Your win probability: ~42% (1 of 3 players, 33% baseline)
- AI 1 win probability: ~29%
- AI 2 win probability: ~29%
- Your hand strength: ~68% (vs single random opponent)

AI Recommendations:
- YOU: RAISE (95% confidence)
  Reason: Premium hand - raise aggressively
- AI 1: CALL (70% confidence)  
  Reason: Good hand - see flop
- AI 2: FOLD (85% confidence)
  Reason: Weak hand - fold
```

### Stage 3: Flop (3 Cards)

```
Input: 2H 3D 4C

Processing:
✓ Validate 3 cards
✓ Check for duplicates with your cards
✓ If duplicate found: Auto-regenerate AI cards
✓ Run analysis

Output: Flop accepted, analysis displays with board texture
```

### Stage 4: Turn (1 Card)

```
Input: 5S

Processing:
✓ Validate 1 card
✓ Check for duplicates with all known cards
✓ If duplicate found: Auto-regenerate AI cards

Output: Turn accepted, updated analysis
```

### Stage 5: River (1 Card)

```
Input: 7H

Processing:
✓ Validate 1 card
✓ Final duplicate check
✓ Evaluate final best hands for all players

Output: Showdown begins
```

### Stage 6: Final Showdown

```
Display:
✓ Your best 5-card hand
✓ AI 1 cards revealed + best 5-card hand
✓ AI 2 cards revealed + best 5-card hand
✓ Winner determination
✓ Ranking of all 3 players

Example output:
YOU: 👉 One Pair (AH AD AK Q2)
AI 1: 👉 One Pair (KH KD KJ 3H)
AI 2: 🎲 High Card (AH K2 Q3 J4)

Winner: YOU with One Pair
Ranking:
1. YOU - One Pair
2. AI 1 - One Pair (lower pair)
3. AI 2 - High Card
```

---

## 🎴 Card Reference

### Ranks

| Rank | Name | Symbol |
|------|------|--------|
| 2-9 | Number cards | Face value |
| T | 10 | Ten |
| J | Jack | Jack |
| Q | Queen | Queen |
| K | King | King |
| A | Ace | Highest |

### Suits

| Suit | Name | Symbol |
|------|------|--------|
| H | Heart | ♥️ |
| D | Diamond | ♦️ |
| C | Club | ♣️ |
| S | Spade | ♠️ |

### Examples

```
AH   = Ace of Hearts
KD   = King of Diamonds
2C   = Two of Clubs
TS   = Ten of Spades
7H   = Seven of Hearts
QS   = Queen of Spades
```

---

## 🤖 AI Decision Logic

### Pre-Flop Decision Tree

```
IF hand_strength >= 70%
  → RAISE (95% confidence)
  "Premium hand - raise aggressively"

ELSE IF hand_strength >= 50%
  → CALL (75% confidence)
  "Good hand - call to see flop"

ELSE IF hand_strength >= 35%
  → CALL (50% confidence)
  "Marginal - call cautiously"

ELSE
  → FOLD (80% confidence)
  "Weak hand - fold"
```

### Flop Decision Tree

```
IF hand_strength >= 80%
  → RAISE (90% confidence)
  "Strong hand on [board_texture] board - bet for value"

ELSE IF hand_strength >= 60%
  IF board_texture == "wet"
    → CALL (70% confidence)
    "Good hand on wet board - proceed cautiously"
  ELSE
    → RAISE (75% confidence)
    "Good hand - bet for value"

ELSE IF hand_strength >= 40%
  → CALL (55% confidence)
  "Drawing hand - see turn card"

ELSE
  → FOLD (75% confidence)
  "Weak - fold"
```

### Turn Decision Tree

```
IF hand_strength >= 75%
  → RAISE (85% confidence)
  "Strong - value bet"

ELSE IF hand_strength >= 55%
  → CALL (70% confidence)
  "Good hand - see river"

ELSE IF hand_strength >= 35%
  → CALL (50% confidence)
  "Drawing - last card coming"

ELSE
  → FOLD (75% confidence)
  "Weak - fold"
```

### River Decision Tree

```
IF hand_strength >= 75%
  → SHOW (85% confidence)
  "Strong - go to showdown"

ELSE IF hand_strength >= 50%
  → SHOW (65% confidence)
  "Decent hand - showdown"

ELSE
  → FOLD (70% confidence)
  "Weak - fold if facing bet"
```

---

## 📈 Understanding the Analysis

### Win Probability Interpretation

```
33.3% (baseline for 3 players)

< 33%     = Disadvantage (worst position)
~33%      = Even (fair share)
33-40%    = Slight edge
40-50%    = Good position
50%+      = Strong favorite
```

### Hand Strength Interpretation

```
0-30%     = Very weak (usually fold)
30-40%    = Weak (fold most times)
40-50%    = Marginal/Drawing (play with caution)
50-60%    = Decent (reasonable equity)
60-75%    = Good (positive equity)
75-90%    = Very good (strong hand)
90%+      = Premium (very strong)
```

### Confidence Score

```
50-60%    = Uncertain decision (could go either way)
60-75%    = Reasonable confidence (fairly clear)
75-85%    = High confidence (clear decision)
85-95%+   = Very high confidence (obvious decision)
```

### Board Texture Impact

```
DRY BOARD:
- Made hands > Draws
- Value betting recommended
- Draw hands weaker

WET BOARD:
- Draws have more outs
- Made hands vulnerable
- Marginal hands risky
- Drawing hands stronger

COORDINATED BOARD:
- Balanced situation
- Mix of outcomes possible
```

---

## 🔧 Troubleshooting

### "Invalid card format" Error

```
Problem: Card not recognized
Solution: 
- Use format: RANKSUIT (no spaces)
- Valid: AH, KD, 2C, TS
- Invalid: A H, King of Hearts, AH KD (in same field)

Correct format:
Your cards: "AH KD"  (with space between cards)
Flop: "2H 3D 4C"     (with spaces between cards)
Turn: "5S"           (single card, no space)
River: "7H"          (single card, no space)
```

### "Duplicate cards detected" Error

```
Problem: Same card appears twice
Solution:
- Check your input for typos
- Each card must be unique across all inputs
- System will auto-regenerate AI cards if needed

Example:
Your cards: AH KD
Board: 2H 3D 4C
✓ All unique - OK

Your cards: AH KD
Board: 2H AD 4C  (AD is duplicate of A suit)
✗ Will auto-regenerate AI cards
```

### Probabilities Change Between Runs

```
This is NORMAL!
Reason: Monte Carlo simulation uses randomness

Each run:
- Generates new random opponent cards
- Runs new 3,000 random simulations
- Results vary ±1-2% due to randomness

If you want exact reproducibility:
- Set Python random seed (advanced)
- Or note that probabilities always converge over many iterations
```

### "Failed to resolve duplicates" Error

```
Problem: Rare - happens if AI card regeneration fails
Solution:
- Try entering different board cards
- Click "Start New Game" and try again
- System will regenerate everything fresh
```

---

## 📚 Advanced Concepts

### Why Monte Carlo Over Analytical?

```
MONTE CARLO (used here):
✓ Simple to implement
✓ Handles 3-player scenarios easily
✓ Fast enough for real-time
✓ Easy to understand
- Slightly less accurate than exact calculation

ANALYTICAL (alternative):
✓ 100% accurate
✓ No randomness/variance
- Complex to implement
- Slower to calculate
- Harder to understand
```

### Limitations of This Model

```
Simplified assumptions:
✗ Assumes all players reach showdown (no folding)
✗ Doesn't account for betting rounds/pot odds
✗ Treats opponents as randomly playing any 2 cards
✗ Doesn't model aggressive/conservative players
✗ Ignores position effects (button, blinds, etc.)

In real poker, consider:
+ Opponent tendencies
+ Pot odds and implied odds
+ Position and stack sizes
+ Opponent tells/patterns
+ Betting dynamics
```

### Improving Accuracy

```
Current accuracy: ±1-2% with 3,000 iterations

To improve (trade-off with speed):
1. Increase iterations to 5,000-10,000
   → More accurate but slower
2. Reduce iterations to 1,000
   → Faster but less accurate
3. Use analytical calculation
   → 100% accurate but complex

Current balance is optimal for:
- Learning
- Real-time analysis
- Understanding concepts
- Quick decision support
```

---

## 🎓 Learning Resources

### Understanding Poker Probability

```
Key concepts covered:
- Hand rankings and evaluation
- Equity calculation
- Board texture impact
- Multi-player dynamics
- Decision thresholds
- Confidence scoring
```

### How to Use for Learning

```
1. Try different hands:
   - Premium (AK, AA, KK)
   - Marginal (KJ, Q9)
   - Weak (27o, 32o)

2. Observe how probabilities change:
   - Pre-flop vs Flop vs Turn vs River
   - How much board impacts strength

3. Learn AI decision thresholds:
   - When to FOLD vs CALL vs RAISE
   - How confidence changes with info

4. Study board texture:
   - Play on dry boards (K72)
   - Play on wet boards (K♥J♥9♥)
   - Observe how recommendations differ
```

---

## 📝 Example Analysis Session

### Session: Learning Hand Strength

```
ROUND 1:
Your cards: AH KD (Premium)
Pre-flop strength: 68%
Decision: RAISE (95%)

Board: 2H 3D 4C (Dry)
Flop strength: 68%
Decision: RAISE (90%)

Board: 2H 3D 4C 5S (Still dry)
Turn strength: 68%
Decision: RAISE (85%)

Board: 2H 3D 4C 5S 7H (Complete)
Final: High Card (AK high)
Winner: AI 1 (Had pair)

Learning:
- Even premium hands don't always win
- High cards need to improve (pair, etc.)
- Luck factor exists in poker

---

ROUND 2:
Your cards: 7♥ 6♥ (Weak starting)
Pre-flop strength: 42%
Decision: CALL (50%)

Board: K♥ 9♥ 3♥ (WET - three-flushed!)
Flop strength: 52% (flush draw!)
Decision: CALL (55%)

Board: K♥ 9♥ 3♥ 4C (Still drawing)
Turn strength: 41% (draw didn't help)
Decision: CALL (50%)

Board: K♥ 9♥ 3♥ 4C 2♥ (Made flush!)
Final: Flush (K♥9♥7♥6♥5♥)
Winner: YOU

Learning:
- Drawing hands can improve dramatically
- Board texture matters
- Wet boards create opportunities
```

---

## 📞 Support

### Need Help?

1. **Card format issues?**
   - Check "Help & Card Reference" section in app
   - Format: RANKSUIT with spaces between cards

2. **Understanding probabilities?**
   - Read "Understanding the Analysis" section
   - Review examples and case studies

3. **Want to learn more?**
   - Run multiple sessions
   - Try different hand types
   - Observe how board affects decisions

---

## 🎯 Summary

This poker analyzer uses:
- **Monte Carlo simulation** for accurate probabilities
- **Exhaustive hand evaluation** for best 5-card selection
- **Stage-aware decision logic** that adapts to game situation
- **Board texture analysis** for contextual recommendations
- **Real-time calculation** with auto-regenerating AI cards

Perfect for:
✓ Learning poker strategy
✓ Understanding probability concepts
✓ Testing different hand scenarios
✓ Visualizing how game evolves
✓ Making informed poker decisions

---

**Ready to analyze? Start with your hole cards! 🎰🎯**

```bash
streamlit run poker.py
```
