import csv
import random
import string

from colorama import Fore, Back, Style, init  # import this stuff to add pretty "pretty printing"
import numpy as np

input_dictionary = {  # Dictionary for flexible input
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24, "twenty-five": 25
}


def flexible_input(question):
    user_input = input(question).lower()  # Convert to lowercase to catch every answer
    if user_input.isdigit():
        return int(user_input)
    if user_input in input_dictionary:
        return input_dictionary[user_input]
    return -1  # Return -1 for invalid input


def export_list_to_text_file(lst, filename):
    try:
        with open(filename, 'w') as f:
            for item in lst:
                f.write(str(item) + '\n')
        print("List exported successfully to", filename)
    except Exception as e:
        print("Error:", e)

def remove_words_with_consecutive_letters(words, letters):
    new_words = []
    for word in words:
        wordIsValid = True
        for letter in range(len(word)-1):
            if word[letter] in letters and word[letter+1] in letters:
                wordIsValid = False
        if wordIsValid:
            new_words.append(word)
    return new_words


class Puzzle:
    def __init__(self):
        self.remaining_alphabet = None
        self.letters = []
        self.top_side = []
        self.bottom_side = []
        self.right_side = []
        self.left_side = []
        self.word_list = []
        self.starting_letter = None
        self.move = 0

    def generate_letters(self):
        self.letters = []
        alphabet = [string.ascii_lowercase[i] for i in range(26)]
        sides = 4
        size_sides = 3
        for i in range(sides):  # Creates a list out of the alphabet with each character that's selected being unique
            for j in range(size_sides):
                random_number = random.randint(0, len(alphabet) - 1)
                self.letters.append(alphabet[random_number])
                alphabet.pop(random_number)
        self.top_side = [self.letters[0], self.letters[1], self.letters[2]]
        self.right_side = [self.letters[3], self.letters[4], self.letters[5]]
        self.bottom_side = [self.letters[6], self.letters[7], self.letters[8]]
        self.left_side = [self.letters[9], self.letters[10], self.letters[11]]
        self.remaining_alphabet = alphabet

    def read_puzzle(self, text):
        self.top_side = []
        self.bottom_side = []
        self.right_side = []
        self.left_side = []
        alphabet = [string.ascii_lowercase[i] for i in range(26)]
        with open(text, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    self.top_side.extend(row)
                elif i == 1:
                    self.right_side.extend(row)
                elif i == 2:
                    self.bottom_side.extend(row)
                elif i == 3:
                    self.left_side.extend(row)
        excluded_letters = self.top_side + self.right_side + self.bottom_side + self.left_side
        self.remaining_alphabet = [letter for letter in alphabet if letter not in excluded_letters]
        print("Top side:", puzzle.top_side)
        print("Right side:", puzzle.right_side)
        print("Bottom side:", puzzle.bottom_side)
        print("Left side:", puzzle.left_side)

    def create_word_list(self, filename):
        self.word_list = []
        with open(filename, 'r') as file:
            for line in file:
                # Assuming each line contains a single word
                self.word_list.append(line.strip())  # Remove trailing newline characters
        return self.word_list

    def print_puzzle(self):
        print(f"   {self.top_side[0]}  {self.top_side[1]}  {self.top_side[2]}")
        print(" +-o--o--o-+")
        print(f"{self.left_side[0]}|         |{self.right_side[0]}")
        print(f"{self.left_side[1]}|         |{self.right_side[1]}")
        print(f"{self.left_side[2]}|         |{self.right_side[2]}")
        print(" +-o--o--o-+")
        print(f"   {self.bottom_side[0]}  {self.bottom_side[1]}  {self.bottom_side[2]}")

    def make_move(self):
        valid_letters = []
        inp = str(input("Enter a valid word: "))
        if inp[0] == self.starting_letter or self.starting_letter is None:
            self.starting_letter = self.letters[-1]

    def make_word_list(self, word_list):
        alphabet = [string.ascii_lowercase[i] for i in range(26)]
        alphabet_dict = {letter: [] for letter in alphabet}
        for word in word_list:
            alphabet_dict[word[0]].append(word)
        return alphabet_dict

    def make_word_pairs(self, word_list, alpha_list, letters_set):
        for word_1 in word_list:
            for word_2 in alpha_list[word_1[-1:]]:
                if (set(letters_set)).issubset(set(word_1 + word_2)):
                    print(word_1, word_2)
    def solve(self):
        self.create_word_list('valid_words.txt')
        print(len(self.word_list))
        print(self.remaining_alphabet)
        self.word_list = [word for word in self.word_list if
                          not any(letter in self.remaining_alphabet for letter in word)]
        print(len(self.word_list))
        self.word_list = remove_words_with_consecutive_letters(self.word_list, self.top_side)
        self.word_list = remove_words_with_consecutive_letters(self.word_list, self.right_side)
        self.word_list = remove_words_with_consecutive_letters(self.word_list, self.bottom_side)
        self.word_list = remove_words_with_consecutive_letters(self.word_list, self.left_side)
        print(len(self.word_list))
        export_list_to_text_file(self.word_list, 'valid_for_puzzle.txt')
        letters = self.top_side + self.right_side + self.bottom_side + self.left_side
        print(letters)
        letters_set = set(letters)
        alpha_list = self.make_word_list(self.word_list)
        self.make_word_pairs(self.word_list, alpha_list, letters_set)

puzzle = Puzzle()
puzzleIsGenerated = False

while True:
    print("1. Generate a puzzle")
    print("2. Print a puzzle")
    print("3. Read in a puzzle")
    print("4. Solve the puzzle")
    inp = flexible_input("Enter your choice:")
    if inp == 1:
        puzzle.generate_letters()
        puzzleIsGenerated = True
    elif inp == 2:
        if puzzleIsGenerated is False:
            print("Generate a puzzle first")
        else:
            puzzle.print_puzzle()
    elif inp == 3:
        puzzleIsGenerated = True
        puzzle.read_puzzle("puzzle.csv")
    elif inp == 4:
        if puzzleIsGenerated is False:
            print("Generate a puzzle first")
        puzzle.solve()
