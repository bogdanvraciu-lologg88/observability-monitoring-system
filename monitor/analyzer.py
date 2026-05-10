from monitor.history import get_service_history
from monitor.alert_engine import create_alert


def analyze_result(result, service, baseline_response_time=None):
    alerts = []

    # Service DOWN
    if not result["success"]:
        alerts.append(
            create_alert(
                "critical",
                f"{result['service']} is DOWN",
                "Check network connectivity or service availability"
            )
        )

        return alerts

    response_time = result["response_time"]

    # Static threshold alert
    if response_time > service["max_response_time"]:
        alerts.append(
            create_alert(
                "warning",
                f"{result['service']} response time is high ({response_time}s)",
                "Investigate possible latency or backend performance issues"
            )
        )

    # Historical anomaly detection
    history = get_service_history(result["service"])

    if len(history) >= 3:
        response_times = [entry["response_time"] for entry in history]

        average_response = sum(response_times) / len(response_times)

        print(f"Average response: {average_response}")
        print(f"Current response: {response_time}")

        if response_time > average_response * 1.2:
            alerts.append(
                create_alert(
                    "warning",
                    "Anomaly detected: response time increased significantly",
                    "Investigate sudden latency spikes or infrastructure problems"
                )
            )

    # Baseline comparison logic
    if (
        baseline_response_time
        and not service.get("baseline", False)
    ):

        print(f"Baseline response: {baseline_response_time}")

        # Dacă serviciul este mult mai lent decât baseline-ul
        if response_time > baseline_response_time * 3:

            alerts.append(
                create_alert(
                    "warning",
                    f"{result['service']} latency is significantly higher than baseline",
                    "Possible service-specific latency anomaly detected"
                )
            )

    return alerts