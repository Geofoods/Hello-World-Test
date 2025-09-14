#!/usr/bin/env python3
"""
Simple Wordle clone (terminal).
- 5-letter words
- 6 guesses
- Uses ANSI colors for feedback (green = correct spot, yellow = present, gray = absent)
- Tries to load 'wordlist.txt' (one 5-letter word per line). If not found, uses a small builtin list.
"""

import random
import sys
import os

# ANSI color codes (works in most terminals)
GREEN = "\033[42m\033[30m"   # green background, black text
YELLOW = "\033[43m\033[30m"  # yellow background, black text
GRAY = "\033[47m\033[30m"    # white/gray background, black text
RESET = "\033[0m"

WORD_LENGTH = 5
MAX_GUESSES = 6

def load_word_list(path="wordlist.txt"):
    """Load words from a file (one word per line). Only keep words of the correct length."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            words = [w.strip().lower() for w in f if len(w.strip()) == WORD_LENGTH and w.strip().isalpha()]
        if not words:
            raise ValueError("No valid words found in file.")
        return words
    except Exception:
        # fallback small list if file missing or empty
        return [
            "crane", "slate", "fling", "clock", "spare", "trend", "plant", "shock",
            "globe", "pride", "shard", "chart", "flute", "brush", "trace", "wield",
            "candy", "fuzzy", "vivid", "about", "house", "grain", "money", "skill"
        ]

def get_feedback(secret, guess):
    """
    Return a list of (char, status) where status is:
      'green'  -> correct letter & position
      'yellow' -> letter in word but wrong position
      'gray'   -> letter not in word (or already matched)
    Implements Wordle rules for repeated letters.
    """
    secret = secret.lower()
    guess = guess.lower()
    result = ['gray'] * WORD_LENGTH

    # Step 1: mark greens and build counts for remaining secret letters
    secret_remaining_counts = {}
    for i in range(WORD_LENGTH):
        if guess[i] == secret[i]:
            result[i] = 'green'
        else:
            secret_remaining_counts[secret[i]] = secret_remaining_counts.get(secret[i], 0) + 1

    # Step 2: mark yellows if letter still available in remaining counts
    for i in range(WORD_LENGTH):
        if result[i] == 'green':
            continue
        gch = guess[i]
        if secret_remaining_counts.get(gch, 0) > 0:
            result[i] = 'yellow'
            secret_remaining_counts[gch] -= 1
        else:
            result[i] = 'gray'

    return list(zip(guess, result))

def colored_feedback(feedback_pairs):
    """Return a colored string for terminal display from feedback pairs."""
    out = []
    for ch, status in feedback_pairs:
        if status == 'green':
            out.append(f"{GREEN}{ch.upper()}{RESET}")
        elif status == 'yellow':
            out.append(f"{YELLOW}{ch.upper()}{RESET}")
        else:
            out.append(f"{GRAY}{ch.upper()}{RESET}")
    return " ".join(out)

def play(words):
    secret = random.choice(words)
    # Uncomment next line for debugging (see the secret)
    # print(f"(DEBUG) secret: {secret}")

    print("WELCOME TO PYWORDLE!")
    print(f"You have {MAX_GUESSES} guesses to find a {WORD_LENGTH}-letter word.")
    print("Green = correct place. Yellow = present but wrong place. Gray = not present.")
    print()

    allowed = set(words)  # valid guesses = same list (you can expand)

    guess_num = 0
    while guess_num < MAX_GUESSES:
        guess_num += 1
        while True:
            guess = input(f"Guess {guess_num}/{MAX_GUESSES}: ").strip().lower()
            if len(guess) != WORD_LENGTH:
                print(f"Please enter exactly {WORD_LENGTH} letters.")
                continue
            if not guess.isalpha():
                print("Please use only alphabetic characters.")
                continue
            if guess not in allowed:
                # allow any 5-letter word if you prefer, but we check against list to mimic Wordle's accepted guesses
                print("Word not in allowed list. Try another word.")
                continue
            break

        pairs = get_feedback(secret, guess)
        print(colored_feedback(pairs))
        print()

        if all(status == 'green' for _, status in pairs):
            print(f"Nice! You guessed the word in {guess_num} guesses 🎉")
            return

    print(f"Out of guesses — the word was: {secret.upper()}. Better luck next time!")

def main():
    words = load_word_list()
    # Normalize words
    words = [w.lower() for w in words if len(w) == WORD_LENGTH]

    # allow user to choose play multiple times
    while True:
        play(words)
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ('y', 'yes'):
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
