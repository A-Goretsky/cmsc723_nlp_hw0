# Author: YOUR NAME HERE
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from curses.ascii import isdigit
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize
class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        self._apostrophe_handler = False

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        try:
            x = min([[len([y for y in x if y[-1].isdigit()])] for x in self._pronunciations[word]])
            return x[0]
        except:
            return 1

    # Returns index of first consonant, -1 is all vowels
    def find_first_cons(self, pron):
        for index, entry in enumerate(pron):
            if not entry[-1].isdigit():
                return index
        return -1

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
       
        a = a.lower()
        a = ''.join(x for x in a if x.isalpha() or x == "'")
        b = b.lower()
        b = ''.join(x for x in b if x.isalpha() or x == "'")

        try:
            phonemes_a = self._pronunciations[a]
            phonemes_b = self._pronunciations[b]
        except:
            return False

        no_vowels_a = True
        for x in phonemes_a[0]:
            if x[-1].isdigit():
                no_vowels_a = False
        no_vowels_b = True
        for x in phonemes_b[0]:
            if x[-1].isdigit():
                no_vowels_b = False
        
        if no_vowels_a or no_vowels_b:
            return False

        for pron_a in phonemes_a:
            for pron_b in phonemes_b:
                rhyme_bool = True
                len_a = len(pron_a)
                len_b = len(pron_b)

                max_ind = -1
                first_cons = -1
                if len_a < len_b:
                    max_ind = len_a - 1
                    first_cons = self.find_first_cons(pron_a)
                else:
                    max_ind = len_b - 1
                    first_cons = self.find_first_cons(pron_b)

                counter = 0
                while max_ind != first_cons:
                    
                    ind_a = len_a - counter - 1
                    ind_b = len_b - counter - 1

                    # If phoneme is same, continue
                    if pron_b[ind_b] == pron_a[ind_a]:
                        max_ind -= 1
                        counter += 1
                        continue
                    else:
                        rhyme_bool = False
                        break

                if rhyme_bool == True:
                    return rhyme_bool

        return False

    def apostrophe_tokenize(self, line):
        line = line.split(' ')
        output = []
        for token in line:
            token = token.lower()
            token = ''.join(x for x in token if x.isalpha() or x == "'")
            output.append(token)
        self._apostrophe_handler = True
        return output

    def is_limerick(self, text):

        # NO TRANSITIVE PROPERTY FOR RHYMING IF A = B, B DOES NOT NECESSARILY = C (Diff pronounce)

        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other (and not the A
        lines).

        (English professors may disagree with this definition, but that's what
        we're using here.)
        """
        lines = text.strip().split('\n')
        all_words = []
#
        if len(lines) != 5:
            return False
        #
        for line in lines:
            tokens = word_tokenize(line)
            #tokens = self.apostrophe_tokenize(line)
            if not self._apostrophe_handler:
                while not tokens[-1].isalpha():
                    tokens.pop()
            else:
                while not any(char.isalpha() for char in tokens[-1]):
                    tokens.pop()
            all_words.append(tokens)

        return (self.rhymes(all_words[0][-1], all_words[1][-1]) 
                and self.rhymes(all_words[0][-1], all_words[4][-1])
                and self.rhymes(all_words[1][-1], all_words[4][-1])
                and self.rhymes(all_words[2][-1], all_words[3][-1])
                and not self.rhymes(all_words[0][-1], all_words[2][-1]))

if __name__ == "__main__":
    #buffer = ""
    #inline = " "
    #while inline != "":
    #    buffer += "%s\n" % inline
    #    inline = input()
#
    ld = LimerickDetector()

    e = """An exceedingly fat friend of mine,
When asked at what hour he'd dine,
Replied, "At eleven,
At three, five, and seven,
And eight and a quarter past nine"""

    #print(ld.rhymes("cant", "pant"))
    #print(ld.rhymes("can't", "pant"))
    #print(ld.rhymes("don't", "wont"))
    #ld.is_limerick(e)
    #print(ld.first_cons(['ER0']))
    #print(ld.rhymes('dog', 'bog'))
    #print(ld.rhymes("failure", "savior"))
    #print(ld.rhymes("test", "rest"))
    #print(ld.rhymes("seven", "eleven"))
    #print(ld.rhymes("granite", "pit"))
    #print(ld.rhymes("apportion", "abortion"))
    #print(ld._pronunciations["cant"])
    #ld.num_syllables("debris")
    #print("%s\n-----------\n%s" % (buffer.strip(), ld.is_limerick(buffer)))
