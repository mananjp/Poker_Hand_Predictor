import streamlit as st
import random
import itertools
from collections import Counter


# ============================================================================
# POKER HAND EVALUATOR
# ============================================================================

class PokerHand:
    RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
             '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    SUITS = {'H': 'Heart', 'D': 'Diamond', 'C': 'Club', 'S': 'Spade'}
    ALL_RANKS = list(RANKS.keys())
    ALL_SUITS = list(SUITS.keys())

    @staticmethod
    def parse_card(card_str):
        """Parse card string like '2H', 'AH' into rank and suit"""
        if len(card_str) < 2:
            raise ValueError(f"Invalid card format: {card_str}")
        rank = card_str[:-1].upper()
        suit = card_str[-1].upper()
        if suit not in 'HDCS':
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in PokerHand.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        return rank, suit

    @staticmethod
    def evaluate_hand(cards):
        """Evaluate a 5-card hand. Returns tuple for comparison."""
        if len(cards) != 5:
            raise ValueError(f"Expected 5 cards, got {len(cards)}")

        ranks = [PokerHand.RANKS[PokerHand.parse_card(card)[0]] for card in cards]
        suits = [PokerHand.parse_card(card)[1] for card in cards]

        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        is_flush = len(suit_counts) == 1

        sorted_ranks = sorted(ranks, reverse=True)
        is_straight = False
        straight_high = 0

        if sorted_ranks[0] - sorted_ranks[4] == 4:
            is_straight = True
            straight_high = sorted_ranks[0]
        elif sorted_ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5

        counts = sorted(rank_counts.values(), reverse=True)
        unique_ranks = sorted(set(ranks), reverse=True)

        if is_straight and is_flush:
            if straight_high == 14 and 13 not in unique_ranks:
                return (9, straight_high)
            return (8, straight_high)
        elif counts == [4, 1]:
            four_kind = [r for r, c in rank_counts.items() if c == 4][0]
            return (7, four_kind)
        elif counts == [3, 2]:
            three_kind = [r for r, c in rank_counts.items() if c == 3][0]
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            return (6, three_kind, pair)
        elif is_flush:
            return (5, tuple(sorted_ranks))
        elif is_straight:
            return (4, straight_high)
        elif counts == [3, 1, 1]:
            three_kind = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (3, three_kind, tuple(kickers))
        elif counts == [2, 2, 1]:
            pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (2, tuple(pairs), kicker)
        elif counts == [2, 1, 1, 1]:
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (1, pair, tuple(kickers))
        else:
            return (0, tuple(sorted_ranks))

    @staticmethod
    def best_five_from_seven(cards):
        """Find best 5-card hand from 7 cards"""
        best_hand = None
        best_score = None

        for combo in itertools.combinations(cards, 5):
            score = PokerHand.evaluate_hand(combo)
            if best_score is None or score > best_score:
                best_score = score
                best_hand = combo

        return best_hand, best_score

    @staticmethod
    def hand_rank_name(score):
        """Convert score to hand name"""
        names = {
            9: "🏆 Royal Flush",
            8: "🔥 Straight Flush",
            7: "👑 Four of a Kind",
            6: "💎 Full House",
            5: "✨ Flush",
            4: "🎯 Straight",
            3: "🎪 Three of a Kind",
            2: "👥 Two Pair",
            1: "👉 One Pair",
            0: "🎲 High Card"
        }
        return names.get(score[0], "Unknown")


# ============================================================================
# AI DECISION SYSTEM
# ============================================================================

