"""
Zaloma es una palabra de 6 letras que tiene la propiedad de que si se le
quitan las dos primeras letras y se las ponen al final, se obtiene otra
palabra de 6 letras, y además, si se le quitan las cuatro primeras letras
y se las ponen al final, se obtiene otra palabra de 6 letras.

Zaloma is a word of 6 letters that has the property that if you remove the
first two letters and put them at the end, you get another word of 6 letters,
and also, if you remove the first four letters and put them at the end, you
get another word of 6 letters.
"""

from pathlib import Path

file_path = Path("misc/0_palabras_todas.txt")

with open(file_path, "r", encoding="utf8") as f:
    words = f.read().splitlines()

words_len_6 = [word for word in words if len(word) == 6]

# Zaloma 1
print("Zaloma 1")

for word in words_len_6:
    word_shift_2 = word[2:] + word[:2]
    word_shift_4 = word[4:] + word[:4]
    if word_shift_2 in words_len_6 and word_shift_4 in words_len_6:
        print(word, word_shift_2, word_shift_4)

# Zaloma 2
print("Zaloma 2")

for i, word_1 in enumerate(words_len_6):
    for j, word_2 in enumerate(words_len_6[i:], i):
        for word_3 in words_len_6[j:]:
            if (
                word_1[2:4] == word_2[:2]
                and word_1[4:] == word_3[:2]
                and word_2[4:] == word_3[2:4]
            ):
                print(word_1, word_2, word_3)
