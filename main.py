from WordGenerator import WordGenerator

if __name__ == "__main__":

    # Read sample txt file 
    wg = WordGenerator("data/moby_dick.txt", seed=10)

    print(wg.generate_words(length=4,N=17*2))