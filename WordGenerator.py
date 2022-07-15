from random import choices, randint
from string import ascii_letters

def read_txt(path:str, newline:str='\n') -> str:
    f = open(path, "r", newline=newline)
    lines  = f.read().splitlines()
    return " ".join(lines)


class WordGenerator:

    def __init__(self, path:str) -> None:
        
        self.path = path
        self.raw_text = read_txt(path)
        self.clean_text = self.__clean_text(self.raw_text)
        self.chunk_dict = self.__generate_chunks(self.clean_text)
        

    def __clean_text(self, raw_text:str) -> None:
        # Legal characters include the alphabet, spaces and hyphos
        legal_chars = ascii_letters+ " " + "-" + "—" # apparently there are two different types of - idk

        # Get a list of all characters in the text
        all_chars = list(set(raw_text))

        # Generate a list of illegal charactes from the legal ones
        illegal_chars = [x for x in all_chars if x not in legal_chars]
        illegal_chars = "".join(illegal_chars)

        # Remove illegal chars and replace hyphons
        raw_text = raw_text.translate({ord(x): "" for x in illegal_chars})
        raw_text = raw_text.replace("-", " ")
        raw_text = raw_text.replace("—", " ")

        return raw_text.lower()


    def __generate_chunks(self, text:str) -> dict:
        # Remove two-letter words
        all_words = text.split()
        all_words = [x for x in all_words if 2 < len(x)]

        # Create the counts of every chunk
        chunk_dict = {}

        for word in all_words:
            for i in range(3, len(word) + 1):
                chunk = word[i-3 : i]
                count = chunk_dict.get(chunk,0)
                chunk_dict[chunk] = count + 1
        
        return chunk_dict

    def generate_word(self, N:int = 6) -> str:
        # Generate a word
        chunks = list(self.chunk_dict.keys())
        
        index = randint(0, len(chunks))
        start = chunks[index]
        word = start

        while len(word) < N:
            tail = word[-2:]
            
            potential_words = [x for x in chunks if tail == x[:2]]
            probabilities = [self.chunk_dict[x] for x in potential_words]

            chosen_word = choices(population=potential_words, weights=probabilities, k=1)[0]
            word += chosen_word[-1]

        return word