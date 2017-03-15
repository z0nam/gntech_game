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
3)금액과 수락여부를 알려주고 난 다음에 <-- 이 부분에 해당함.
~~~~~~~~~~~~~~~~~~~~~~~
4)거부당한 사람이 누구인지 알려준 다음에
"""


class Constants:
    name_in_url = 'ult1_3'
    players_per_group = None
    endowment = c(10000)
    payoff_if_rejected = c(0)
    offer_incr = c(1000)

    offer_choices = currency_range(0,endowment,offer_incr)

    choices = []
    for offer in offer_choices:
        choices.append((offer, endowment - offer))

    num_rounds = 1


class Group:
    def set_payoffs(self): # 1명 그룹이 있을 경우에는 이 부분을 통과할 수 없어야 한다. view 차원에서 아예 블로킹 되어 있어야 함.
        if len(self.get_players())!=2:
            return
        p1, p2 = self.get_players()
        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player:

    def test(self):
        return [1,2,3]

    def role(self):
        if self.id_in_group == 1:
            return '제안자'
        if self.id_in_group == 2:
            return '응답자'

    def get_partner(self):
        return self.get_others_in_group()[0]

        # 응답자였을 때의 결과만을 return해준다.
    def get_historic_results(self,role):
        # return [1,2,3]
        playerHistory =  self.participant.get_players()[1:3]

        response = []
        for p in playerHistory:
            if p.id_in_group==role:
                history = History(p.group.amount_offered,self.trans(p.group.offer_accepted))
                response.append(history)
        return response

    def get_responder_history(self):
        response = self.get_historic_results(2)
        return response

    def get_proposer_history(self):
        response =  self.get_historic_results(1)
        return response

    def trans(self,msg):
        if msg:
            return "수락"
        else:
            return "거절"


class History:
    def __init__(self,offered,accepted):
        self.offered=offered
        self.accepted=accepted
