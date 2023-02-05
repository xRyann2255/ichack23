import db_tools as tools
from datetime import datetime
import flask_cors
import pytricia
import dotenv, sqlite3, pathlib, requests, json
from os import getenv
from flask import Flask, request
from operator import itemgetter
from flask_restful import Resource, Api

HOME = pathlib.Path(__file__).parent.absolute()
dotenv.load_dotenv(HOME / ".env")

db = sqlite3.connect(HOME / "test.db")

app = Flask(__name__)
flask_cors.CORS(app)
api = Api(app)

pyt_4 = pytricia.PyTricia()
t_addr = t_gigs = 0
for ip, co2 in json.load(open(HOME / "../assets/all-ranges.json")).items():
    pyt_4[ip] = co2
    n = 1 << int(ip.rsplit("/", 1)[-1])
    if co2 is not None:
        t_addr += co2 * n
        t_gigs += n
avg_4 = t_addr / t_gigs
print(avg_4)

pyt_6 = pytricia.PyTricia(128)
t_addr = t_gigs = 0
for ip, co2 in json.load(open(HOME / "../assets/v6-ranges.json")).items():
    pyt_6[ip] = co2
    n = 1 << int(ip.rsplit("/", 1)[-1])
    if co2 is not None:
        t_addr += co2 * n
        t_gigs += n
avg_6 = t_addr / t_gigs
print(avg_6)

pyt_cpu4 = pytricia.PyTricia()
t_addr = t_gigs = 0
for ip, co2 in json.load(open(HOME / "../assets/all-ranges.json")).items():
    pyt_cpu4[ip] = co2
    n = 1 << int(ip.rsplit("/", 1)[-1])
    if co2 is not None:
        t_addr += co2 * n
        t_gigs += n
avg_cpu4 = t_addr / t_gigs
print(avg_cpu4)

pyt_cpu6 = pytricia.PyTricia(128)
t_addr = t_gigs = 0
for ip, co2 in json.load(open(HOME / "../assets/v6-ranges.json")).items():
    pyt_cpu6[ip] = co2
    n = 1 << int(ip.rsplit("/", 1)[-1])
    if co2 is not None:
        t_addr += co2 * n
        t_gigs += n
avg_cpu6 = t_addr / t_gigs
print(avg_cpu6)

# print(pyt.get('3.2.34.1'))


def get_url_data(url: str):
    # print('started')
    resp = requests.post(
        f"https://www.klazify.com/api/categorize?url=https://{url}",
        headers={
            "Authorization": f'Bearer {getenv("KTOKEN")}',
            "User-Agent": "carbonara_api",
        },
    )
    print(url)
    print(resp.text)
    data = resp.json()
    print(f"{data = }")
    if "domain" not in data: return (None, None)
    return (
        data["domain"]["logo_url"],
        data["domain"]["categories"][0]["name"][1:].replace("/", " ")
    )


def get_co2(ip: str):
    return pyt_6.get(ip) or avg_6 if ":" in ip else pyt_4.get(ip) or avg_4

def get_cpu(ip: str):
    return pyt_cpu6.get(ip) or avg_cpu6 if ":" in ip else pyt_cpu4.get(ip) or avg_cpu4

class Rest(Resource):
    def get(self, name):
        if not tools.validate(name, request.args["password"]):
            return
        return tools.getCategories(name)

    def post(self, name):
        body = json.loads(request.data)
        print(body)
        if not tools.validate(name, body["password"]):
            return
        hosts = body["hosts"]
        print(hosts)

        for url, data in hosts.items():
            co2 = sum(
                get_co2(d["ip"]) * d["transfer_size"] / 1e6 for d in data.values()
            ) + sum(
                get_cpu(d["ip"]) * d["duration"] / 3.6e6 for d in data.values()
            )
            
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logo, category = get_url_data(url)
            tools.update_row(name, time, url, category, co2, logo)
        return {}


class Leaderboard(Resource):
    def get(self, name):
        if not tools.validate(name, request.args["password"]):
            return
        return tools.leaderboard(name, request.args.get("type", "friends"))


class Friends(Resource):
    def get(self, name):
        if not tools.validate(name, request.args["password"]):
            return
        print("friends, do we have those?")
        return tools.addRelation(name, request.args["other"], "friends")


class Graph(Resource):
    def get(self, name):
        if not tools.validate(name, request.args["password"]):
            return
        print("friends, do we have those?")
        return tools.loadGraph(name)


class Auth(Resource):
    def get(self):
        res = tools.validate(request.args["username"], request.args["password"])
        print(res)
        return res, 200 if res else 403  # an utter crime

    def post(self):
        # check user in db?
        print("Thanks for calling, I aws so lonely")
        data = json.loads(request.data)
        print(data)
        print(data["username"], data["password"])
        tools.register(data["username"], data["password"])

        return {}


# @app.before_request
# def before_req():
#     print(request.method)


api.add_resource(Auth, "/login")
api.add_resource(Leaderboard, "/leaderboard/<string:name>")
api.add_resource(Friends, "/friends/<string:name>")
api.add_resource(Graph, "/graph/<string:name>")
api.add_resource(Rest, "/api/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
