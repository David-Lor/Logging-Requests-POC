from random import randint
import requests

if __name__ == '__main__':
    body = {
        "username": f"Agent warn {randint(1, 1000)}"
    }
    headers = {
        "Content-Type": "application/json"
    }

    requests.post("http://localhost:5000/users", json=body, headers=headers)
