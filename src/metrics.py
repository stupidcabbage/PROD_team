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

counter_definitions = {
    'buisness_card': 'Clicked Buisness Card for organizations',
    'individual_card_count': 'Clicked Buisness Card for organizations',
    'online_bank_small': 'Clicked Online Bank for small business',
    'online_bank_middle': 'Clicked Online Bank for middle business',
    'buisness_credit': 'Clicked credit for business',
    'accounting': 'Clicked accounting for business',
    'payment': 'Clicked payment handling for business',
}

product_counters = {}
for name, description in counter_definitions.items():
    product_counters[name] = prometheus_client.Counter(name, description)
