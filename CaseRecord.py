class CaseRecordObj:
    def __init__(self, year, cause_name_113, cause_name, state, deaths, death_rate):
        self.year = year
        self.cause_name_113 = cause_name_113
        self.cause_name = cause_name
        self.state = state
        self.deaths = deaths
        self.death_rate = death_rate

    def return_record(self):
        return ",".join({str(self.year), self.cause_name_113, self.cause_name, self.state, str(self.deaths), str(self.death_rate)})
