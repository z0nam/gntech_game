from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'QuizBank'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass

"""
최후통첩 2번 항목의 질문은 5개만 하지 뭐 그래서 3개 이상은 제안자로 2개 이하는 응답자로
Q2-1 다음 사람 중 경제학자가 아닌 사람은? 정답(       )  ①존 메나드 케인즈  ② 존 내쉬 ③ 한나 아렌트 ④ 조셉 스티글리츠
Q2-2 하나의 재화를 선택했을 때, 그로 인해 포기한 것들 중 가장 큰 것의 가치를 말하는 개념은? 정답(       )  ① 매몰비용 ②사회적 비용 ③거래비용 ④기회비용
Q2-3 '공유지의 비극'을 얘기한 경제학자는? 정답(       )  ①가렛 하딘  ② 엘리너 오스트롬 ③ 윌리암 헤밀턴 ④ 로버트 악설로드
Q2-4 서로 협력할 경우 서로에게 가장 이익이 되는 상황일때 개인적 욕심으로 서로에게 불리한 상황을 선택하는 게임은? 정답(       )  ① 용의자 딜레마 게임 ②치킨게임 ③ 사슴사냥게임  ④ 제로섬 게임
Q2-5 다음 중에서 한계비용이 '0'에 가까운  상품은? 정답(       )  ① 로봇 ②자동차 ③ Airb&b서비스 ④백옥주사액

독재자 게임의 질문
Q3-1 다음 중에서 독재가가 아닌 사람은? 정답(       )  ① 넬슨 만델라 ② 아돌프 히틀러 ③ 박정희 ④ 베니토 무솔리니
Q3-2 게임이론과 거리가 먼 경제학자는? 정답(       )   ①폰 노이만  ② 존 내쉬 ③ 존 하산니 ④ 조셉 스티글리츠
Q3-3 다음 중 게임의 구성요소가 아닌 것은 ? 정답(       )  ① player ② payoff ③ strategy ④ self-interest
Q3-4 중고자동차를 이르는 말로 적당한 것은 ? 정답(       )  ①lemon ②peach ③apple ④ pear
Q3-5 정보비대칭 해결을 위해 정보를 가지고 있는 측에서 적극적으로 정보를 알리는 행위를 무엇이라 하는가?  정답(       ) ①screening ②signaling ③selection ④rationing
"""

class Quiz():
    def __init__(self, data):
        self.loc = data['loc']
        self.question = data['question'] # String
        self.answer = data['answer'] # Set of key of choice
        self.choices = self.build(data) # Set of Dictionary

    def is_correct(self,choice):
        return self.choices[self.answer] == choice

    def get_choices(self):
        choices = self.choices[:]
        random.shuffle(choices)
        return choices


    def build(self, data):
        return [Choice(c,data) for c in range(1,5)]

class Choice():
    def __init__(self,id,data):
        self.id = id
        self.value = data[str(id)]


def readCSV(filename):
    quiz = []
    import csv
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            quiz.append(Quiz(row))

    return quiz

quizzes = readCSV('quiz.csv')
