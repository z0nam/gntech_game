from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


author = 'Namun Cho'

doc = """
1. 최후통첩게임 1.: 공정성에 대한 평가로서
- 제안자 응답자 정하는 퀴즈: 게임 내용과 무관한

Q1-1: 당신은 행복하다고 느끼십니까?로 하여 두그룹으로 나누고, 많은 쪽 사람들만을 대상으로 하여
Q1-2 당신은 파란색을 좋아하시나요?

1) 전통적인 게임  
2) 기부자와 수령자 바꾸어서
3)금액과 수락여부를 알려주고 난 다음에
4)거부당한 사람이 누구인지 알려준 다음에
"""


class Constants(BaseConstants):
    name_in_url = 'ult1'
    players_per_group = 2
    endowment = c(10000)
    payoff_if_rejected = c(0)
    offer_incr = 1000

    offer_choices = currency_range(0,endowment,offer_incr)

    choices = []
    for offer in offer_choices:
        choices.append((offer, endowment - offer))

    num_rounds = 1


class Subsession(BaseSubsession):

"""
utl1에서는 취향 질문에 따라 역할을 배정한다. 질문은 binary choice q1, q2
일단 q1에 기반하여 매칭한 뒤, 남는 사람들을 q2로 매칭하고 그래도 남는 사람들은
임의배정하는 알고리즘을 사용하기로 함.
"""

    def before_session_starts(self):
        rnd_num = random.randint(1,2)  #이 값이 q1- 1이 맡게 될 group id임.
        logging.debug("rnd_num={}".format(rnd_num))
        if self.round_number == 1:
            players = self.get_players() # 일단 플레이어를 모두 모은다.

            q1_1_players = [p for p in players if p.participant.vars['q1']==True]
            q1_2_players = [p for p in players if p.participant.vars['q1']==False]

            group_matrix = []

            count1 = len(q1_1_players)
            count2 = len(q1_2_players)

            if count1 < count2:
                smallerGroup = q1_1_players
                largerGroup = q1_2_players
            else:
                smallerGroup = q1_2_players
                largerGroup = q1_1_players

            while smallerGroup:
                if rnd_num == 1:
                    new_group = [
                        q1_1_players.pop(),
                        q1_2_players.pop()
                    ]
                else:
                    new_group = [
                        q1_2_players.pop(),
                        q1_1_players.pop()
                    ]
                group_matrix.append(new_group)

            # 이 과정을 거치면 둘 중 더 많은 놈이 남는다. 따라서 q2에 기반하여 동일한 내용을 반복한다.

            q2_1_players = [p for p in largerGroup if p.participant.vars['q2'] == True]
            q2_2_players = [p for p in largerGroup if p.participant.vars['q2'] == False]

            







class Group(BaseGroup):
    pass


class Player(BasePlayer):
    proposed_amount = models.CurrencyField(min=0,max=Constants.endowment)

    accept_reject = models.BooleanField() # true:accept, false:reject

    def role(self):
        if self.id_in_group == 1:
            return 'Proposer'
        if self.id_in_group == 2:
            return 'Responder'
