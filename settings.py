from os import environ

SESSION_CONFIGS = [
    dict(
        name='employee_task',
        display_name="Employee Task",
        num_demo_participants=1,
        app_sequence=['instructions','employee_task','peq'],
    ),
    dict(
        name='employee_task_experiment',
        display_name="Employee Task (no intro)",
        num_demo_participants=1,
        app_sequence=['employee_task', 'peq'],
    ),
    dict(
        name='employee_task_PEQ',
        display_name="Employee Task PEQ",
        num_demo_participants=1,
        app_sequence=['peq'],
    ),

]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0,
    participation_fee=0.0,
    doc="",
)

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
        use_secure_urls=True
    ),
    dict(
        name='econ_lab',
        display_name='Experimental Economics Lab'
    ),
]
# Security stuff
SECRET_KEY = 'irgendwas_einzigartiges_12345'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')

# oTree Apps
INSTALLED_APPS = ['employee_task']

ROOT_URLCONF = 'employee_task.urls'

PARTICIPANT_FIELDS = [
    # for correct controll of trials
    'current_trial_index',

    # flags to skip rounds if training is take
    'skip_trials_11_12',
    'wants_training_r16',
    'wants_training_r22',

    # track, which trainings were taken
    'training_1_taken',
    'training_2_taken',
    'training_3_taken',
]

SESSION_EXPORT_FIELDS = [
    'participant.id_in_session',
    'participant.code',
    'player.id_in_group',
    'player.selected_option',
    'player.revealed_fields',
    'player.num_revealed_fields',
    'player.trial_net_performance',
    'player.wants_training',
    'subsession.round_number',
]