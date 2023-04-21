import os
import redis



r = redis.Redis(host='ipgeolocation-redis', port=6379)
#r.set('8.8.8.8', 'bar#')
print(r.get('8.8.8.8'))






