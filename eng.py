#coding: utf-8

import random
import re
import unittest
import argparse
import sys

class Question:
    def __init__(self, english, japanese):
        self.en = parse_english(english) # double dimention array
        self.jp = japanese # str

    def ask(self, level):
        moth = {} # moth = ___
        GREEN = "\033[92m"
        RED = "\033[91m"
        END = "\033[0m"
        word_matcher = re.compile("\S+") # match to word

        for v in random.sample(self.en, min(level, len(self.en))):
            # some are turned to moth
            if v:
                moth[self.en.index(v)] = v

        # print problem
        print(self.jp) # japanese
        for i, w in enumerate(self.en):
            # english
            if i in moth:
                print("_" * len(moth[i][0]), end=" ")
            else:
                print(w[0], end = " ")

        print()

        answers = word_matcher.findall(input()) # split to words
        corrects = 0

        for i, ans in enumerate(answers):
            if len(self.en[i]) > i:
                correct = ans in self.en[i] # are candidates include answer?
            else:
                correct = False

            if correct:
                corrects += 1
                print(GREEN + "O" + END, end="")
            else:
                allcorrect = False
                print(RED + "X" + END, end="")
            print("{} {}".format(self.en[i], ans))

        if len(answers) < len(self.en):
            for v in self.en[len(answers):]:
                print(RED + "X" + END,end="")
                print(v)

        if corrects == len(self.en):
            print(GREEN + "Correct!" + END)
        else:
            print(RED + "Wrong..." + END)



def parse_paren(text):
    words = []
    wbuf = str()
    for i, c in enumerate(text):
        if c == '|':
            words.append(wbuf)
            wbuf = str()
        elif c == ')':
            words.append(wbuf)
            return (i, words)
        else:
            wbuf += c

def parse_english(sentence):
    elements = []
    word = []
    wbuf = str()
    i = 0
    sentence += " " # sentinel
    while i < len(sentence):
        c = sentence[i]
        if c.isspace():
            if wbuf:
                word.append(wbuf)
            elements.append(word)
            wbuf = str()
            word = []
        elif c == '(':
            i += 1 # read '('
            index, choices = parse_paren(sentence[i:])
            i += index
            word = word + choices
        else:
            wbuf += c
        i += 1
    return elements[:-1]



def Questions(filename):
    questions = []
    en = ""
    jps = []
    with open(filename, encoding="utf-8") as f:
        for l in f:
            if not l.strip():
                for jp in jps:
                    questions.append(Question(en, jp))
                en = ""
                del jps[:]
            else:
                if not en:
                    en = l
                else:
                    jps.append(l)
    return questions

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level", type=int, default=random.randint(0, sys.maxsize), help="The mothes increase with level. Default is random (almost cases level max")
    parser.add_argument("-f", "--file", default="problems.txt", help="Set problem files path")
    args = parser.parse_args()

    qs = Questions(args.file)
    random.shuffle(qs)
    for q in qs:
        q.ask(args.level)
        print("Continue to press RETURN")
        cont = input()
        if cont is not "":
            break

class Test_parse_english(unittest.TestCase):
    def setUp(self):
        self.sentences = ["What is your name?", "I (don't|do not) like it.","I think (that|) I am right."]

    def test_parse_english(self):
        self.assertEqual(parse_english(self.sentences[0]), [["What"], ["is"], ["your"], ["name?"]])
        self.assertEqual(parse_english(self.sentences[1]), [["I"], ["don't", "do not"], ["like"], ["it."]])
        self.assertEqual(parse_english(self.sentences[2]), [["I"], ["think"], ["that", ""], ["I"], ["am"], ["right."]])
