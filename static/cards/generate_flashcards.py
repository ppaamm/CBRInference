import csv
import random


filename = "cards.csv"

cards = []

with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        cards.append(row)
random.shuffle(cards)

for i in range(len(cards)):
    card = cards[i]
    text1 = "\\begin{flashcard}{ "
    text2 = " \quad $\longrightarrow$ \quad "
    text3 = " }"
    text4 = "\end{flashcard}"
    
    print(text1 + card[0] + text2 + card[1] + text3 + str(i+1) + text4)
