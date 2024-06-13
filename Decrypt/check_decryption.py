import subprocess
try:
    import enchant
except ModuleNotFoundError:
    subprocess.check_call(['pip', 'install', 'pyenchant'])
    import enchant

try:
    import nltk
except ModuleNotFoundError:
    subprocess.check_call(['pip', 'install', 'nltk'])
    import nltk


class WordChecker:
    def __init__(self) -> None:
        self.dictionary = enchant.Dict("en_US")

    def tokenize(self, text):
        return nltk.word_tokenize(text, language='english', preserve_line=False)
    
    def count_correct_words(self, tokens):
        count = 0
        for token in tokens:
            valid_token = self.dictionary.check(token)
            if valid_token:
                count += 1
        return count

word_checker = WordChecker()
tokens = word_checker.tokenize("Peter Piper picked a peck of pickled peppers. A peck of pickled peppers Peter Piper picked. If Peter Piper picked a peck of pickled peppers, Where's the peck of pickled peppers Peter Piper picked?")
correct_words = word_checker.count_correct_words(tokens)
print("The ratio of english words to total words is: " + str(correct_words / len(tokens)))
