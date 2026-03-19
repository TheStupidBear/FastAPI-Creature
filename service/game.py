import data.game as data
from collections import Counter, defaultdict
HIT = "H"
MISS = "M"
CLOSE = "C" # (буква находится в слове, но в другой позиции)

def get_score(actual: str, guess: str) -> str:
    length: int = len(actual)
    if len(guess) != length:
        return "ERROR"
    actual_counter = Counter(actual)  # {буква: подсчет, ...}
    guess_counter = defaultdict(int)
    result = [MISS] * length
    for pos, letter in enumerate(guess):
        if letter == actual[pos]:
            result[pos] = HIT
            guess_counter[letter] += 1
    for pos, letter in enumerate(guess):
        if result[pos] == HIT:
            continue
        guess_counter[letter] += 1
        if (letter in actual and
            guess_counter[letter] <= actual_counter[letter]):
            result[pos] = CLOSE
    result = ''.join(result)
    return result

def get_word() -> str:
    return data.get_word()