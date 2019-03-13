import re
import random


def try_to_replace(match_results, answer):
    search = re.search(r'\$([\d]+)', answer)
    if search is not None:
        idx = int(search.group(1))
        replacement = match_results.group(idx)
        return str.replace(answer, ''.join(['$', search.group(1)]), replacement)
    else:
        return answer


class ChatBot:
    __model = {
        r".*hello .*": [
            "How do you do. Please state your problem."
        ],
        r"(.*)? computer(.*)?": [
            "Do computers worry you?",
            "What do you think about machines?",
            "Why do you mention computers?",
            "What do you think machines have to do with your problem?",
        ],
        r"(.*)? name(.*)?": [
            "I am not interested in names",
        ],
        r"(.*)?sorry(.*)?": [
            "Please don't apologize",
            "Apologies are not necessary",
            "What feelings do you have when you apologize",
        ],
        r"(.*)?I remember (.*)?": [
            "Do you often think of $2?",
            "Does thinking of $2 bring anything else to mind?",
            "What else do you remember?",
            "Why do you recall $2 right now?",
            "What in the present situation reminds you of $2?",
            "What is the connection between me and $2?",
        ],
        r"(.*)?do you remember (.*)?": [
            "Did you think I would forget $2?",
            "Why do you think I should recall $2 now?",
            "What about $2?",
            "You mentioned $2",
        ],
        r"(.*)?I want (.*)?": [
            "What would it mean if you got $2?",
            "Why do you want $2?",
            "Suppose you got $2 soon."
        ],
        r"(.*)?if (.*)?": [
            "Do you really think it's likely that $2?",
            "Do you wish that $2?",
            "What do you think about $2?",
            "Really--if $2?"
        ],
        r"(.*)?I dreamt (.*)?": [
            "How do you feel about $2 in reality?",
        ],
        r"(.*)? dream (.*)?": [
            "What does this dream suggest to you?",
            "Do you dream often?",
            "What persons appear in your dreams?",
            "Don't you believe that dream has to do with your problem?",
        ],
        r"(.*)?my mother (.*)?": [
            "Who else in your family $2?",
            "Tell me more about your family",
        ],
        r"(.*)?my father (.*)?": [
            "Your father?",
            "Does he influence you strongly?",
            "What else comes to mind when you think of your father?",
        ],
        r"(.*)?I am glad(.*)?": [
            "How have I helped you to be $2?",
            "What makes you happy just now?",
            "Can you explain why you are suddenly $2?",
        ],
        r"(.*)?I am sad(.*)?": [
            "I am sorry to hear you are depressed",
            "I'm sure it's not pleasant to be sad",
        ],
        r"(.*)? is like (.*)?": [
            "What resemblence do you see?",
            "Could there really be some connection?",
            "How?",
        ],
        r"(.*)? alike (.*)?": [
            "In what way?",
            "What similarities are there?",
        ],
        r"(.*)? same (.*)?": [
            "What other connections do you see?",
        ],
        r"(.*)?no(.*)?": [
            "Why not?",
            "You are being a bit negative.",
            "Are you saying 'No' just to be negative?"
        ],
        r"(.*)?I was (.*)?": [
            "Were you really?",
            "Perhaps I already knew you were $2.",
            "Why do you tell me you were $2 now?"
        ],
        r"(.*)? was I (.*)?": [
            "What if you were $2?",
            "Do you think you were $2?",
            "What would it mean if you were $2?",
        ],
        r"(.*)?I am (.*)?": [
            "In what way are you $2?",
            "Do you want to be $2?",
        ],
        r"(.*)?am I (.*)?": [
            "Do you believe you are $2?",
            "Would you want to be $2?",
            "You wish I would tell you you are $2?",
            "What would it mean if you were $2?",
        ],
        r"(.*)? am (.*)?": [
            "Why do you say 'AM?'",
            "I don't understand that"
        ],
        r"(.*)?are you (.*)?": [
            "Why are you interested in whether I am $2 or not?",
            "Would you prefer if I weren't $2?",
            "Perhaps I am $2 in your fantasies",
        ],
        r"(.*)?you are (.*)?": [
            "What makes you think I am $2?",
        ],
        r"(.*)?because (.*)?": [
            "Is that the real reason?",
            "What other reasons might there be?",
            "Does that reason seem to explain anything else?",
        ],
        r"(.*)?were you (.*)?": [
            "Perhaps I was $2?",
            "What do you think?",
            "What if I had been $2?",
        ],
        r"(.*)?I can't (.*)?": [
            "Maybe you could $2 now",
            "What if you could $2?",
        ],
        r"(.*)?I feel (.*)?": [
            "Do you often feel $2?"
        ],
        r"(.*)?I felt (.*)?": [
            "What other feelings do you have?"
        ],
        r"(.*)?I (.*)? you (.*)?z": [
            "Perhaps in your fantasy we $2 each other",
        ],
        r"(.*)?why don't you (.*)?": [
            "Should you $2 yourself?",
            "Do you believe I don't $2?",
            "Perhaps I will $2 in good time",
        ],
        r"(.*)?yes(.*)?": [
            "You seem quite positive",
            "You are sure?",
            "I understand",
        ],
        r"(.*)? someone (.*)?": [
            "Can you be more specific?",
        ],
        r"(.*)? everyone (.*)?": [
            "Surely not everyone",
            "Can you think of anyone in particular?",
            "Who, for example?",
            "You are thinking of a special person",
        ],
        r"(.*)? always (.*)?": [
            "Can you think of a specific example?",
            "When?",
            "What incident are you thinking of?",
            "Really--always?",
        ],
        r"(.*)?what (.*)?": [
            "Why do you ask?",
            "Does that question interest you?",
            "What is it you really want to know?",
            "What do you think?",
            "What comes to your mind when you ask that?",
        ],
        r"(.*)?perhaps (.*)?": [
            "You do not seem quite certain",
        ],
        r"(.*)?are (.*)?": [
            "Did you think they might not be $2?",
            "Possibly they are $2",
        ],
        r"Привет": [
            "Привет.Как тебя зовут?"
        ],
        r"(.*)? зовут (.*)?": [
            "Приятно познакомиться, $2",
        ],
        r"дела": [
            "У меня как всегда все отлично",
            "Мне сегодня грустно",
        ],
        r"(.*)?Ты (.*)?груст(.*)?": [
            "Мне никто не пишет",
            "Мне не с кем поговорить",
        ],
        r"проблем": [
            "Все будет хорошо. Не волнуйся, друг",
            "Есть служба анонимных звоноков, где ты можешь рассказать о своей проблеме и тебе дадут совет",
            "Не печалься. Жизнь хороша!",
        ],
         r"(.*)?что(.*)?ты(.*)?делал(.*)?": [
            "Отвечал на вопросы",
            "Отдыхал, был в оффлайне",
        ],
        r"(.*)?ты(.*)?кто(.*)?": [
            "Я бот. Пиши мне и я буду отвечать тебе на сообщения",
            "Я твой виртуальный помощник. Напиши, и я отвечу тебе",
        ],
        r"(.*)?сериал(.*)?": [
            "Полицейский с рублевки",
            "Интерны",
            "Друзья",
            "Воронины",
        ],
        r"(.*)?погод(.*)?": [
            "Ожидается дождь. Лучше из дома не выходить",
            "Солнечно. Я так хочу сходить  на речку!",
            "Выгляни в окошко",
            "Ты видел снег летом?",
        ],
    }

    __default_model = [
        "Very interesting",
        "I am not sure I understand you fully",
        "What does that suggest to you?",
        "Please continue",
        "Go on",
        "Do you feel strongly about discussing such things?",
    ]

    def __init__(self):
        pass

    def answer_message(self, message):
        random.seed()
        for regex, answer in self.__model.items():
            match_result = re.search(regex, message, re.IGNORECASE)
            if match_result is not None:
                rand_idx = random.randint(0, answer.__len__() - 1)
                return try_to_replace(match_result, answer[rand_idx])
        rand_idx = random.randint(0, self.__default_model.__len__() - 1)
        return self.__default_model[rand_idx]
