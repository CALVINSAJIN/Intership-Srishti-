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

# Randomly reveal about 30% of the unique letters as a hint
unique_letters = list(set(word))
num_to_reveal = max(1, len(unique_letters) // 3)
letters_to_reveal = r.sample(unique_letters, num_to_reveal)
for char in letters_to_reveal:
    for i in range(word_length):
        if word[i] == char:
            display[i] = char

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
