#Coding Partners: Israel Lopez + Christopher Jimenez

import psycopg2
import random

connection = psycopg2.connect(database='game_db')
cursor = connection.cursor()

word_list = [
    "pokemon",
    "wealthiest",
    "bless",
    "rich",
    "yes",
    "hello",
    "pen",
    "python",
    "javascript",
    "express",
    "guitar",
    "html",
    "css",
    "mongoose",
    "react",
    "mongodb",
    "aws",
    "deployment",
    "devops",
    "postgresql",
    "database",
    "github",
    "postman",
    "vscode",
]

random_Word = None
correctGuesses = []
incorrectGuesses = []
wins = 0
losses = 0


def init():
    initialInput = int(input('1.Create a new account or 2.Login: '))
    if initialInput == 1:
        createPlayer()
    if initialInput == 2:
        cursor.execute('SELECT * FROM players')
        print(cursor.fetchall())
        loginId = int(input('Select your id: '))
        if loginId:
            return loginId
 
def createPlayer():
    name = input('What is your name? ')
    cursor.execute('INSERT INTO players (player_name) VALUES (%s)', [name])
    connection.commit()
    print('You have created a player named: ' + name)
    init()

def saveResult(id):
    cursor.execute('INSERT INTO saves (save_time, player_id) VALUES (CURRENT_TIMESTAMP, %s)', [id] )
    connection.commit()

def viewSaves(id):
    cursor.execute('SELECT * FROM players FULL OUTER JOIN saves ON players.id = saves.player_id WHERE saves.player_id = %s' ,[id])
    print(F'Your saves: {cursor.fetchall()}')


# Generate random word
def randomWord(list):
    global random_Word
    random_Word = random.choice(list)
    return random_Word

# Length of random word
def lengthOfWord(list):
    randomWord(list)
    # print(random_Word, len(random_Word))
    return len(random_Word)

# Display current state of word
def createDisplayString(word, correctGuesses):
    displayString = ""
    for letter in word:
        if letter in correctGuesses:
            displayString += letter
        else:
            displayString += "_"
    return displayString

# Start Game - Single Letter Guess Input
def startGame(list):
    while True:
    # Initialize global list variables inside function to reset each time the startGame() function is invoked - This avoids any residual data from previous games
        global correctGuesses, incorrectGuesses, wins, losses
        correctGuesses = []
        incorrectGuesses = []
        id = init()
        print(f'id you entered -> {id}')
        print(F"Welcome Player, this is Hangman and your word is - {lengthOfWord(list)} letters long and you have {6} guesses")
        while True:
            guess = input("What is your guess?: ").lower()
            # Here, we do a while loop to restrict and validate user input to a single alphabetical letter, no spaces, or empty string --> The method isalpha() returns True for alphabetical string and False for number, special characters, space, or empty string
            while len(guess) != 1 or not guess.isalpha():
                if len(guess) == 0:
                    print("You didn't enter anything, please enter a single letter")
                elif len(guess) > 1:
                    print("You entered mulitple letters, please enter only a single letter")
                elif not guess.isalpha():
                    print("Invalid input, please enter an alphabetical letter")
                guess = input("what is your guess?: ").lower()

            if guess in random_Word:
                if guess not in correctGuesses:
                    correctGuesses.append(guess)
                    displayString = createDisplayString(random_Word, correctGuesses)
                    print(F"Correct! Current word: {displayString}")
                else:
                    print("You alread guessed that letter")
            else:
                if len(incorrectGuesses) >= 5:
                    losses += 1
                    print(F"Sorry, you ran out of guesses. The word was {random_Word}")
                    saveResult(id)
                    break
                else:
                    incorrectGuesses.append(guess)
                    displayString = createDisplayString(random_Word, correctGuesses)
                    print(F"Wrong, Try again. Current word is - {displayString} - You have guessed {incorrectGuesses} and have {6 - len(incorrectGuesses)} guesses left")

            # Win Condition - Here, we are using the state of the "displayString" that is capturing the correct guesses and comparing them with the correct word --> Logic is in the createDisplayString() function, where if a letter from the generated word EXISTS in the correctGuesses list then it will populate the intially empty string and IN ORDER of the actual word, otherwise the string will display underscores (to represent empty available spaces) = If there are not more empty spaces and ALL letters of the word EXIST in the correctGuesses list, then the player has guessed all the letters and completed the word
            if "_" not in displayString:
                wins += 1
                print(f"Congratulations, you won! Your word was {random_Word}.")
                saveResult(id)
                break

        
        # Reset feature: We tried to nest the while loop for reset functionality inside both the lose and win conditions, but a bug was introduced that caused a prompt to come up again after typing "n" for no to the reset once a single cycle was completed beforehand --> Learned from ChatGPT about how nesting while loops like that and breaking or returning from them will get out of that while loop and onto what ever is outside of that --> To fix that, we had to separate the reset functionality to the main while loop of the function
        reset = input(F"You have {wins} victories and {losses} defeats - Do you want to play again? - Please type y (yes) or n (no): ").lower()
        while reset != "y" and reset != "n":
            reset = input("Invalid input. Please type y (yes) or n (no): ").lower()
        
        if reset == "n":
            print(F"Very well, you had {wins} victories and {losses} defeats - until next time...")
            viewSaves(id)
            break
            
startGame(word_list)


    




cursor.close()
connection.close()