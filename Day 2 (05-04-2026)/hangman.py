import random as r

stages = [
    """ Stage 6:
 ----------
    |   |
    O   |
   /|\  |
   / \  |
        |
        |
==========""",
    """ Stage 5:
 ----------
    |   |
    O   |
   /|\  |
   /    |
        |
        |
==========""",
    """ Stage 4:
 ----------
    |   |
    O   |
   /|\ |
        |
        |
        |
==========""",
    """ Stage 3:
 ----------
    |   |
    O   |
   /|   |
        |
        |
        |
==========""",
    """ Stage 2:
 ----------
    |   |
    O   |
    |   |
        |
        |
        |
==========""",
    """ Stage 1:
 ----------
    |   |
    O   |
        |
        |
        |
        |
==========""",
    """ Stage 0:
 ----------
    |   |
        |
        |
        |
        |
        |
=========="""]

word=input("Enter a word for Hangman: ")
word=word.upper()
word_list=list(word)
word_length=len(word)

# Create a display list with underscores
display = ["_"] * word_length

# Randomly reveal about 30% of the letters as a hint
num_to_reveal = max(1, word_length // 3)
indices = r.sample(range(word_length), num_to_reveal)
for i in indices:
    display[i] = word[i]

lives = 6
guessed_wrong = set()

while "_" in display and lives > 0:
    print(stages[lives])
    print(f"Word to guess: {' '.join(display)}")
    if guessed_wrong:
        print(f"Incorrect guesses so far: {', '.join(sorted(guessed_wrong))}")

    guess = input("\nGuess a letter: ").upper()

    # Input validation
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single valid letter.")
        continue

    if guess in display or guess in guessed_wrong:
        print(f"The letter '{guess}' has already been guessed or revealed. Try another.")
    if guess in guessed_wrong:
        print(f"You already guessed '{guess}' and it's not in the word. Try another.")
        continue

    # If the letter is already partially revealed, check if there are still hidden ones
    if guess in display:
        hidden_left = False
        for i in range(word_length):
            if word[i] == guess and display[i] == "_":
                hidden_left = True
        if not hidden_left:
            print(f"All instances of '{guess}' are already visible. Try another.")
            continue

    if guess in word:
        print(f"Good job! '{guess}' is in the word.")
        for i in range(word_length):
            if word[i] == guess:
                display[i] = guess
    else:
        guessed_wrong.add(guess)
        lives -= 1
        print(f"Incorrect! '{guess}' is not in the word. Lives left: {lives}")

if "_" not in display:
    print(" ".join(display))
    print("\nCongratulations! You guessed the word and won!")
else:
    print(stages[0])
    print(f"\nGame Over! You ran out of lives. The word was: {word}")
