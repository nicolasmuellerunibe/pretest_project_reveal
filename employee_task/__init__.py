from otree.api import *
import json


class Constants(BaseConstants):
    name_in_url = 'employee_task'
    players_per_group = None
    num_rounds = 55

    # Match your logic: 7, 15, 25, 35, 45, 53
    REVIEW_ROUNDS = [7, 15, 25, 35, 45, 53]
    # Match your logic: 16, 26, 36
    OFFER_ROUNDS = [16, 26, 36]
    # Match your logic: 17, 27, 37
    TRAINING_ROUNDS = [17, 27, 37]


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    for p in subsession.get_players():
        p.participant.vars.setdefault('current_trial_index', 1)
        p.participant.vars.setdefault('trial_net_performances', {})
        p.participant.vars.setdefault('trigger_empty_page_in_round', 0)
        for i in range(1, 4):
            p.participant.vars.setdefault(f'training_{i}_taken', False)
            p.participant.vars.setdefault(f'training_{i}_done', False)

    # In Subsession.creating_session
    for p in subsession.get_players():
        treatment = p.participant.vars.get('treatment', 'high_')  # default fallback
        if treatment == 'high_':
            from .hardcoded_trials_high import TRIALS as trial_data, WEIGHTS as weights_data
        else:
            from .hardcoded_trials_low import TRIALS as trial_data, WEIGHTS as weights_data
        p.participant.vars['TRIALS'] = trial_data
        p.participant.vars['WEIGHTS'] = weights_data


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    selected_option = models.IntegerField(blank=True, null=True)
    value_of_choice = models.FloatField(blank=True, null=True)
    num_revealed_fields = models.IntegerField(initial=0)
    reveal_cost_total = models.FloatField(blank=True, null=True)
    revisited_trainings = models.LongStringField(blank=True)
    revisit_cost = models.FloatField(blank=True, null=True)

    action_plan_suggestions = models.LongStringField(
        label='What actions or strategies do you think would help you perform better in the project-selection task?',
        blank=True
    )

    # save the refresh penalty
    refresh_penalty = models.CurrencyField(initial=0)

    trial_net_performance = models.FloatField(initial=0)
    revealed_fields = models.LongStringField(blank=True)

    visited_training = models.IntegerField(blank=True, null=True)
    training_accepted = models.BooleanField(blank=True)
    wants_training = models.BooleanField(blank=True, initial=False)


# -----------------------------------------------------------------------------
# Helper functions
# These contain the exact same logic that previously lived as Page instance
# methods in pages.py. In single-file oTree apps, page callbacks receive Player
# directly, so helpers are kept at module level.
# -----------------------------------------------------------------------------

def get_period_info(trial_idx):
    """Helper to determine period and relative round."""
    if 1 <= trial_idx <= 6:
        return 1, trial_idx
    if 7 <= trial_idx <= 12:
        return 2, trial_idx - 6
    if 13 <= trial_idx <= 18:
        return 3, trial_idx - 12
    if 19 <= trial_idx <= 24:
        return 4, trial_idx - 18
    if 25 <= trial_idx <= 30:
        return 5, trial_idx - 24
    if 31 <= trial_idx <= 36:
        return 6, trial_idx - 30
    return 0, 0


def get_lowest_open_training_num(participant):
    for i in range(1, 4):
        if not participant.vars.get(f'training_{i}_done', False):
            return i
    return 0


def get_slot_for_round(round_number):
    # Updated to match your logic: 17->1, 27->2, 37->3
    if round_number == 17:
        return 1
    if round_number == 27:
        return 2
    if round_number == 37:
        return 3
    return 0


def get_period_num(round_num):
    # Updated mapping to match your specified rounds
    mapping = {7: 1, 15: 2, 25: 3, 35: 4, 45: 5, 53: 6}
    return mapping.get(round_num, 0)


def get_trial_range_for_period(period_num):
    ranges = {
        1: range(1, 7),
        2: range(7, 13),
        3: range(13, 19),
        4: range(19, 25),
        5: range(25, 31),
        6: range(31, 37)
    }
    return ranges.get(period_num, range(0))


