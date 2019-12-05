import sentiment_mod as s
import nltk
from nltk.tokenize import sent_tokenize
text = '''
That is a broad question. Obviously I do like the sense of community I get when I go down to some of the community events, especially ones at the market house. I love going down to the farmers' market. I love really being able to interact with the farmers and i love going down and just being able to see everyone there. It is a little bit of a social scene. Also, I do like that it's small and if I do go into any of the coffee shops, I will run onto someone I know. I would say that if there's an event, it's nice that it's a small enough community that you can read about it in the paper and you can usually go to it and see people there. So I guess i would say that I like that there are things to do but when you do them you're always running into people you know. I like the small community feel, I like that there's still a lot of really great events you can go to. Especially things like the plays at Allegheny. I love what the college brings into the town. I love the culture that gets brought in with that. And I'm really excited to see some of the stuff at the Academy Theater. I haven't really been there so thats a place I need to get to. For a small town, Ive lived here for almost five years now, theres still a lot of places i haven't been. I do like that all of those options are there. And with the MCA, I like when they offer shows and stuff there. And i think the market house is a real asset to this community. The market house has a gathering space both for the farmers market, the second saturdays, but also the cooking classes. Oh man, that reminds me I was gonna go to a cooking class yesterday and I totally forgot.
'''

tokenized_text = sent_tokenize(text)
for sent in tokenized_text:
    print(sent)
    print(s.sentiment(sent))

print(s.sentiment('I dont like that all of those options are there.'))
