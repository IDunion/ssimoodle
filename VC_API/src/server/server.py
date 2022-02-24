import json
from datetime import datetime
from flask import Flask, Response, request, jsonify
from flasgger import Swagger
from functools import wraps

from globalSettings import Settings

class Server:
    app = Flask(__name__)
    
    # Start server
    def run(self):
        # import controller
        import server.controller.agent_controller
        import server.controller.credential_controller

        # init swagger
        swagger_template = {"securityDefinitions": {"APIKeyHeader": {"type": "apiKey", "name": "x-auth-token", "in": "header"}}}
        Swagger(self.app, template=swagger_template)

        self.app.run(host=Settings.serverAddress, port=Settings.serverPort)

    ##### Wrapper #####
    # Check auth Token
    def token_required(f):
        """Checks if request contains the correct x-auth-token"""
        @wraps(f)
        def decorated(*args, **kwargs):
            #token passed in the request header
            if 'x-auth-token' in request.headers:
                token = request.headers['x-auth-token']
                if token == Settings.authToken:
                    return f(*args, **kwargs)
            # return 401 if token is not passed
            return jsonify({'message' : 'x-auth-token is missing or wrong!'}), 401
    
        return decorated

    # Serilize class to json
    def returns_json(f):
        """Serialize the object to a json and adds the json to the response"""
        @wraps(f)
        def decorated(*args, **kwargs):
            r = f(*args, **kwargs)
            if not r:
                return Response("{}", content_type='application/json; charset=utf-8')

            if type(r) == list:
                response = json.dumps([json.loads(Server.to_json_str(object)) for object in r])
                return Response(response, content_type='application/json; charset=utf-8')
            else:
                response = Server.to_json_str(r)
                return Response(response, content_type='application/json; charset=utf-8')

        return decorated    

    # Only accept json
    def contentType_json(f):
        """Checks if the request body is content-type application/json"""
        @wraps(f)
        def decorated(*args, **kwargs):
            content_type = request.headers.get('Content-Type')
            if (content_type != 'application/json'):
                return 'Content-Type not supported! Requires application/json', 415
            else:
                return f(*args, **kwargs)

        return decorated
    
    ##### Methods #####
    # json converter for serialization
    def to_json_str(inst):
        jsonObj = { c.name: getattr(inst, c.name) for c in inst.__table__.columns }
        lambdaObj = lambda obj: obj.isoformat() if type(obj) == datetime else TypeError
        return json.dumps(jsonObj, default= lambdaObj)

    ##### Controler #####
    # Simple status controler
    @app.route('/', methods=['GET'])
    def home():
        return "<h1>Online</h1>"