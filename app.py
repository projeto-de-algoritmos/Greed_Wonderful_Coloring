from flask import Flask, request, jsonify
from redis import Redis
from flask_restful import Resource, Api

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
api = Api(app)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

class Sequence(Resource):
    def get(self):
        return jsonify({"sequence":  list(map(lambda x: int(x.decode('utf-8')), 
        redis.lrange('sequence', 0, -1)))})

    def post(self):
        data = request.get_json()
        sequence = data['sequence']
        for e in sequence:
            print(e)
            redis.rpush('sequence', e)
        return data

    def delete(self):
        redis.delete('sequence')


api.add_resource(Sequence, '/sequence')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)