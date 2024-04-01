def get_client(user_id: int):
    if user_id == 1:
        return {'name': 'Ivanov Ivan Tinkoffovich',
                'phone': '+79850000000',
                'type': 'ИП',
                'company': 'Tails And Nails',
                'employees': [{'name': 'Dimitriy Dimitrievich Prodov', 'job': 'Clerk'},
                            {'name': 'John Doe Doevich', 'job': 'Secretary'}]
                }
    return {'name': 'Ivanov Ivan Tinkoffovich',
            'phone': '+79850000000',
            'type': 'ООО',
            'company': 'Tails And Nails',
            'employees': [{'name': 'Dimitriy Dimitrievich Prodov', 'job': 'Clerk'},
                        {'name': 'John Doe Doevich', 'job': 'Secretary'}]
            }
