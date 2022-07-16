from WordGenerator import WordGenerator

if __name__ == "__main__":

    wg = WordGenerator("data/pride_and_prejudice.txt")

    print(wg.generate_words(N=20))