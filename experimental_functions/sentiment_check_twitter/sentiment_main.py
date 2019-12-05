import sentiment_mod as s
import nltk
from nltk.tokenize import sent_tokenize
text = '''
I love going down to the farmers' market. I love really being able to interact with the farmers and i love going down and just being able to see everyone there.
'''

tokenized_text = sent_tokenize(text)
for sent in tokenized_text:
    print(sent)
    print(s.sentiment(sent))

print(s.sentiment('I dislike that all of those options are there.'))
