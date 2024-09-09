import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP P NP | NP VP Conj S | NP VP Conj S | VP | NP VP P NP Conj S | VP P NP | NP VP P NP P NP
NP -> N | Det NP | Det NP P NP | Det P NP | P Det Adj NP | P Adj NP | Det Adj NP | P Det Adj NP Adv | Det NP Adv | Adj Adj NP
VP -> V | V NP | Adv V | V Adv | Adv V NP | V Adv NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words_old = nltk.tokenize.word_tokenize(sentence)
    words_new = []
    for num in range(len(words_old)):
        if words_old[num].isalpha():
            words_new.append(words_old[num])
    for num in range(len(words_new)):
        words_new[num] = words_new[num].lower()

    return words_new


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    output = []

    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            # Check if the subtree itself contains any 'NP' subtrees
            contains_np = False
            for subsubtree in subtree:
                if subsubtree.label() == 'NP':
                    contains_np = True
                    break
                for subb in subsubtree.subtrees():
                    if subb.label() == 'NP':
                        contains_np = True
                        break
            if not contains_np:
                output.append(subtree)

    return output


if __name__ == "__main__":
    main()
