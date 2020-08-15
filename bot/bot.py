from pytrivia import Trivia
import logging

STATE = "state"
NUM_QUESTIONS = "num questions"
QUESTIONS = "1"
GAME = "3"
QUESTIONS_LIST = "questions"
QCOUNTER = "qcounter"


class Bot(object):
    def __init__(self):
        self.trivia = Trivia(True)
        self.id = id
        logging.basicConfig(level=logging.INFO)


    def get_questions(self, session):
        session[QUESTIONS_LIST] = self.trivia.request(session[NUM_QUESTIONS])['results']
        logging.info("obtaining questions")

    def Handle(self, session, text: str):
        try:
            if STATE not in session or session[STATE] is None:
                session[STATE] = QUESTIONS
                return "Сколько вопросов будем играть?"
            elif session[STATE] == QUESTIONS:
                try:
                    session[NUM_QUESTIONS] = int(text)
                except:
                    return "Не поняла, введи число заново"
                session[STATE] = GAME
                return "Ищу вопросы. Приготовьтесь! Когда будете готовы, напишите что-нибудь."
            elif session[STATE] == GAME:
                if QCOUNTER not in session or session[QCOUNTER] == 0 or session[QCOUNTER] is None:
                    self.get_questions(session)
                    session[QCOUNTER] = 0
                if session[QCOUNTER] == session[NUM_QUESTIONS]:
                    session[STATE] = None
                    session[QCOUNTER] = 0
                    return "Поздравляем, игра закончилась! Напишите, когда захотите поиграть еще!"
                session[QCOUNTER] += 1
                return session[QUESTIONS_LIST][session[QCOUNTER] - 1]['question']
            else:
                session[STATE] = None
                return "Что-то пошло не так. Давайте заново. Ответьте что-нибудь"
        except Exception as e:
            print(e)
            session[STATE] = None
            session[QCOUNTER] = 0
            return "Я перегрелась. Скажи что-нибудь, давай начнем заново!"
