from datetime import datetime
from datetime import timedelta


class daterangeFilter:

    def __init__(self, query):
        self.query = query

    def start(self):
        query = self.query.replace(' ', '')
        start = datetime.strptime(query.split('-', 1)[0], "%m/%d/%Y").date()
        return start

    def end(self):
        query = self.query.replace(' ', '')
        end = datetime.strptime(query.split('-', 1)[1], "%m/%d/%Y").date()
        end = end + timedelta(days=1)
        return end
