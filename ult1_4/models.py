from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from ult import models as ult

author = 'Your name here'

doc = """
1. 최후통첩게임 1.: 공정성에 대한 평가로서
- 제안자 응답자 정하는 퀴즈: 게임 내용과 무관한

Q1-1: 당신은 행복하다고 느끼십니까?로 하여 두그룹으로 나누고, 많은 쪽 사람들만을 대상으로 하여
Q1-2 당신은 파란색을 좋아하시나요?

1) 전통적인 게임  
2) 기부자와 수령자 바꾸어서
3)금액과 수락여부를 알려주고 난 다음에
4)거부당한 사람이 누구인지 알려준 다음에 <-- 이 부분에 해당함.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Constants(BaseConstants,ult.Constants):
    name_in_url = 'ult1_4'


class Subsession(BaseSubsession):
    pass



class Group(BaseGroup,ult.Group):
    amount_offered = models.CurrencyField(choices=Constants.offer_choices)
    offer_accepted = models.BooleanField()


class Player(BasePlayer,ult.Player):
    is_exception = models.BooleanField(default=False) # 사람 수가 맞는지를 체크하기 위한 것. True이면 이 사람은 조 배정에서 남는 사람으로, 이 사람에 대한 처리를 항상 해주어야 한다.

    def get_prev_payoffs(self):
        players = self.participant.get_players()
        payoffList = []
        for i in range(len(players)):
            if i > 0: #exclude survey
                payoffList.append(players[i].payoff)

        return payoffList

    def get_prev_list(self):
        players = self.participant.get_players()
        games = []
        for i in range(len(players)):
            if i >0 :
                games.append("Game "+str(i))
        return games

class History(ult.History):
    pass
