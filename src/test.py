import asyncio

from schemas.meetings import MeetingAddSchema, ParticipantSchema
from db.crud.meetings import add_meeting, get_all_meetings


async def test():
    meeting_data = {
        'date': '2024-03-31T12:00:00',
        'place': {'longitude': 0.0, 'latitude': 0.0, 'name': 'Test Location'},
        'participants': [{"name": "Ваня крутой", "position": "Ген дир", "phone_number": "89123123"},
                         {"name": "Ваня не крутой", "position": "бейджик", "phone_number": "89123123"},
                         {"name": "Не ну круто!", "position": "квадрат", "phone_number": "89123123"}]
    }
    meeting_data["participants"] = [ParticipantSchema(name=i["name"], position=i["position"], phone_number=i["phone_number"]) for i in meeting_data["participants"]]
    print(meeting_data)
    print(type(meeting_data))
    meeting = MeetingAddSchema(**meeting_data)
    
    print(meeting)
    meeting = await add_meeting(0, meeting)
    print(meeting)


asyncio.run(test())
