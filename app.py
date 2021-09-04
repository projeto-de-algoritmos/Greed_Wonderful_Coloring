from flask import Flask, request, jsonify
from redis import Redis
from flask_restful import Resource, Api
from wonderful import get_wonderful_colors

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
api = Api(app)

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

class Colors(Resource):
    def get(self):
        return jsonify({"colors":  list(map(lambda x: x.decode('utf-8'), 
        redis.lrange('colors', 0, -1)))})

    def post(self):
        data = request.get_json()
        colors = data['colors']
        for c in colors:
            redis.rpush('colors', c)
        return data
    
    def delete(self):
        redis.delete('colors')

class Wonderful(Resource):
    def get(self):
        colors = list(map(lambda x: x.decode('utf-8'), redis.lrange('colors', 0, -1)))
        sequence = list(map(lambda x: int(x.decode('utf-8')), redis.lrange('sequence', 0, -1)))
        
        
        if len(sequence) == 0:
            return "Sequence is empty", 404
        
        if len(colors) == 0:
            print("colors is empty")
            return "Colors is empty", 404

        res = get_wonderful_colors(sequence, colors)
        
        return jsonify({"wonderful_colors": res})


api.add_resource(Sequence, '/sequence')
api.add_resource(Colors, '/colors')
api.add_resource(Wonderful, '/wonderful-colors')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)