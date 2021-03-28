

from ask.models import Question, Tag, Answer

for i in range(30):
    q = Question(text=f'I am telling you the {i+1}th time that I am a good programmer', title=f'Question example #{i+1}')
    q.save()