import db_tools as tools
import dotenv, sqlite3, pathlib, requests
from os import getenv
from flask import Flask, request
from operator import itemgetter
from flask_restful import Resource, Api

HOME = pathlib.Path(__file__).parent.absolute()
dotenv.load_dotenv(HOME/'.env')

db = sqlite3.connect(HOME/'test.db')

app = Flask(__name__)
api = Api(app)

def get_url_data(url:str):
    print('started')
    resp = requests.post(f'https://www.klazify.com/api/categorize?url={url}',headers={'Authorization':f'Bearer {getenv("KTOKEN")}','User-Agent':'telnet'})
    print(resp)
    data = resp.json()
    print(data)
    return dict(
        logo=data["domain"]["logo_url"],
        category=data["domain"]["categories"][0]["name"],
    )


class TodoSimple(Resource):
    def get(self, name):
        return {}

    def put(self, name):
        name,url,time,co2 = (request.form[n] for n in ["name","url","timestamp","co2_emissions"])
        data = get_url_data(url)
        print(name,time,url,data["category"],co2,data["logo"])
        # tools.update_row(name,time,url,data["category"],co2,data["logo"])
        return {}

api.add_resource(TodoSimple, '/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)