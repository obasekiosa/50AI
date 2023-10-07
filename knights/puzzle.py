from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

def exclusive_or(a, b):
    return Or(And(a, Not(b)), And(Not(a), b))

def maybe_statement(sayer, nay_sayer, statement):
    return Or(And(sayer, statement), And(nay_sayer, Not(statement)))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    exclusive_or(AKnight, AKnave),
    maybe_statement(AKnight, AKnave, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    exclusive_or(AKnight, AKnave),
    exclusive_or(BKnight, BKnave),
    maybe_statement(AKnight, AKnave, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    exclusive_or(AKnight, AKnave),
    exclusive_or(BKnight, BKnave),
    maybe_statement(AKnight, AKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    maybe_statement(BKnight, BKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    exclusive_or(AKnight, AKnave),
    exclusive_or(BKnight, BKnave),
    exclusive_or(CKnight, CKnave),
    maybe_statement(AKnight, AKnave, Or(AKnight, AKnave)),
    BKnave,
    maybe_statement(BKnight, BKnave, CKnave),
    maybe_statement(CKnight, CKnave, AKnight)
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
