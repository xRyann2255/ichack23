import db_tools as tools
import pytricia
import dotenv, sqlite3, pathlib, requests, json
from os import getenv
from flask import Flask, request
from operator import itemgetter
from flask_restful import Resource, Api

HOME = pathlib.Path(__file__).parent.absolute()
dotenv.load_dotenv(HOME/'.env')

db = sqlite3.connect(HOME/'test.db')

app = Flask(__name__)
api = Api(app)

pyt = pytricia.PyTricia()
t_addr = t_gigs = 0
for ip,co2 in json.load(open(HOME/'../assets/all-ranges.json')).items():
    pyt[ip] = co2
    n = 1 << int(ip.rsplit('/',1)[-1])
    t_addr += (co2 or 0)  * n
    t_gigs += n
avg = t_addr / t_gigs
print(avg)

# print(pyt.get('3.2.34.1'))

def get_url_data(url:str):
    # print('started')
    resp = requests.post(f'https://www.klazify.com/api/categorize?url={url}',headers={'Authorization':f'Bearer {getenv("KTOKEN")}','User-Agent':'carbonara_api'})
    # print(resp)
    data = resp.json()
    print(f"{data = }")
    return (
        data["domain"]["logo_url"],
        data["domain"]["categories"][0]["IAB12"],
    )


class Rest(Resource):
    def get(self, name):
        return {"":tools.get_websites(name)}

    def put(self, name):
        print(request.json)
        data = request.json["hosts"]
        co2 = sum((pyt.get(d["ip"]) or avg)*d["transferred"] for d in data.values()) # fix ratio :/
        url,time = request.json["url"],request.json["timestamp"]
        logo,category = get_url_data(url)
        print(name,time,url,category,co2,logo)
        # tools.update_row(name,time,url,category,co2,logo)
        return {}

api.add_resource(Rest, '/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)