def calculate_review_period_performance(player):
    p = player.participant
    period_num = get_period_num(player.round_number)
    trial_range = get_trial_range_for_period(period_num)
    total_perf = sum(
        p.vars.get('trial_net_performances', {}).get(i, 0)
        for i in trial_range
    )
    return round(total_perf, 2)


def calculate_final_period_performance(player, period_num):
    mapping = {
        1: range(1, 7),
        2: range(7, 13),
        3: range(13, 19),
        4: range(19, 25),
        5: range(25, 31),
        6: range(31, 37)
    }
    trial_range = mapping.get(period_num, range(0))

    p = player.participant
    total_perf = sum(
        p.vars.get('trial_net_performances', {}).get(i, 0)
        for i in trial_range
    )
    return round(total_perf, 2)


# -----------------------------
# 1. Reveal Page
# -----------------------------
class Reveal(Page):
    form_model = 'player'
    form_fields = [
        'selected_option',
        'revisit_cost',
        'revealed_fields',
        'num_revealed_fields',
        'revisited_trainings',
        'refresh_penalty',
    ]

    @staticmethod
    def vars_for_template(player):
        p = player.participant
        r = p.vars['current_trial_index']

        period_num, round_in_period = get_period_info(r)

        # Pull trial and period-specific weight data
        trial_options = p.vars.get('TRIALS', {}).get(r, [])
        all_weights = p.vars.get('WEIGHTS', {})
        current_weights = all_weights.get(period_num, {})

        reveal_cost = current_weights.get('RevealCost', 0)

        options = []
        for row in trial_options:
            options.append({
                'name': f"Project {row['Opt']}",
                'Opt': row['Opt'],
                'fields': [row['A1'], row['A2'], row['A3'], row['A4']],
                'ev_weights': [
                    current_weights.get('A1', 0),
                    current_weights.get('A2', 0),
                    current_weights.get('A3', 0),
                    current_weights.get('A4', 0)
                ],
                'true_value': row['true_value']
            })

        training_done_status = {
            1: p.vars.get('training_1_done', False),
            2: p.vars.get('training_2_done', False),
            3: p.vars.get('training_3_done', False)
        }

        # Hardcoded training data for revisits (Static)
        training_data = {
            1: {
                'data': [
                    {'Opt': 1, 'A1': 3, 'A2': 5, 'A3': 4, 'A4': 2},
                    {'Opt': 2, 'A1': 6, 'A2': 4, 'A3': 1, 'A4': 1},
                    {'Opt': 3, 'A1': 8, 'A2': 2, 'A3': 2, 'A4': 1},
                    {'Opt': 4, 'A1': 1, 'A2': 7, 'A3': 5, 'A4': 2},
                    {'Opt': 5, 'A1': 1, 'A2': 1, 'A3': 1, 'A4': 1}
                ],
                'weights': {'A1': 20, 'A2': 40, 'A3': 20, 'A4': 10},
                'correct_answer': 'A2'
            },
            2: {
                'data': [
                    {'Opt': 1, 'A1': 5, 'A2': 5, 'A3': 9, 'A4': 2},
                    {'Opt': 2, 'A1': 4, 'A2': 4, 'A3': 8, 'A4': 2},
                    {'Opt': 3, 'A1': 7, 'A2': 2, 'A3': 11, 'A4': 3},
                    {'Opt': 4, 'A1': 1, 'A2': 7, 'A3': 5, 'A4': 1},
                    {'Opt': 5, 'A1': 1, 'A2': 1, 'A3': 1, 'A4': 1}
                ],
                'weights': {'A1': 20, 'A2': 40, 'A3': 20, 'A4': 10},
                'correct_answer': 'A1+4'
            },
            3: {
                'data': [
                    {'Opt': 1, 'A1': 3, 'A2': 2, 'A3': 1, 'A4': 4},
                    {'Opt': 2, 'A1': 6, 'A2': 5, 'A3': 2, 'A4': 1},
                    {'Opt': 3, 'A1': 9, 'A2': 9, 'A3': 3, 'A4': 2},
                    {'Opt': 4, 'A1': 12, 'A2': 8, 'A3': 4, 'A4': 2},
                    {'Opt': 5, 'A1': 1, 'A2': 1, 'A3': 1, 'A4': 1}
                ],
                'weights': {'A1': 10, 'A2': 40, 'A3': 40, 'A4': 10},
                'correct_answer': 'opt1'
            }
        }

        return dict(
            trial_num=r,
            period_num=period_num,
            round_in_period=round_in_period,
            options=options,
            reveal_cost=reveal_cost,
            training_done_status=training_done_status,
            training_data=training_data,
            player_code=player.participant.code
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        p = player.participant
        r = p.vars['current_trial_index']

        period_num, _ = get_period_info(r)

        selected = player.selected_option
        revisit_cost = player.revisit_cost or 0.0
        refresh_penalty = player.refresh_penalty or 0.0

        trial_options = p.vars['TRIALS'].get(r, [])
        all_weights = p.vars.get('WEIGHTS', {})
        current_weights = all_weights.get(period_num, {})

        # --- Value of Choice ---
        value_of_choice = 0
        if selected is not None:
            for row in trial_options:
                if row['Opt'] == selected:
                    value_of_choice = row['true_value']
                    break
        player.value_of_choice = value_of_choice

        # --- Reveal Cost (Period Specific) ---
        reveal_cost_per_field = current_weights.get('RevealCost', 0)
        num_revealed = player.num_revealed_fields or 0
        total_reveal_cost = num_revealed * reveal_cost_per_field
        player.reveal_cost_total = total_reveal_cost

        # --- Net Performance ---
        total_costs_with_penalty = total_reveal_cost + revisit_cost + refresh_penalty
        player.trial_net_performance = float(value_of_choice - total_costs_with_penalty)

        # Revisit Logic
        COST_PER_REVISIT = 100.0
        num_revisits = round(revisit_cost / COST_PER_REVISIT) if revisit_cost > 0 else 0

        if 'review_data' not in p.vars:
            p.vars['review_data'] = {}

        p.vars['review_data'][r] = {
            'value': player.value_of_choice or 0.0,
            'reveals': player.num_revealed_fields or 0,
            'reveal_cost': total_reveal_cost,
            'revisit_cost': revisit_cost,
            'net_perf': player.trial_net_performance,
            'total_cost': total_costs_with_penalty,
            'num_revisits': num_revisits,
            'refresh_penalty': refresh_penalty,
        }

        if 'trial_net_performances' not in p.vars:
            p.vars['trial_net_performances'] = {}

        p.vars['trial_net_performances'][r] = player.trial_net_performance

        player.visited_training = None
        p.vars['current_trial_index'] += 1

    @staticmethod
    def is_displayed(player):
        p = player.participant
        r = player.round_number

        # 1. Block Reveal on all non-working rounds defined in Constants
        if r in Constants.OFFER_ROUNDS or r in Constants.REVIEW_ROUNDS or r in Constants.TRAINING_ROUNDS:
            return False

        # 2. Block Reveal on explicit transition/buffer rounds
        if r in [8, 18, 28, 38, 46, 54, 55]:
            return False

        # 3. Block Reveal if the EmptyPage trigger is active
        if p.vars.get('trigger_empty_page_in_round') == r:
            return False

        # 4. Correct the "Slot" logic:
        # You must block Reveal if the round falls within the transition window
        # Period 2 transition: 15, 16, 17, 18
        # Period 3 transition: 25, 26, 27, 28
        # Period 4 transition: 35, 36, 37, 38
        if 15 <= r <= 18:
            return False
        if 25 <= r <= 28:
            return False
        if 35 <= r <= 38:
            return False

        # 5. Stop if all 36 trials are completed
        if p.vars.get('current_trial_index', 1) > 36:
            return False

        return True


# -----------------------------
# TrainingOffer Page
# -----------------------------
class TrainingOffer(Page):
    form_model = 'player'
    form_fields = ['wants_training']

    @staticmethod
    def is_displayed(player):
        return player.round_number in Constants.OFFER_ROUNDS

    @staticmethod
    def vars_for_template(player):
        # Maps the specific round to the correct training number
        mapping = {16: 1, 26: 2, 36: 3}
        return dict(offer_training_num=mapping.get(player.round_number, 0))

    @staticmethod
    def before_next_page(player, timeout_happened):
        p = player.participant
        # Ensure round mapping matches OFFER_ROUNDS
        round_to_training = {16: 1, 26: 2, 36: 3}.get(player.round_number, 0)
        if round_to_training:
            p.vars[f'training_{round_to_training}_taken'] = player.wants_training


# -----------------------------
# TrainingGate Page
# -----------------------------
class TrainingGate(Page):

    @staticmethod
    def is_displayed(player):
        p = player.participant
        r = player.round_number

        if r not in Constants.TRAINING_ROUNDS:
            return False

        slot = get_slot_for_round(r)
        # Verify they accepted it in the Offer round
        if not p.vars.get(f'training_{slot}_taken', False):
            return False

        return True

    @staticmethod
    def vars_for_template(player):
        training_num = get_lowest_open_training_num(player.participant)

        # hardcoded trainingsdata
        training_data = {
            1: {
                'options': [
                    {'name': 'Project 1', 'fields': [3, 5, 4, 2], 'ev_weights': [30, 40, 20, 10]},
                    {'name': 'Project 2', 'fields': [6, 4, 1, 1], 'ev_weights': [30, 40, 20, 10]},
                    {'name': 'Project 3', 'fields': [8, 2, 2, 3], 'ev_weights': [30, 40, 20, 10]},
                    {'name': 'Project 4', 'fields': [1, 7, 5, 2], 'ev_weights': [30, 40, 20, 10]},
                    {'name': 'Project 5', 'fields': [1, 1, 1, 1], 'ev_weights': [30, 40, 20, 10]}
                ],
                'correct_answer': 'A2'
            },
            2: {
                'options': [
                    {'name': 'Project 1', 'fields': [5, 5, 9, 1], 'ev_weights': [30, 20, 40, 10]},
                    {'name': 'Project 2', 'fields': [4, 4, 8, 2], 'ev_weights': [30, 20, 40, 10]},
                    {'name': 'Project 3', 'fields': [7, 2, 11, 3], 'ev_weights': [30, 20, 40, 10]},
                    {'name': 'Project 4', 'fields': [1, 7, 5, 4], 'ev_weights': [30, 20, 40, 10]},
                    {'name': 'Project 5', 'fields': [1, 1, 1, 1], 'ev_weights': [30, 20, 40, 10]}
                ],
                'correct_answer': 'A1+4'
            },
            3: {
                'options': [
                    {'name': 'Project 1', 'fields': [3, 2, 1, 3], 'ev_weights': [10, 40, 40, 10]},
                    {'name': 'Project 2', 'fields': [6, 5, 2, 2], 'ev_weights': [10, 40, 40, 10]},
                    {'name': 'Project 3', 'fields': [9, 9, 3, 3], 'ev_weights': [10, 40, 40, 10]},
                    {'name': 'Project 4', 'fields': [12, 8, 4, 4], 'ev_weights': [10, 40, 40, 10]},
                    {'name': 'Project 5', 'fields': [1, 1, 1, 1], 'ev_weights': [10, 40, 40, 10]}
                ],
                'correct_answer': 'opt1'
            }
        }

        options = training_data.get(training_num, {}).get('options', [])
        correct_answer = training_data.get(training_num, {}).get('correct_answer', '')

        return dict(
            training_num=training_num,
            options=options,
            correct_answer=correct_answer,
            Constants=Constants
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        p = player.participant
        training_num = get_lowest_open_training_num(p)

        if training_num > 0:
            p.vars[f'training_{training_num}_done'] = True
            p.vars['current_trial_index'] += 0
            p.vars['trigger_empty_page_in_round'] = player.round_number + 1

            player.selected_option = None
            player.revealed_fields = json.dumps([])
            player.num_revealed_fields = 0
            player.trial_net_performance = 0
            player.visited_training = training_num
            player.training_accepted = player.wants_training


# -----------------------------
# EmptyPage
# -----------------------------
class EmptyPage(Page):
    timeout_seconds = 3

    @staticmethod
    def is_displayed(player):
        r = player.round_number
        p_vars = player.participant.vars

        # Show if it's a scheduled empty round OR the dynamic trigger is set
        return r in [8, 18, 28, 38, 46, 54] or p_vars.get('trigger_empty_page_in_round') == r

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Reset the trigger
        player.participant.vars['trigger_empty_page_in_round'] = 0


# -----------------------------
# PerformanceReview
# -----------------------------
class PerformanceReview(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number in Constants.REVIEW_ROUNDS

    @staticmethod
    def vars_for_template(player):
        period_num = get_period_num(player.round_number)
        period_net_perf = calculate_review_period_performance(player)
        period_trials = get_trial_range_for_period(period_num)  # Das ist z.B. range(7, 13)
        p_vars = player.participant.vars
        review_data = p_vars.get('review_data', {})

        # Wir bestimmen den ersten Trial dieser Periode, um davon abzuziehen
        # Falls period_trials leer ist, nehmen wir 0
        start_trial_of_period = min(period_trials) if period_trials else 0

        show_refresh_penalty_column = False
        table_rows = []

        for trial_index in period_trials:
            data = review_data.get(trial_index)

            if data and data.get('value') is not None:
                penalty_value = data.get('refresh_penalty', 0.0)
                if float(penalty_value) > 0:
                    show_refresh_penalty_column = True

                # HIER BERECHNEN WIR DIE RELATIVE RUNDE:
                # Beispiel: Trial 7 (Index) - Start 7 + 1 = Runde 1
                relative_round_num = trial_index - start_trial_of_period + 1

                table_rows.append({
                    'round': relative_round_num,  # Wir schicken die relative Nummer ans HTML
                    'value': data.get('value'),
                    'reveals': data.get('reveals'),
                    'num_revisits': data.get('num_revisits'),
                    'refresh_penalty': penalty_value,
                    'net_perf': data.get('net_perf'),
                })

        return dict(
            period_num=period_num,
            period_net_perf=period_net_perf,
            table_rows=table_rows,
            show_refresh_penalty_column=show_refresh_penalty_column,
        )


# -----------------------------
# FinalReview
# -----------------------------
class FinalReview(Page):

    @staticmethod
    def vars_for_template(player):
        # collect net performance for all periods
        period_data = []

        for i in range(1, 7):  # Periods 1 to 5
            net_perf = calculate_final_period_performance(player, i)

            period_data.append({
                'period_num': i,
                'net_perf': f"{net_perf:.2f}"  # round to 2 decimals
            })

        total_score = sum(
            calculate_final_period_performance(player, i)
            for i in range(1, 7)
        )

        return dict(
            period_data=period_data,
            total_score=f"{total_score:.2f}",
        )

    @staticmethod
    def is_displayed(player):
        # show FinalReview only in the second to last round (before Thankyou page)
        return player.round_number == Constants.num_rounds - 1


class ActionPlanInput(Page):
    form_model = 'player'
    form_fields = ['action_plan_suggestions']

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds - 1


# -----------------------------
# ThankYou
# -----------------------------
class ThankYou(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds


page_sequence = [
    PerformanceReview,
    TrainingOffer,
    TrainingGate,
    EmptyPage,
    Reveal,
    FinalReview,
    ActionPlanInput,
]


def custom_export(players):
    yield [
        'participant_code',
        'round_number',
        'action_plan_suggestions',
    ]

    for p in players:
        if p.action_plan_suggestions:
            yield [
                p.participant.code,
                p.round_number,
                p.action_plan_suggestions,
            ]