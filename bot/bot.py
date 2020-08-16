import logging

from pytrivia import Trivia, Diffculty, Type

STATE = "state"
NUM_QUESTIONS = "num questions"
QUESTIONS = "1"
GAME = "3"
WAITING_FOR_ANSWER = "4"
QUESTIONS_LIST = "questions"
QCOUNTER = "qcounter"
SCORE = "score"


class Bot(object):
    def __init__(self):
        self.trivia = Trivia(True)
        self.id = id
        logging.basicConfig(level=logging.INFO)

    def get_questions(self, session):
        session[QUESTIONS_LIST] = self.trivia.request(session[NUM_QUESTIONS], None, Diffculty.Easy, Type.True_False)[
            'results']
        logging.info("obtaining questions")

    def recognize_ans(self, ans):
        try:
            val = int(ans)
            if val == 1:
                return "True"
            if val == 2:
                return "False"
        except:
            return None

    def Handle(self, session, text: str):
        if STATE not in session or session[STATE] is None or text.lower() == "сброс":
            session[STATE] = QUESTIONS
            return "Начинаем игру. Сколько вопросов будем играть?"
        elif session[STATE] == QUESTIONS:
            try:
                session[NUM_QUESTIONS] = int(text)
            except:
                return "Не поняла, введи число заново"
            session[STATE] = GAME
            return "Ищу вопросы. Приготовьтесь! Когда будете готовы, напишите что-нибудь."
        elif session[STATE] == GAME:
            prefix = ""
            if WAITING_FOR_ANSWER in session and session[WAITING_FOR_ANSWER]:
                ans = self.recognize_ans(text)
                if ans is None:
                    return "Не поняла твой ответ. Введи 1, если правда, и 2, если ложь!"
                session[WAITING_FOR_ANSWER] = False
                if ans == session[QUESTIONS_LIST][session[QCOUNTER] - 1]['correct_answer']:
                    prefix = "Правильно! "
                    session[SCORE] += 1
                else:
                    prefix = "Неправильно! "

            if QCOUNTER not in session or session[QCOUNTER] == 0 or session[QCOUNTER] is None:
                self.get_questions(session)
                session[QCOUNTER] = 0
                session[WAITING_FOR_ANSWER] = False
                session[SCORE] = 0
            if session[QCOUNTER] == session[NUM_QUESTIONS]:
                session[STATE] = None
                session[QCOUNTER] = 0
                old_score = session[SCORE]
                session[SCORE] = 0
                session[WAITING_FOR_ANSWER] = False
                return prefix + ("Поздравляем, игра закончилась! Вы набрали %d очков. "
                                 "Напишите, когда захотите поиграть еще!" % (old_score))
            session[QCOUNTER] += 1
            session[WAITING_FOR_ANSWER] = True
            return prefix + session[QUESTIONS_LIST][session[QCOUNTER] - 1]['question']
        else:
            session[STATE] = None
            return "Что-то пошло не так. Давайте заново. Ответьте что-нибудь"
