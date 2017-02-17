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

# utl1에서는 취향 질문에 따라 역할을 배정한다. 질문은 binary choice q1, q2
# 일단 q1에 기반하여 매칭한 뒤, 남는 사람들을 q2로 매칭하고 그래도 남는 사람들은
# 임의배정하는 알고리즘을 사용하기로 함.


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

            rnd_num = random.randint(1,2)

            q2_1_players = [p for p in largerGroup if p.participant.vars['q2'] == True]
            q2_2_players = [p for p in largerGroup if p.participant.vars['q2'] == False]

            count1 = len(q2_1_players)
            count2 = len(q2_2_players)

            if count1 < count2:
                smallerGroup = q2_1_players
                largerGroup = q2_2_players
            else:
                smallerGroup = q2_2_players
                largerGroup = q2_1_players

            while smallerGroup:
                if rnd_num == 1:
                    new_group = [
                        q2_1_players.pop(),
                        q2_2_players.pop()
                    ]
                else:
                    new_group = [
                        q2_2_players.pop(),
                        q2_1_players.pop()
                    ]
                group_matrix.append(new_group)

                # 이러고도 남는 아이들은 어쩔 수 없이 랜덤으로 배치한다.
            while largerGroup:
                if len(largerGroup) > 1:
                    new_group = [
                        largerGroup.pop(),
                        largerGroup.pop()
                    ]
                # 만일 한 명만 남았다면 이 사람은 예외 처리를 해야 한다. 이것을 처리하기 위해서는 크게 두 가지 방식이 있다. (1) 게임 밖에서 처리하는 방식. 즉, 이때는 참가자가 홀수일 경우 추첨을 해서 한 사람 빼고 나머지 짝수 인원으로만 하게 해서 절대 이런 상황이 나오지 않게 하는 것인데, 경험상 좋지 않다. (2) 예외처리를 하는 방법. 코딩이 복잡해지는데, 예외 플래그를 만들어서 체크하는 수 밖에 없을 듯하다.
                elif len(largerGroup) == 1:
                    largerGroup.pop().is_exception = True
                group_matrix.append(new_group)

            self.set_group_matrix(group_matrix)
        else:
            self.group_like_round(1)



class Group(BaseGroup):
    amount_offered = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.BooleanField()

    def set_payoffs(self): # 1명 그룹이 있을 경우에는 이 부분을 통과할 수 없어야 한다. view 차원에서 아예 블로킹 되어 있어야 함.
        p1, p2 = self.get_players()
        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):
    is_exception = models.BooleanField(default=False) # 사람 수가 맞는지를 체크하기 위한 것. True이면 이 사람은 조 배정에서 남는 사람으로, 이 사람에 대한 처리를 항상 해주어야 한다.

    def role(self):
        if self.id_in_group == 1:
            return '제안자'
        if self.id_in_group == 2:
            return '응답자'
