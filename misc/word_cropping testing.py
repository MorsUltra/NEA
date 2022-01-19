def word_cropper(string, seperator=" ", word_count=1):
    count = 0
    for i, char in enumerate(string):
        if char == seperator:
            count += 1
            if count == word_count:
                return i
    return

s = "thisisatest"
print(s[:word_cropper(s, word_count=2)])
