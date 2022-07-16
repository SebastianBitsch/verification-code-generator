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
        

    def __clean_text(self, raw_text:str) -> str:
        """
        Given a text this functions cleans it, removing all non alphabet characters and converting to lowercase
        
        Parameters
        ----------
            raw_text: str
                the text to be cleaned
        """
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
        """ 
        Given a text this function splits the text into words and generates a dictionary of all unique 
        3-letter chunks of letters with the key being the chunk and the count the value.
        Note that all two letter words are removed.

        Parameters
        ----------
            text: str,
                the text from where to generate the chunks
        """
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


    def generate_words(self, length:int = 6, N:int = 1) -> list[str]:
        """ 
        A function for generating and returning N words of a given length 

        Parameters
        ----------
            length: int, optional
                the length of the word to be generated

            N: int, optional
                the number of words to generate
        """
        return [self.generate_word(length=length) for _ in range(N)]


    def generate_word(self, length:int = 6) -> str:
        """ 
        This function generates and returns a random word of a given length.

        Parameters
        ----------
            length: int, optional
                the length of the word to be generated
        """
        chunks = list(self.chunk_dict.keys())
        
        # Get random starting word from the chunks
        index = randint(0, len(chunks))
        start = chunks[index]
        word = start

        while len(word) < length:
            tail = word[-2:]

            # Look for words where the last two letters of the current word matches the two first in a given word            
            potential_words = [x for x in chunks if tail == x[:2]]
            probabilities = [self.chunk_dict[x] for x in potential_words]

            # Chose the word to append weighted by the number of times it occurs in the text
            chosen_word = choices(population=potential_words, weights=probabilities, k=1)[0]
            word += chosen_word[-1]

        return word.capitalize()