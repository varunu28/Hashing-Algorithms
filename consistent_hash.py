import sys
import requests
import CsvReader
import hashlib


class ConsistentHash:

    node_hash = list()
    node_hash_map = dict()
    nodes = ['5000', '5001', '5002', '5003']
    BASE_URL = " http://localhost:{}/api/v1/entries"
    records = list()

    def send_requests(self, record_list):
        count = 0

        for record in record_list:
            hash_code = self.get_hash_value(str(record.year) + record.cause_name + record.state)
            hash_value = (hash_code % 3600)/10
            payload = {str(hash_code): str(record.return_record())}

            node_id = -1

            for hash_val in self.node_hash:
                if hash_value < hash_val:
                    node_id = self.node_hash_map[hash_val]
                    break

            if node_id == -1:
                node_id = self.node_hash_map[self.node_hash[0]]

            requests.post(self.BASE_URL.format(str(node_id)), json=payload)
            count += 1

    def get_hash_value(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def get_requests(self):
        for node in self.nodes:
            print("GET http://localhost:{}".format(str(node)))
            r = requests.get(self.BASE_URL.format(str(node)))
            print(r.text + "\n")

    def perform_node_hash(self):
        for node in self.nodes:
            hash_val = (self.get_hash_value(node) % 3600)/10
            self.node_hash.append(hash_val)
            self.node_hash_map[hash_val] = node
        self.node_hash.sort()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Please run the program with a filename")
        sys.exit()

    filename = sys.argv[1]
    csv_reader = CsvReader.CsvReader()

    records = csv_reader.read_csv(filename)

    consistent_hash = ConsistentHash()

    consistent_hash.perform_node_hash()

    consistent_hash.send_requests(records)
    print("Uploaded all {} entries.".format(len(records)))
    print("Verifying the data")

    consistent_hash.get_requests()
