from ask.models import Question, Answer
from feedback.models import Feedback
from appointment.models import Appointment, Clinic, Patient
from django.contrib.auth.models import User
import random
import datetime
from django.db.utils import IntegrityError



user1 = User.objects.create_user(username='roman', first_name='Роман', last_name='Шелемех', password='5rdFT^7yg',
                                 email='shelemekh@tut.by', is_superuser=True, is_staff=True)
user2 = User.objects.create_user(username='kate', first_name='Катя', password='5rdFT^7yg', email='kate@tut.by')
user3 = User.objects.create_user(username='croissant', first_name='Крус', password='5rdFT^7yg', email='croissant@tut.by')

for i in range(1, 60, 3):
    Question.objects.create(
        title=f'Это вопрос № {i} от Романа',
        text=f'Python — высокоуровневый язык программирования общего назначения с динамической строгой типизацией и '
             f'автоматическим управлением памятью, ориентированный на повышение производительности разработчика, '
             f'читаемости кода и его качества, а также на обеспечение переносимости написанных на нём программ. ',
        author=user1
    )
    Question.objects.create(
        title=f'Это вопрос № {i+1} от Кати',
        text=f'Ортодонтия (греч. ορθός «прямой; правильный» + οδόντι «зуб») — раздел стоматологии, занимающийся '
             f'изучением этиологии, диагностики, методов профилактики и лечения зубо-челюстных аномалий. '
             f'Преимущественным объектом вмешательств в ортодонтии является жевательно-речевой аппарат детей и '
             f'подростков.',
        author=user2
    )
    Question.objects.create(
        title=f'Это вопрос № {i + 2} от Круса',
        text="""
Французский бульдог (фр. bouledogue français) — порода собак. Некрупная, отличающаяся крупной, но короткой 
мордой, плоским раздвоенным носом, широкой раздвоенной верхней губой. Стоячие уши, широкие у основания и 
закругляющиеся сверху. Выступающие надбровные дуги отделены друг от друга глубокой бороздкой между глазами. 
Бороздка не должна продолжаться на лбу, как у английских бульдогов. Затылочный бугор слабо развит. Могут 
иметь самый разнообразный окрас: тигровый, бело-тигровый, палевый, бело-палевый.
        """,
        author=user3
    )


for i in range(1, 60, 5):
    question = Question.objects.get(id=i)
    for i in range(random.randint(1, 5)):
        question.answer_set.create(text=f'Тестовый комментарий № {i+1} к вопросу {question.title}',
                                   author=random.choice([user1, user2, user3]))

for i in range(100):
    random.choice(Question.objects.all()).like.add(random.choice([user1, user2, user3]))


Feedback.objects.create(name='Роман', email='shelemekh@tut.by', is_published=True,
                        comment='Екатерина Сергеевна - очень внимательный и чуткий специалист, я бы даже сказал, что '
                                'она - не только стоматолог, а ещё и квалифицированный психолог, потому что её подходы '
                                'к людям не только успокаивают перед непростым стоматологическим лечением, но и '
                                'вселяют уверенность в то, что всё будет безболезненно, и поводов для беспокойства '
                                'нет! Спасибо вам, Екатерина Сергеевна!')
Feedback.objects.create(name='Крус', email='croissant@tut.by', is_published=True,
                        comment='Обратилась в стоматологию "Имплант" за консультацией по прикусу. Меня записали к '
                                'Екатерине Сергеевне. Это самый лучший ортодонт на свете. Уже полгода прохожу лечение '
                                'с брекетами "Даймон". Не могу нарадоваться, с каждым приемом все лучше и лучше '
                                'результат. Екатерина Сергеевна всегда улыбается и все все рассказывает, показывает '
                                'мои фото для сравнения, дает разъяснения по каждому зубу. Еще я удаляла в этой '
                                'клинике все зубы мудрости - это было быстро и безболезненно. Хороших и благодарных '
                                'клиентов!')
Feedback.objects.create(name='Катя', email='kate@tut.by', is_published=True,
                        comment='Я поставила брекет-систему у Екатерины Сергеевны и очень счастлива, что попала '
                                'именно к ней. Я долго выбирала доктора. В имплант клинику пришла удалять зубы '
                                'мудрости, хирург пригласил ортодонта на совместную консультацию перед удалением. '
                                'В итоге я третий месяц нахожусь на ортодонтическом лечении, чему безмерно рада.')
Feedback.objects.create(name='Константин', email='kostya@tut.by', is_published=True,
                        comment='Очень квалифицированный, внимательный и вежливый врач. Прохожу ортодонтическое '
                                'лечение у Екатерины Сергеевны уже полгода. Рассказала мне о некоторых решениях '
                                'моих стоматологических проблем, о которых не говорили другие.')

Clinic.objects.create(name='ДЕНТиК на Тургенева', address='ул. Тургенева, 23')
Clinic.objects.create(name='Имплант на 40 лет победы', address='ул. 40 лет победы, 178/1')
Clinic.objects.create(name='Имплант на Ставропольской', address='ул. Ставропольская, 135')

Patient.objects.create(name='Роман', email='shelemekh@tut.by', phone_number='+375295264')



def random_date():
    from django.utils import timezone
    import datetime
    import random
    start_date = timezone.now().date()
    end_date = timezone.now().date() + datetime.timedelta(days=60)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)



for i in range(30):
    try:
        time = [datetime.time(9, 30), datetime.time(10, 00), datetime.time(10, 30),
                datetime.time(11, 00), datetime.time(12, 00)]
        date = random_date()
        for i in range(random.randint(1,5)):
            day_time = time[:]
            Appointment.objects.create(clinic=random.choice(Clinic.objects.all()),
                                      date=date,
                                      time=day_time.pop(random.randrange(len(day_time))))
    except IntegrityError:
        pass





