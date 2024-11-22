import random
import streamlit as st

# App title
st.title("Number Guessing Game")

# Allow the user to set a custom range
st.subheader("Set the Range for the Game")
use_custom_range = st.checkbox("Do you want to set a custom range?", value=False)

if use_custom_range:
    range_min = st.number_input("Enter the minimum value:", value=0, step=1)
    range_max = st.number_input("Enter the maximum value:", value=100, step=1)
    if range_min >= range_max:
        st.error("Minimum value must be less than maximum value.")
else:
    range_min = 0
    range_max = 100

# Game mode selection
mode = st.radio("Choose a mode:", ("You Guess the Number", "Computer Guesses the Number"))

# --- YOU GUESS THE NUMBER MODE ---
if mode == "You Guess the Number":
    # Initialize session state for the game
    if "number_to_guess" not in st.session_state:
        st.session_state["number_to_guess"] = random.randint(range_min, range_max)

    if "attempts" not in st.session_state:
        st.session_state["attempts"] = 0

    # Default number of attempts
    total_attempts = st.number_input(
        "Set total number of attempts (default is 5):", min_value=1, value=5
    )
    if "max_attempts" not in st.session_state:
        st.session_state["max_attempts"] = total_attempts

    st.subheader(f"Guess a number between {range_min} and {range_max}!")
    user_guess = st.number_input(f"Enter your guess:", min_value=range_min, max_value=range_max, step=1)

    if st.button("Submit Guess"):
        st.session_state["attempts"] += 1
        remaining_attempts = st.session_state["max_attempts"] - st.session_state["attempts"]

        if user_guess == st.session_state["number_to_guess"]:
            st.success(
                f"🎉 Congratulations! You guessed the correct number ({st.session_state['number_to_guess']}) in {st.session_state['attempts']} attempts!"
            )
            if st.button("Play Again"):
                st.session_state["number_to_guess"] = random.randint(range_min, range_max)
                st.session_state["attempts"] = 0
                st.session_state["max_attempts"] = total_attempts
        elif st.session_state["attempts"] >= st.session_state["max_attempts"]:
            st.error(f"❌ You've used all your attempts! The number was {st.session_state['number_to_guess']}.")
            if st.button("Try Again"):
                st.session_state["number_to_guess"] = random.randint(range_min, range_max)
                st.session_state["attempts"] = 0
                st.session_state["max_attempts"] = total_attempts
        elif user_guess < st.session_state["number_to_guess"]:
            st.info(f"🔼 Try a higher number. Attempts left: {remaining_attempts}")
        else:
            st.info(f"🔽 Try a lower number. Attempts left: {remaining_attempts}")

    st.write(f"Attempts used: {st.session_state['attempts']} / {st.session_state['max_attempts']}")

# --- COMPUTER GUESSES THE NUMBER MODE ---
if mode == "Computer Guesses the Number":
    if "low" not in st.session_state:
        st.session_state["low"] = range_min

    if "high" not in st.session_state:
        st.session_state["high"] = range_max

    if "computer_attempts" not in st.session_state:
        st.session_state["computer_attempts"] = 0

    st.subheader(f"Think of a number between {range_min} and {range_max}, and I will try to guess it!")
    limited_attempts = st.checkbox("Do you want to limit the number of attempts?", value=False)

    if limited_attempts:
        max_computer_attempts = st.number_input(
            "Set total attempts for me (binary search will be used):", min_value=1, value=7
        )
    else:
        max_computer_attempts = None  # Unlimited

    computer_guess = (st.session_state["low"] + st.session_state["high"]) // 2

    if st.button("Computer's Guess"):
        st.write(f"My guess is: {computer_guess}")
        st.session_state["computer_attempts"] += 1

    feedback = st.radio(
        "Is my guess too high, too low, or correct?",
        ("Too High", "Too Low", "Correct"),
        key="feedback"
    )

    if st.button("Submit Feedback"):
        if feedback == "Too High":
            st.session_state["high"] = computer_guess - 1
        elif feedback == "Too Low":
            st.session_state["low"] = computer_guess + 1
        elif feedback == "Correct":
            st.success(
                f"🎉 I guessed your number ({computer_guess}) in {st.session_state['computer_attempts']} attempts!"
            )
            if st.button("Play Again"):
                st.session_state["low"] = range_min
                st.session_state["high"] = range_max
                st.session_state["computer_attempts"] = 0

        # Check if attempts are exhausted in limited mode
        if limited_attempts and st.session_state["computer_attempts"] >= max_computer_attempts:
            st.error(
                f"❌ I couldn't guess your number within {max_computer_attempts} attempts!"
            )
            if st.button("Try Again"):
                st.session_state["low"] = range_min
                st.session_state["high"] = range_max
                st.session_state["computer_attempts"] = 0

    # Display attempts
    st.write(f"Attempts used: {st.session_state['computer_attempts']}")
    if limited_attempts:
        st.write(f"Max attempts allowed: {max_computer_attempts}")