class PokerAI:
    """AI system for poker decisions"""

    @staticmethod
    def calculate_hand_strength(player_cards, board_cards, num_sims=500):
        """Calculate hand strength as percentage (0-100)"""
        all_cards = []
        for rank in PokerHand.ALL_RANKS:
            for suit in PokerHand.ALL_SUITS:
                all_cards.append(rank + suit)

        known = set(player_cards + board_cards)
        remaining = [c for c in all_cards if c not in known]

        if len(remaining) < 2:
            return 100.0

        wins = 0
        total = 0

        for _ in range(min(num_sims, max(50, len(remaining) // 2))):
            opp_cards = random.sample(remaining, min(2, len(remaining)))
            if len(opp_cards) < 2:
                continue

            sim_remaining = [c for c in remaining if c not in opp_cards]
            cards_needed = 5 - len(board_cards)

            if cards_needed > 0 and len(sim_remaining) >= cards_needed:
                sim_board = board_cards + random.sample(sim_remaining, cards_needed)
            else:
                sim_board = board_cards

            try:
                _, player_hand = PokerHand.best_five_from_seven(player_cards + sim_board)
                _, opp_hand = PokerHand.best_five_from_seven(opp_cards + sim_board)

                if player_hand >= opp_hand:
                    wins += 1
            except:
                pass

            total += 1

        return (wins / total * 100) if total > 0 else 50.0

    @staticmethod
    def get_board_texture(board_cards):
        """Analyze board texture"""
        if len(board_cards) < 3:
            return "unknown"

        ranks = [PokerHand.RANKS[c[0]] for c in board_cards[:3]]
        suits = [c[1] for c in board_cards[:3]]

        suit_counts = Counter(suits)
        is_suited = any(count >= 2 for count in suit_counts.values())

        sorted_ranks = sorted(ranks, reverse=True)
        is_connected = (sorted_ranks[0] - sorted_ranks[1] <= 2) and \
                       (sorted_ranks[1] - sorted_ranks[2] <= 2)

        if is_suited and is_connected:
            return "wet"
        elif is_suited or is_connected:
            return "coordinated"
        else:
            return "dry"

    @staticmethod
    def recommend_action(player_cards, board_cards):
        """AI decision engine - returns (action, confidence, reason, hand_strength)"""
        hand_strength = PokerAI.calculate_hand_strength(player_cards, board_cards, 300)
        board_texture = PokerAI.get_board_texture(board_cards)

        board_len = len(board_cards)
        if board_len == 0:
            stage = "preflop"
        elif board_len == 3:
            stage = "flop"
        elif board_len == 4:
            stage = "turn"
        else:
            stage = "river"

        # Decision logic
        if stage == "preflop":
            if hand_strength >= 70:
                return ("RAISE", 95, f"Premium hand ({hand_strength:.1f}%) - raise aggressively", hand_strength)
            elif hand_strength >= 50:
                return ("CALL", 75, f"Good hand ({hand_strength:.1f}%) - call to see flop", hand_strength)
            elif hand_strength >= 35:
                return ("CALL", 50, f"Marginal ({hand_strength:.1f}%) - call cautiously", hand_strength)
            else:
                return ("FOLD", 80, f"Weak hand ({hand_strength:.1f}%) - fold", hand_strength)

        elif stage == "flop":
            if hand_strength >= 80:
                return ("RAISE", 90, f"Strong hand ({hand_strength:.1f}%) on {board_texture} board - bet for value",
                        hand_strength)
            elif hand_strength >= 60:
                if board_texture == "wet":
                    return (
                    "CALL", 70, f"Good hand ({hand_strength:.1f}%) on wet board - proceed cautiously", hand_strength)
                else:
                    return ("RAISE", 75, f"Good hand ({hand_strength:.1f}%) - bet for value", hand_strength)
            elif hand_strength >= 40:
                return ("CALL", 55, f"Drawing hand ({hand_strength:.1f}%) - see turn card", hand_strength)
            else:
                return ("FOLD", 75, f"Weak ({hand_strength:.1f}%) - fold", hand_strength)

        elif stage == "turn":
            if hand_strength >= 75:
                return ("RAISE", 85, f"Strong ({hand_strength:.1f}%) - value bet", hand_strength)
            elif hand_strength >= 55:
                return ("CALL", 70, f"Good hand ({hand_strength:.1f}%) - see river", hand_strength)
            elif hand_strength >= 35:
                return ("CALL", 50, f"Drawing ({hand_strength:.1f}%) - last card coming", hand_strength)
            else:
                return ("FOLD", 75, f"Weak ({hand_strength:.1f}%) - fold", hand_strength)

        else:  # river
            if hand_strength >= 75:
                return ("SHOW", 85, f"Strong ({hand_strength:.1f}%) - go to showdown", hand_strength)
            elif hand_strength >= 50:
                return ("SHOW", 65, f"Decent hand ({hand_strength:.1f}%) - showdown", hand_strength)
            else:
                return ("FOLD", 70, f"Weak ({hand_strength:.1f}%) - fold if facing bet", hand_strength)


# ============================================================================
# PROBABILITY CALCULATOR
# ============================================================================

def calculate_win_probabilities(player1_cards, player2_cards, player3_cards,
                                current_board, num_simulations=3000):
    """Calculate win/tie probabilities for all 3 players"""

    known_cards = set(player1_cards + player2_cards + player3_cards + current_board)

    all_cards = []
    for rank in PokerHand.ALL_RANKS:
        for suit in PokerHand.ALL_SUITS:
            all_cards.append(rank + suit)

    remaining_cards = [c for c in all_cards if c not in known_cards]

    player1_wins = 0
    player2_wins = 0
    player3_wins = 0
    ties = 0

    for _ in range(num_simulations):
        cards_needed = 5 - len(current_board)
        if cards_needed > 0 and len(remaining_cards) >= cards_needed:
            additional_cards = random.sample(remaining_cards, cards_needed)
        else:
            additional_cards = []
        complete_board = current_board + additional_cards

        p1_hand, p1_score = PokerHand.best_five_from_seven(player1_cards + complete_board)
        p2_hand, p2_score = PokerHand.best_five_from_seven(player2_cards + complete_board)
        p3_hand, p3_score = PokerHand.best_five_from_seven(player3_cards + complete_board)

        scores = [(p1_score, 1), (p2_score, 2), (p3_score, 3)]
        scores.sort(reverse=True)

        best_score = scores[0][0]
        winners = [s[1] for s in scores if s[0] == best_score]

        if len(winners) > 1:
            ties += 1
        elif winners[0] == 1:
            player1_wins += 1
        elif winners[0] == 2:
            player2_wins += 1
        else:
            player3_wins += 1

    total = num_simulations
    return {
        'player1_win': (player1_wins / total) * 100,
        'player2_win': (player2_wins / total) * 100,
        'player3_win': (player3_wins / total) * 100,
        'ties': (ties / total) * 100
    }


def generate_random_cards(excluded_cards):
    """Generate 2 random cards not in excluded set"""
    all_cards = []
    for rank in PokerHand.ALL_RANKS:
        for suit in PokerHand.ALL_SUITS:
            all_cards.append(rank + suit)

    available = [c for c in all_cards if c not in excluded_cards]
    return random.sample(available, 2)


def display_stage_analysis(stage_name, p1_cards, p2_cards, p3_cards, board_cards):
    """Display analysis for a specific stage"""

    # Calculate probabilities
    probs = calculate_win_probabilities(p1_cards, p2_cards, p3_cards, board_cards, num_simulations=3000)

    # Get AI recommendations
    action1, conf1, reason1, strength1 = PokerAI.recommend_action(p1_cards, board_cards)
    action2, conf2, reason2, strength2 = PokerAI.recommend_action(p2_cards, board_cards)
    action3, conf3, reason3, strength3 = PokerAI.recommend_action(p3_cards, board_cards)

    # Display stage header
    st.markdown(f"### 📍 **{stage_name}**")
    st.write(f"Board: **{' '.join(board_cards) if board_cards else 'Empty (Pre-Flop)'}**")

    # Win probabilities
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("You Win %", f"{probs['player1_win']:.1f}%")
    with col2:
        st.metric("AI 1 Win %", f"{probs['player2_win']:.1f}%")
    with col3:
        st.metric("AI 2 Win %", f"{probs['player3_win']:.1f}%")
    with col4:
        st.metric("Ties", f"{probs['ties']:.1f}%")

    # AI Recommendations
    st.markdown("**🤖 Recommendations:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("**👤 YOU**")
            st.write(f"**{action1}** ({conf1}%)")
            st.write(f"Strength: {strength1:.1f}%")
            st.caption(reason1)

    with col2:
        with st.container(border=True):
            st.markdown("**🤖 AI 1**")
            st.write(f"**{action2}** ({conf2}%)")
            st.write(f"Strength: {strength2:.1f}%")
            st.caption(reason2)

    with col3:
        with st.container(border=True):
            st.markdown("**🤖 AI 2**")
            st.write(f"**{action3}** ({conf3}%)")
            st.write(f"Strength: {strength3:.1f}%")
            st.caption(reason3)

    st.divider()


# ============================================================================
# STREAMLIT UI
# ============================================================================

st.set_page_config(page_title="🎰 Poker Step-by-Step Analyzer", layout="wide")

st.title("🎰 Poker Step-by-Step Analyzer")
st.markdown("""
**Progressive Analysis:** Enter your cards, then add board cards one stage at a time and see:
- Win probabilities at each stage
- AI recommendations
- How the game changes with each new card
""")

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'p1_cards' not in st.session_state:
    st.session_state.p1_cards = []
if 'p2_cards' not in st.session_state:
    st.session_state.p2_cards = []
if 'p3_cards' not in st.session_state:
    st.session_state.p3_cards = []
if 'flop_cards' not in st.session_state:
    st.session_state.flop_cards = []
if 'turn_card' not in st.session_state:
    st.session_state.turn_card = None
if 'river_card' not in st.session_state:
    st.session_state.river_card = None

# ============================================================================
# STEP 1: GET YOUR CARDS
# ============================================================================

st.header("Step 1️⃣: Your Hole Cards")

col1, col2 = st.columns([3, 1])
with col1:
    your_cards_input = st.text_input(
        "Enter your 2 hole cards (e.g., 'AH KD')",
        placeholder="2 cards separated by space",
        key="your_cards"
    )

# Validate and store your cards
if your_cards_input:
    try:
        cards = your_cards_input.strip().split()
        if len(cards) != 2:
            st.error("❌ Please enter exactly 2 cards")
            st.stop()

        for card in cards:
            PokerHand.parse_card(card)

        st.session_state.p1_cards = [c.upper() for c in cards]
        st.success(f"✅ Your cards: {' '.join(st.session_state.p1_cards)}")

        # Generate opponent cards only once
        if not st.session_state.game_started:
            known_cards = set(st.session_state.p1_cards)
            st.session_state.p2_cards = generate_random_cards(known_cards)
            known_cards.update(st.session_state.p2_cards)
            st.session_state.p3_cards = generate_random_cards(known_cards)
            st.session_state.game_started = True
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.stop()

if not st.session_state.p1_cards:
    st.info("👆 Enter your cards to continue")
    st.stop()

# ============================================================================
# STEP 2: PRE-FLOP ANALYSIS
# ============================================================================

st.header("Step 2️⃣: Pre-Flop Analysis")

with st.expander("📊 Pre-Flop Analysis", expanded=True):
    display_stage_analysis("Pre-Flop",
                           st.session_state.p1_cards,
                           st.session_state.p2_cards,
                           st.session_state.p3_cards,
                           [])

# ============================================================================
# STEP 3: FLOP
# ============================================================================

st.header("Step 3️⃣: The Flop")

col1, col2 = st.columns([3, 1])
with col1:
    flop_input = st.text_input(
        "Enter 3 flop cards (e.g., '2H 3D 4C')",
        placeholder="3 cards separated by space",
        key="flop"
    )

flop_valid = False
if flop_input:
    try:
        cards = flop_input.strip().split()
        if len(cards) != 3:
            st.error("❌ Please enter exactly 3 cards for the flop")
            st.stop()

        for card in cards:
            PokerHand.parse_card(card)

        cards = [c.upper() for c in cards]

        # Check duplicates with current AI cards
        all_cards = set(st.session_state.p1_cards + st.session_state.p2_cards +
                        st.session_state.p3_cards + cards)

        if len(all_cards) != 9:
            # DUPLICATE DETECTED - Regenerate AI cards
            st.warning("⚠️ Duplicate detected with initial AI cards. Regenerating AI opponent cards...")

            # Regenerate AI cards to avoid duplicates
            excluded = set(st.session_state.p1_cards + cards)
            st.session_state.p2_cards = generate_random_cards(excluded)
            excluded.update(st.session_state.p2_cards)
            st.session_state.p3_cards = generate_random_cards(excluded)

            # Verify again
            all_cards = set(st.session_state.p1_cards + st.session_state.p2_cards +
                            st.session_state.p3_cards + cards)

            if len(all_cards) == 9:
                st.session_state.flop_cards = cards
                flop_valid = True
                st.success(f"✅ Flop: {' '.join(cards)} (AI cards regenerated)")
            else:
                st.error("❌ Failed to resolve duplicates. Please try again.")
                st.stop()
        else:
            st.session_state.flop_cards = cards
            flop_valid = True
            st.success(f"✅ Flop: {' '.join(cards)}")

    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.stop()

if flop_valid:
    with st.expander("📊 Flop Analysis", expanded=True):
        display_stage_analysis("Flop",
                               st.session_state.p1_cards,
                               st.session_state.p2_cards,
                               st.session_state.p3_cards,
                               st.session_state.flop_cards)

    # ============================================================================
    # STEP 4: TURN
    # ============================================================================

    st.header("Step 4️⃣: The Turn")

    col1, col2 = st.columns([3, 1])
    with col1:
        turn_input = st.text_input(
            "Enter 1 turn card (e.g., '5S')",
            placeholder="1 card",
            key="turn"
        )

    turn_valid = False
    if turn_input:
        try:
            card = turn_input.strip().upper()
            PokerHand.parse_card(card)

            # Check duplicates
            all_cards = set(st.session_state.p1_cards + st.session_state.p2_cards +
                            st.session_state.p3_cards + st.session_state.flop_cards + [card])

            if len(all_cards) != 10:
                # DUPLICATE DETECTED - Regenerate AI cards
                st.warning("⚠️ Duplicate detected. Regenerating AI opponent cards...")

                # Regenerate AI cards to avoid duplicates
                excluded = set(st.session_state.p1_cards + st.session_state.flop_cards + [card])
                st.session_state.p2_cards = generate_random_cards(excluded)
                excluded.update(st.session_state.p2_cards)
                st.session_state.p3_cards = generate_random_cards(excluded)

                # Verify again
                all_cards = set(st.session_state.p1_cards + st.session_state.p2_cards +
                                st.session_state.p3_cards + st.session_state.flop_cards + [card])

                if len(all_cards) == 10:
                    st.session_state.turn_card = card
                    turn_valid = True
                    st.success(f"✅ Turn: {card} (AI cards regenerated)")
                else:
                    st.error("❌ Failed to resolve duplicates. Please try again.")
                    st.stop()
            else:
                st.session_state.turn_card = card
                turn_valid = True
                st.success(f"✅ Turn: {card}")

        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.stop()

    if turn_valid:
        turn_board = st.session_state.flop_cards + [st.session_state.turn_card]

        with st.expander("📊 Turn Analysis", expanded=True):
            display_stage_analysis("Turn",
                                   st.session_state.p1_cards,
                                   st.session_state.p2_cards,
                                   st.session_state.p3_cards,
                                   turn_board)

        # ============================================================================
        # STEP 5: RIVER
        # ============================================================================

        st.header("Step 5️⃣: The River")

        col1, col2 = st.columns([3, 1])
        with col1:
            river_input = st.text_input(
                "Enter 1 river card (e.g., '7H')",
                placeholder="1 card",
                key="river"
            )

        if river_input:
            try:
                card = river_input.strip().upper()
                PokerHand.parse_card(card)

                # Check duplicates
                all_cards = set(st.session_state.p1_cards + st.session_state.p2_cards +
                                st.session_state.p3_cards + st.session_state.flop_cards +
                                [st.session_state.turn_card] + [card])

                if len(all_cards) != 11:
                    # DUPLICATE DETECTED - Regenerate AI cards
                    st.warning("⚠️ Duplicate detected. Regenerating AI opponent cards...")

                    # Regenerate AI cards to avoid duplicates
                    excluded = set(st.session_state.p1_cards + st.session_state.flop_cards +
                                   [st.session_state.turn_card] + [card])
                    st.session_state.p2_cards = generate_random_cards(excluded)
                    excluded.update(st.session_state.p2_cards)
                    st.session_state.p3_cards = generate_random_cards(excluded)

                    # Verify again
                    all_cards = set(st.session_state.p1_cards + st.session_state.p2_cards +
                                    st.session_state.p3_cards + st.session_state.flop_cards +
                                    [st.session_state.turn_card] + [card])

                    if len(all_cards) != 11:
                        st.error("❌ Failed to resolve duplicates. Please try again.")
                        st.stop()

                st.session_state.river_card = card
                st.success(f"✅ River: {card}")

                final_board = turn_board + [card]

                with st.expander("📊 River Analysis", expanded=True):
                    display_stage_analysis("River",
                                           st.session_state.p1_cards,
                                           st.session_state.p2_cards,
                                           st.session_state.p3_cards,
                                           final_board)

                # ============================================================================
                # FINAL SHOWDOWN
                # ============================================================================

                st.header("🏆 FINAL SHOWDOWN")

                final_board_list = st.session_state.flop_cards + [st.session_state.turn_card,
                                                                  st.session_state.river_card]

                # Get best hands
                hand1, score1 = PokerHand.best_five_from_seven(st.session_state.p1_cards + final_board_list)
                hand2, score2 = PokerHand.best_five_from_seven(st.session_state.p2_cards + final_board_list)
                hand3, score3 = PokerHand.best_five_from_seven(st.session_state.p3_cards + final_board_list)

                st.markdown(f"**Board:** {' '.join(final_board_list)}")
                st.markdown("---")

                col1, col2, col3 = st.columns(3)

                with col1:
                    with st.container(border=True):
                        st.markdown("### 👤 **YOU**")
                        st.markdown(f"**{PokerHand.hand_rank_name(score1)}**")
                        st.code(' '.join(hand1), language="text")

                with col2:
                    with st.container(border=True):
                        st.markdown("### 🤖 **AI 1**")
                        st.markdown(f"**{PokerHand.hand_rank_name(score2)}**")
                        st.code(f"{' '.join(st.session_state.p2_cards)} → {' '.join(hand2)}", language="text")

                with col3:
                    with st.container(border=True):
                        st.markdown("### 🤖 **AI 2**")
                        st.markdown(f"**{PokerHand.hand_rank_name(score3)}**")
                        st.code(f"{' '.join(st.session_state.p3_cards)} → {' '.join(hand3)}", language="text")

                st.markdown("---")

                # Determine winner
                scores = [(score1, "You"), (score2, "AI 1"), (score3, "AI 2")]
                scores.sort(reverse=True)

                if scores[0][0] == scores[1][0]:
                    st.warning(f"🤝 **TIE!** Multiple players have {PokerHand.hand_rank_name(scores[0][0])}")
                else:
                    if scores[0][1] == "You":
                        st.success(f"🎉 **YOU WIN!** with {PokerHand.hand_rank_name(scores[0][0])}!")
                    else:
                        st.info(f"**{scores[0][1]} wins** with {PokerHand.hand_rank_name(scores[0][0])}")

                # Ranking
                st.markdown("**Ranking:**")
                for i, (score, player) in enumerate(scores, 1):
                    st.markdown(f"{i}. **{player}** - {PokerHand.hand_rank_name(score)}")

                # Reset button
                st.markdown("---")
                if st.button("🔄 Start New Game"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

            except ValueError as e:
                st.error(f"❌ {str(e)}")
                st.stop()

# ============================================================================
# HELP SECTION
# ============================================================================

with st.expander("📖 Help & Card Reference"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Ranks (Values):**
        - 2-9: Face value
        - T: 10
        - J: Jack
        - Q: Queen
        - K: King
        - A: Ace (highest)
        """)

    with col2:
        st.markdown("""
        **Suits:**
        - H: Heart ♥️
        - D: Diamond ♦️
        - C: Club ♣️
        - S: Spade ♠️
        """)

    st.markdown("""
    **Examples:**
    - AH = Ace of Hearts
    - KD = King of Diamonds
    - 2C = Two of Clubs
    - TS = Ten of Spades

    **Input Format:**
    - Separate cards with spaces
    - No special characters needed
    - Case insensitive

    **Your Example:**
    - Your cards: 2S 9S ✅ (Both spades - suited!)
    - Flop: 6C 3H 4S ✅ (Valid - AI cards auto-adjusted)
    """)