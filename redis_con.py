import os
import redis
import requests, json
from flask import jsonify, Flask, make_response

def get_from_redis(*,host_ip=None,redis_host=None):

    try:
        redis_con = redis.Redis(host=redis_host, port=redis_port)
        cached_data = redis_con.get(host_ip)
        if cached_data:
            output = json.load(cached_data)
            output["cached_data"] = True
            output["api_server"] = hostname
            return output
        else:
            return set_to_redis(host_ip=host_ip,redis_host=redis_host,api_key=api_key)
    except:
        return "Error In get_from_redis function."        


def set_to_redis(*,host_ip=None,redis_host=None,api_key=None):
    try:

        redis_con = redis.Redis(host=redis_host, port=redis_port)
        ipgeolocation_api = 'https://api.ipgeolocation.io/ipgeo?apiKey={}&ip={}'.format(api_key,host_ip)
        api_data = requests.get(url = ipgeolocation_api).json()
        api_data["cached"] = "False"
        api_data["api_server"] = hostname
        redis_con.set(host_ip,json.dumps(api_data) )
        output = redis_con.get(host_ip)
        redis_con.expire(host_ip,3600)
        
        return output
    except:
        return "Error In set_to_redis function."   



app = Flask(__name__)
@app.route('/ip/<ip>',strict_slashes=False)
def ipGetData(ip=None):
    output = get_from_redis(host_ip=ip,redis_host=redis_host)
    return jsonify(output)
@app.route('/status',strict_slashes=False)
def status():
    return make_response(jsonify(message = "Health check success!!"),200)    



if __name__ == "__main__":
    hostname = os.getenv("HOSTNAME",None)
    #api_key = os.getenv("API_KEY",None)
    api_key = "0d801ba530ff4c1e82a270c2b97d4d3b" 
    #redis_host = os.getenv("REDIS_HOST",None)
    redis_host = '172.18.0.2'
    redis_port = os.getenv("REDIS_PORT",'6379')
    app_port = os.getenv("APP_PORT",'8080')
    api_key = os.getenv("API_KEY",None)
    
    app.run(port = app_port,host='0.0.0.0',debug=True )










