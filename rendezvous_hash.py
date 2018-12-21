import sys
import requests
import CsvReader
import hashlib

class RendezvousHash:

    nodes = ['5000', '5001', '5002', '5003']
    BASE_URL = " http://localhost:{}/api/v1/entries"
    records = list()

    def send_requests(self, record_list):
        for record in record_list:
            max_hash_value = None
            highest_node = None

            hash_value = (self.get_hash_value(str(record.year) + record.cause_name + record.state))

            for node in self.nodes:
                temp_hash = self.get_hash_value(node + str(hash_value))
                if max_hash_value is None:
                    max_hash_value = temp_hash
                    highest_node = node
                elif temp_hash > max_hash_value:
                    max_hash_value = temp_hash
                    highest_node = node

            payload = {str(hash_value): str(record.return_record())}
            requests.post(self.BASE_URL.format(highest_node), json=payload)
    
    def get_hash_value(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def get_requests(self):
        for node in self.nodes:
            print("GET http://localhost:{}".format(str(node)))
            r = requests.get(self.BASE_URL.format(str(node)))
            print(r.text + "\n")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please run the program with a filename")
        sys.exit()

    filename = sys.argv[1]
    csv_reader = CsvReader.CsvReader()

    records = csv_reader.read_csv(filename)

    rendezvous_hash = RendezvousHash()

    # Sending requests
    rendezvous_hash.send_requests(records)
    print("Uploaded all {} entries.".format(len(records)))
    print("Verifying the data")

    # Getting response
    rendezvous_hash.get_requests()
