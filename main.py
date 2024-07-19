# hook
from hook.saveVoice import SaveVoiceAPI

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
CORS(app)  # client와 server가 동일 선상에 있을 때는 없어도 됨.
api = Api(app)

api.add_resource(SaveVoiceAPI,'/saveVoice')

def main():
   app.run(debug=True, port=5000, host='0.0.0.0')


if __name__ == '__main__':
   main()




