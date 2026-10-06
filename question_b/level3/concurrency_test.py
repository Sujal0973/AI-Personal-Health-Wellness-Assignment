import concurrent.futures
import time

import requests


API_URL = "http://127.0.0.1:8000/predict"
CONCURRENT_USERS = 100

PATIENT = {
    "age": 40,
    "anaemia": 0,
    "creatinine_phosphokinase": 150,
    "diabetes": 0,
    "ejection_fraction": 60,
    "high_blood_pressure": 0,
    "platelets": 300000,
    "serum_creatinine": 0.9,
    "serum_sodium": 140,
    "sex": 1,
    "smoking": 0,
}


def send_request(request_number):
    start = time.perf_counter()

    try:
        response = requests.post(
            API_URL,
            json=PATIENT,
            timeout=30,
        )

        elapsed = time.perf_counter() - start

        return {
            "request": request_number,
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "time": elapsed,
        }

    except Exception as error:
        elapsed = time.perf_counter() - start

        return {
            "request": request_number,
            "status_code": None,
            "success": False,
            "time": elapsed,
            "error": str(error),
        }


def main():
    print(f"Starting {CONCURRENT_USERS} concurrent requests...")

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=CONCURRENT_USERS
    ) as executor:
        results = list(
            executor.map(
                send_request,
                range(1, CONCURRENT_USERS + 1),
            )
        )

    total_time = time.perf_counter() - start

    successful = sum(result["success"] for result in results)
    failed = CONCURRENT_USERS - successful

    response_times = [
        result["time"]
        for result in results
        if result["success"]
    ]

    print("\n--- Concurrency Test Results ---")
    print(f"Requests sent : {CONCURRENT_USERS}")
    print(f"Successful    : {successful}")
    print(f"Failed        : {failed}")
    print(f"Total time    : {total_time:.3f} seconds")

    if response_times:
        print(f"Fastest       : {min(response_times):.3f} seconds")
        print(f"Slowest       : {max(response_times):.3f} seconds")
        print(
            f"Average       : "
            f"{sum(response_times) / len(response_times):.3f} seconds"
        )

    if failed:
        print("\nFailed requests:")
        for result in results:
            if not result["success"]:
                print(result)


if __name__ == "__main__":
    main()