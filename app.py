import sys

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

record = list()


class Server(Resource):
    def get(self):
        return {"num_entries": len(record),
                "entries": record}

    def post(self):
        record.append(request.get_json())
        return "201 Created"


api.add_resource(Server, "/api/v1/entries")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please run the server with a port number")
        sys.exit()

    port = sys.argv[1]

    app.run(debug=True, port=port)
