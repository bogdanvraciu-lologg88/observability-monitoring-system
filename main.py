import yaml
from monitor.collector import check_service


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


services = config["services"]

for service in services:
    result = check_service(service)

    print("\n===================")
    print(f"Service: {result['service']}")

    if result["success"]:
        print(f"Status: {result['status_code']}")
        print(f"Response Time: {result['response_time']}s")
    else:
        print(f"ERROR: {result['error']}")