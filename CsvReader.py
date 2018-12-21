import csv
import CaseRecord


class CsvReader:
    def __init__(self):
        self.records = list()

    def read_csv(self, filename):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file)
            count = 0
            for row in csv_reader:
                if count == 0:
                    count += 1
                    pass
                else:
                    case_record = CaseRecord.CaseRecordObj(int(row[0]), row[1], row[2], row[3], int(row[4]), float(row[5]))
                    self.records.append(case_record)

        return self.records
