from src.star.rest.client import test_rest_client
from src.utilities.colors import print_yellow


print_yellow("Testing client using RestAPI...")
result = test_rest_client("127.0.0.1:5000", "127.0.0.1:5002")
print(result)
