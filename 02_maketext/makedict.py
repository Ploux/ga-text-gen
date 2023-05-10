# return a text file with the words sorted by length

with open('20k.txt', 'r') as infile:
    words = infile.read().splitlines()
    
words.sort(key=len)

with open('words_sorted.txt', 'w') as outfile:
    for word in words:
        outfile.write(word + '\n')
        
print('Done')

    