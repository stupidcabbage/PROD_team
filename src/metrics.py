from datetime import datetime
from config import NUMBER_OF_AGENTS
import prometheus_client


meetings_count = prometheus_client.Counter(
    'meetings_count', 'Number of meetings'
)

canceled_meetings_count = prometheus_client.Counter(
    'canceled_meetings_count', 'Number of canceled meetings')

product_counter_mapping = {
    1: 'buisness_card',
    2: 'individual_card_count',
    3: 'online_bank_small',
    4: 'online_bank_middle',
    5: 'buisness_credit',
    6: 'buisness_credit',
    7: 'accounting',
    8: 'payment',
    9: 'accounting',
}

product_counter_definitions = {
    'buisness_card': 'Clicked Buisness Card for organizations',
    'individual_card_count': 'Clicked Buisness Card for organizations',
    'online_bank_small': 'Clicked Online Bank for small business',
    'online_bank_middle': 'Clicked Online Bank for middle business',
    'buisness_credit': 'Clicked credit for business',
    'accounting': 'Clicked accounting for business',
    'payment': 'Clicked payment handling for business',
}

product_counters = {}
for name, description in product_counter_definitions.items():
    product_counters[name] = prometheus_client.Counter(name, description)

weekday_counter = prometheus_client.Counter(
    'week_day', 'Day of week of meeting')

weekday_definitions = {
    'mon_counter': '',
    'tue_counter': '',
    'wed_counter': '',
    'thu_counter': '',
    'fri_counter': '',
    'sat_counter': '',
    'sun_counter': '',
}

weekday_mapping = {
    0: 'mon_counter',
    1: 'tue_counter',
    2: 'wed_counter',
    3: 'thu_counter',
    4: 'fri_counter',
    5: 'sat_counter',
    6: 'sun_counter',
}

weekday_counters = {}
for name, description in weekday_definitions.items():
    weekday_counters[name] = prometheus_client.Counter(name, description)


def inc_day_of_week(date: datetime):
    day = date.weekday()
    weekday_counters[weekday_mapping[day]].inc(1)


morning_counter = prometheus_client.Counter('morning_couter', '')
late_morning_counter = prometheus_client.Counter('late_morning_counter', '')
day_counter = prometheus_client.Counter('day_counter', '')
late_day_counter = prometheus_client.Counter('late_day_counter', '')
evening_counter = prometheus_client.Counter('evening_counter', '')


def inc_time_of_day(date: datetime):
    hour = date.hour

    if 8 < hour < 12:
        morning_counter.inc(1)
    elif 12 < hour < 14:
        late_morning_counter.inc(1)
    elif 14 < hour < 16:
        day_counter.inc(1)
    elif 16 < hour < 19:
        late_day_counter.inc(1)
    elif 19 < hour < 20:
        evening_counter.inc(1)


agents_mapping = {}
agents_counter = {}

for agent_id in range(1, NUMBER_OF_AGENTS + 1):
    name = f'agent_{agent_id}'
    agents_counter[name] = prometheus_client.Counter(name, '')
    agents_mapping[agent_id] = name


def inc_agent_id(id: int):
    agents_counter[agents_mapping[id]].inc(1)
