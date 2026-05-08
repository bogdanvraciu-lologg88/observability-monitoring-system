import yaml

from monitor.collector import check_service
from monitor.analyzer import analyze_result
from monitor.notifier import send_telegram_alert
from monitor.history import save_result


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


services = config["services"]
telegram_enabled = config["alerting"]["telegram_enabled"]


for service in services:
    result = check_service(service)

    alerts = analyze_result(result, service)

    save_result(result)

    print("\n====================")
    print(f"Service: {result['service']}")

    if result["success"]:
        print(f"Response Time: {result['response_time']}s")

        info_message = f"""
[INFO]

Service: {result['service']}
Response Time: {result['response_time']}s
"""

    else:
        print(f"ERROR: {result['error']}")

        info_message = f"""
[ERROR]

Service: {result['service']}
Error: {result['error']}
"""

    if telegram_enabled:
        send_telegram_alert(info_message, config)

    if alerts:
        print("\nALERTS:")

        for alert in alerts:
            alert_message = f"""
[{alert['severity'].upper()}]

Service: {result['service']}
Message: {alert['message']}
Recommendation: {alert['recommendation']}
"""

            if telegram_enabled:
                print("Sending Telegram alert...")
                send_telegram_alert(alert_message, config)