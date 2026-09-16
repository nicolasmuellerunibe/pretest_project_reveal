from otree.api import *

author = 'Marte Abts'

doc = """
Introduction
"""

import itertools


class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    import random

    if subsession.round_number == 1:
        for p in subsession.get_players():
            # randomly assign treatment
            p.participant.vars['treatment'] = random.choice(['high_', 'low_'])
            print('participant.vars is', p.participant.vars['treatment'])



def group_by_arrival_time_method(subsession, waiting_players):
        print("starting group_by_arrival_time_method")
        from collections import defaultdict
        d = defaultdict(list)
        for p in waiting_players:
            print("Participant ID: ", p.id_in_group)
            print("Participant treatment:", p.participant.vars['treatment'])
            treatment = p.participant.vars['treatment']
            players_with_this_treatment = d[treatment]
            players_with_this_treatment.append(p)
            if len(players_with_this_treatment) == 4:
                print("forming group...")
                return players_with_this_treatment



class Group(BaseGroup):
    treatment = models.StringField()


class Player(BasePlayer):
    #rightanswerAcc= models.BooleanField(label='',choices=[True, False])
    #rightanswerPay = models.BooleanField(label='',choices=[True, False])
    informedconsent = models.BooleanField(
        label='',
        choices=[
            [True, 'I agree to participate in this study. The study will start shortly.'],
            [False,
             'I do not agree to participate in this study. The study will end here.'],
        ],
        widget=widgets.RadioSelect,
    )

    question1=models.IntegerField(label='1. Employees will perform a decision-making task for six periods. Each period consists of six rounds.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question2=models.IntegerField(label='2. In every round, employees need to select one out of five projects.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question3=models.IntegerField(label='3. The Expected Project Value of a project is determined by multiplying the Attribute Values (A1, A2, A3, A4) with their respective Attribute Weights (WeightA1, Weight A2, WeightA3, WeightA4).', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question4=models.IntegerField(label='4. To determine which project offers the highest Expected Project Value, an employee can choose to reveal the Attribute Values A1, A2, A3 and A4 for each of the five projects.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question5=models.IntegerField(label='5. Revealing an Attribute Value automatically updates the Expected Project Value (EV Revealed).', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question6=models.IntegerField(label='6.	Once an Attribute Value is revealed, employees can undo the revealing.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question7=models.IntegerField(label='7.	I am allowed to refresh/reload the page during the experiment.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question8=models.IntegerField(label='8.	The Attribute Weights range from 10 to 40, and the three Attribute Weights always sum up to 100.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question9=models.IntegerField(label='9.	Revealing Attribute Values is free of cost.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question10_low=models.IntegerField(label='10. The Realized Project Value of a project is determined by the Expected Project Value plus the Noise Term. The Noise Term ranges between [-50; +50].', choices=[[1, '[-50; +50] '],[2,'[-150; +150]'],[3,'[-250; +250]']],widget=widgets.RadioSelect,)
    question10_high = models.IntegerField(label='10. The Realized Project Value of a project is determined by the Expected Project Value plus the Noise Term. The Noise Term ranges between [-50; +50].', choices=[[1, '[-50; +50] '], [2, '[-150; +150]'], [3, '[-250; +250]']], widget=widgets.RadioSelect, )
    question11=models.IntegerField(label='11. Employees are paid based on their Performance. The Performance in a round corresponds to the Realized Project Value less Total Reveal Costs and less Total Revisit Costs.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question12=models.IntegerField(label='12. After selecting a project, employees receive feedback on Realized Project Value of the selected project.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question13=models.IntegerField(label='13. Employees are paid based on the sum of the Period Performance for all periods.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question14=models.IntegerField(label='14. Participants complete a training after Periods 2, 3, and 4.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question15=models.IntegerField(label='15. Employees can revisit the training insights in later periods, but this incurs a cost of 100 points every time they revisit a training insight.', choices=[[1, 'True'],[2,'False']],widget=widgets.RadioSelect,)
    question1_feedback = models.StringField(blank=True)


    def get_categories(self):
        if self.participant.vars['treatment'] == 'high_':
            self.participant.vars['noise'] = 'high'
            #self.participant.vars['orientation'] = 'past'
        if self.participant.vars['treatment'] == 'low_':
            self.participant.vars['noise'] = 'low'
            #self.participant.vars['orientation'] = 'future'

#PAGES

class Welcome(Page):
    pass

class InformedConsent(Page):
    form_model = 'player'
    form_fields = ['informedconsent']

class BlockDropouts(Page):
    def is_displayed(player: Player):
        return player.informedconsent == False

class Overview(Page):
    pass

class Task_1(Page):
    pass

class Task_2(Page):
    pass

class Task_3(Page):
    pass

class Task_4(Page):
    pass

class Task_5_low(Page):
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars['noise'] == 'low'

class Task_5_high(Page):
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars['noise'] == 'high'

class WelcomeScreen(Page):
    timeout_seconds = 0.0000000001

    def before_next_page(player: Player,  timeout_happened):
        player.get_categories()
        print('def_get_categories')

    def is_displayed(player):
        return player.round_number == 1

class ExampleTask1(Page):
    pass

class ExampleTask2(Page):
    pass

class ExampleTask3(Page):
    pass

#class EmployeeFeedback(Page):
 #   pass

class EmployeeTraining(Page):
    pass

class NetPerformance(Page):
    pass


class RecapQuiz1(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class RecapQuiz2(Page):
     def is_displayed(player: Player):
        return player.round_number == 1


class RecapQuiz3(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz4(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class RecapQuiz5(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz6(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class RecapQuiz7(Page):

    def is_displayed(player: Player):
        return player.round_number == 1


class RecapQuiz8(Page):

    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz9(Page):

    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz11(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz_high(Page):

    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars['noise'] == 'high'

class RecapQuiz_low(Page):

    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars['noise'] == 'low'

class EmployeeFeedback_low(Page):

    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars['noise'] == 'low'

class EmployeeFeedback_high(Page):

    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars['noise'] == 'high'

class RecapQuiz12(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz13(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz14(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class RecapQuiz15(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class PreQuiz(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

class StartTask(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

page_sequence = [Welcome,
                 InformedConsent,
                 BlockDropouts,
                 Overview,
                 Task_1,
                 Task_2,
                 Task_3,
                 Task_4,
                 WelcomeScreen,
                 Task_5_low,
                 Task_5_high,
                 EmployeeTraining,
                 NetPerformance,
                 EmployeeFeedback_high,
                 EmployeeFeedback_low,
                 PreQuiz,
                 RecapQuiz1,
                 RecapQuiz2,
                 RecapQuiz3,
                 RecapQuiz4,
                 RecapQuiz5,
                 RecapQuiz6,
                 RecapQuiz7,
                 RecapQuiz8,
                 RecapQuiz9,
                 RecapQuiz_high,
                 RecapQuiz_low,
                 RecapQuiz11,
                 RecapQuiz12,
                 RecapQuiz13,
                 RecapQuiz14,
                 RecapQuiz15,
                 StartTask,
                 ]
