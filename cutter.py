def cutter(path):
    with open(path, "r") as file:
        lst_words = []
        for word in file:
            lst_words.append(word.strip())
    with open('test.txt', "w") as file_w:
        for word in lst_words:
            if lst_words.index(word) % 20 == 0:
                file_w.write(word)
                print(word)
                file_w.write("\n")
cutter("words.txt")