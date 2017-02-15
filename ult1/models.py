from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


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
