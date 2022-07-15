from WordGenerator import WordGenerator

if __name__ == "__main__":
    wg = WordGenerator("data/moby_dick.txt")
    for _ in range(10):
        print(wg.generate_word())