import redis

def set_customer_details(redis_client, customer_id, details):
    for field, value in details.items():
        redis_client.hset(f"customer:{customer_id}", field, value)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('foo','bar')

# Customer data
# customer_id = "1001"
# customer_data = {
#     "username": "Yasin",
# }

# # Setting the customer details
# set_customer_details(r, customer_id, customer_data)

# # Retrieve and print all fields for the customer
# customer_info = r.hgetall(f"customer:{customer_id}")
print(r.get('foo'))



