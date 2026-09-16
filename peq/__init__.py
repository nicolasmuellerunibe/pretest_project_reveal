from otree.api import *


author = 'Marte Abts'

doc = """
Post Experimental Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'peq'
    players_per_group = None
    num_rounds = 1
    progress_template = 'peq/progress_bar.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

  task1 = models.IntegerField(
        label='I enjoyed working on the decision-making task.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  task2 = models.IntegerField(
        label='The decision-making task was challenging',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  control1 = models.IntegerField(
        label='your ability?',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  control2 = models.IntegerField(
        label='your effort?',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  control3 = models.IntegerField(
        label='the difficulty of the task?',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  control4 = models.IntegerField(
        label='good and bad luck?',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  affected1 = models.IntegerField(
        label='My project choice(s) directly affected my net performance in the task.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  affected2 = models.IntegerField(
        label='I felt that revealing more attribute values helped me to choose a project with a higher realized value.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  affected3 = models.IntegerField(
        label='I was in control over my performance outcomes in the task.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )

  clear = models.IntegerField(
        label='The instructions of the decision-making task were clear.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  age = models.IntegerField(
        label='What is your age (in years)? ', min=17, max=80)
  gender = models.IntegerField(
        label='Please indicate your gender',
        choices=[[1, 'Male'], [2, 'Female'], [3, 'Diverse'], [4, 'Prefer not to answer']])

  study = models.IntegerField(
        label='What is your academic major?',
        choices=[[1, 'Economics'], [2, 'Business Economics'], [3, 'Law'],
                 [4, 'Science & Health'],[5, 'Psychology'],[6, 'Other']])
  grade = models.IntegerField(
        label='What is your current grade status',
        choices=[[1, 'High School'],[2, 'Bachelor'], [3, 'Master'], [4, 'PhD']])

  training10 = models.IntegerField(
        label='I found it difficult to understand the first training session.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )

  training11 = models.IntegerField(
        label='I would have chosen to take the first training if it had been voluntary.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  training12 = models.IntegerField(
        label='The first training helped me understand how to perform the task better.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )

  training20 = models.IntegerField(
      label='I found it difficult to understand the second training session.',
      choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
      widget=widgets.RadioSelectHorizontal
  )

  training21 = models.IntegerField(
      label='I would have chosen to take the second training if it had been voluntary.',
      choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
      widget=widgets.RadioSelectHorizontal
  )
  training22 = models.IntegerField(
      label='The second training helped me understand how to perform the task better.',
      choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
      widget=widgets.RadioSelectHorizontal
  )
  training30 = models.IntegerField(
      label='I found it difficult to understand the third training session.',
      choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
      widget=widgets.RadioSelectHorizontal
  )

  training31 = models.IntegerField(
      label='I would have chosen to take the third training if it had been voluntary.',
      choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
      widget=widgets.RadioSelectHorizontal
  )
  training32 = models.IntegerField(
      label='The third training helped me understand how to perform the task better.',
      choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly Agree']],
      widget=widgets.RadioSelectHorizontal
  )

  #attention checks
  attentioncheck1 = models.IntegerField(
        label='choose Strongly Disagree.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''],[6,''],[7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )
  attentioncheck2 = models.IntegerField(
        label='Choose Not at All.',
        choices=[[1, 'Strongly Disagree'], [2, ''], [3, ''], [4, ''], [5, ''],[6,''],[7, 'Strongly Agree']],
        widget=widgets.RadioSelectHorizontal
    )

  open = models.LongStringField(
      label='Do you want to share any thoughts about the experiment with the researchers?',
      blank=True
  )

# PAGES
class Task(Page):
    form_model = 'player'
    form_fields = ['task1', 'task2', 'clear']

    def is_displayed(player:Player):
        return player.round_number==1

class sep(Page):
    form_model = 'player'
    form_fields = ['control1', 'control2','control3', 'control4','affected1','affected2','affected3']

    def is_displayed(player:Player):
        return player.round_number==1

class Fin(Page):
    form_model = 'player'
    form_fields = ['age','gender','study','grade', 'open']

    def is_displayed(player: Player):
        return player.round_number == 1


class Payout(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        # Sum all trial_net_performances across all rounds (1–36)
        p = player.participant
        all_perfs = p.vars.get('trial_net_performances', {})
        total_points = sum(all_perfs.get(i, 0) for i in range(1, 37))

        base_pay    = 3.00          # EUR 3 show-up fee
        rate        = 1.00 / 3000   # EUR 1 per 3000 points
        bonus       = total_points * rate
        payout      = max(base_pay, base_pay + bonus)  # floor at EUR 3

        return dict(
            total_points=round(total_points, 2),
            bonus_pay=round(max(0, bonus), 2),
            payout=round(payout, 2),
        )

class ENDEND(Page):
    def is_displayed(player:Player):
        return player.round_number==1

class T1(Page):
    form_model = 'player'
    form_fields = ['training10', 'training11', 'training12']

    def is_displayed(player:Player):
        return player.round_number==1

class T2(Page):
    form_model = 'player'
    form_fields = ['training20', 'training21', 'training22']

    def is_displayed(player: Player):
        return player.round_number == 1

class T3(Page):
    form_model = 'player'
    form_fields = ['training30', 'training31', 'training32']

    def is_displayed(player: Player):
        return player.round_number == 1

page_sequence = [sep, Task, T1, T2, T3, Fin, Payout, ENDEND]