from src.ring.rest.client import run_rest_discovery, test_rest_client
from src.utilities.colors import print_yellow


print("\n\nDiscovering servers...\n")
response = run_rest_discovery("127.0.0.1:5000")

if response.status_code == 200:
    print_yellow("Testing client using RestAPI...")
    result = test_rest_client("127.0.0.1:5000", "127.0.0.1:5002")
    print(result)
