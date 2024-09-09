from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0 = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(Not(sentence0), AKnave),
    Implication(sentence0, AKnight)
)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence1_A = And(AKnave, BKnave)

knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(Not(sentence1_A), AKnave),
    Implication(sentence1_A, AKnight),


)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentence2_A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
sentence2_B = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(Not(sentence2_A), AKnave),
    Implication(sentence2_A, AKnight),
    Implication(Not(sentence2_B), BKnave),
    Implication(sentence2_B, BKnight)

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight.
sentence3_A = Or(AKnight, AKnave)
sentence3_B = And(Implication(sentence3_A, BKnave), CKnave)
sentence3_C = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Implication(Not(sentence3_A), AKnave),
    Implication(sentence3_A, AKnight),
    Implication(Not(sentence3_B), BKnave),
    Implication(sentence3_B, BKnight),
    Implication(Not(sentence3_C), CKnave),
    Implication(sentence3_C, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
