from datetime import datetime

class Refugee(object):
    def __init__(self, refugee_id: int, name: str, date: datetime):
        self.id = refugee_id
        self.name = name
        self.date = date
