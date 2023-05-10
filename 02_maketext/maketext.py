def isword(word):
# check if the word is in american-english
    with open ('02_maketext/american-english') as f:
        for line in f:
            if word == line.strip():
                return True
    return False

print(isword('hello'))

