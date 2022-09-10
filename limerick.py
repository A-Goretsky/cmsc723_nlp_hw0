# Author: YOUR NAME HERE
# Date: DATE SUBMITTED

# Use word_tokenize to split raw text into words
from curses.ascii import isdigit
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

# TODO: Consider reducing punctuation effectivity in rhyme in regards to apostrophe (or keep it? depends on tokenizer)

class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        #pron = self._pronunciations[word]
        try:
            #orig = self._pronunciations[word]
            #print(orig)
            #[['B', 'AA1', 'G'], ['B', 'AO1', 'A03', 'G']]
            #x = min([[len([y for y in x if y[-1].isdigit()])] for x in [['B', 'AA1', 'G'], ['B', 'AO1', 'A03', 'G']]])
            x = min([[len([y for y in x if y[-1].isdigit()])] for x in self._pronunciations[word]])
            #print(x)
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

        CHECK ALL PRONOUNCIATIONS
        """
        # NUMBERS IN VOWEL PRONOUNCE DONT CHANGE PRONOUNCE
        # CASE IF WORD NOT IN DICTIONARY (CHECK IF LEN OF SHORTEST IS 0)
        # After getting max ind, just find first consonant in shortest word, sub its index from len, make that max iterations
        a = a.lower()
        a = ''.join(x for x in a if x.isalpha())
        b = b.lower()
        b = ''.join(x for x in b if x.isalpha())
        #print(a)
        #print(b)
        try:
            phonemes_a = self._pronunciations[a]
            phonemes_b = self._pronunciations[b]
        except:
            return False

        #print(phonemes_a)
        #print(phonemes_b)

        #final_bools = []

        #rhyme_bool = True
        for pron_a in phonemes_a:
            for pron_b in phonemes_b:
                rhyme_bool = True
                len_a = len(pron_a)
                len_b = len(pron_b)
                #print(pron_a)
                #print(pron_b)
                #print(len_a)
                #print(len_b)
                max_ind = -1
                first_cons = -1
                if len_a < len_b:
                    max_ind = len_a - 1
                    first_cons = self.find_first_cons(pron_a)
                else:
                    max_ind = len_b - 1
                    first_cons = self.find_first_cons(pron_b)
                #print("Max Ind: " + str(max_ind))

                #len - max_ind
                #5 - 4 = 1 - 1   len - 0 - 1
                #6 - 4 = 2 - 1   len - 1 - 1
                #len - (len - max_ind - 1) - 1
                counter = 0
                while max_ind != first_cons:
                    
                    #pron_a_phon = pron_b[::-1]
                    
                    ind_a = len_a - counter - 1
                    ind_b = len_b - counter - 1
                    #print(ind_a)
                    #print(ind_b)
                    #print("CHECKING")
                    #print(pron_a[ind_a])
                    #print(pron_b[ind_b])
                    #print("STRIPPED")
                    #print(pron_a[ind_a].rstrip('012'))
                    #print(pron_b[ind_b].rstrip('012'))

                    # THIS LINE IS AN ISSUE, STRIPPED VOWEL MAY BE SAME AS CONS REPRESENTATION

                    # If phoneme is same, continue
                    if pron_b[ind_b] == pron_a[ind_a]:
                        max_ind -= 1
                        counter += 1
                        #print("continued")
                        continue
                    else:
                        rhyme_bool = False
                        break

                    #else:
                    ##print("in else")
                    #    if not (not pron_a[ind_a][-1].isdigit() and not pron_b[ind_b][-1].isdigit()):
                    ##print("in if")
                    #        rhyme_bool = False
                    #    else:
                    #        if counter == 0:
                    #            rhyme_bool = False
                    #        else:
                    #            rhyme_bool = True
                    #    break

                #final_bools.append(rhyme_bool)
                #print(rhyme_bool)
                if rhyme_bool == True:
                    return rhyme_bool

        return False


        ## FIX LATER ONLY WORKS FOR ONE PRONUNCIATION
        # REPEAT PROCESS BELOW FOR ALL POSSIBLE COMBINATIONS OF PRONUNCIATIONS OF BOTH WORDS
        # IF ANY ARE TRUE IT IS TRUE
        
        # Same sounds in their pronounciation except their initial consonant
        # If one word is longer, sounds of shorter should be suffix of sounds of longer
        # Handle punctuation
        # End rhymes are rhymes



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
        print(lines)
        all_words = []
#
        if len(lines) != 5:
            return False
        #
        for line in lines:
            tokens = word_tokenize(line)
            while not tokens[-1].isalpha():
                tokens.pop()
            all_words.append(tokens)
#
        print(all_words)
#
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

    ld.is_limerick(e)
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
