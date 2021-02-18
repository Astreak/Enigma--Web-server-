from flask import *
from app import app

@app.route('/api')
def Data():
        A={
                "name":"Paraj",
                "Age":12
        }
        res=make_response(jsonify(A),200)
        print(res.headers)
        res.headers['Content-Type']='application/json'
        return res

