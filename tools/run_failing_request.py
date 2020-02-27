import requests

if __name__ == '__main__':
    body = {
        "username": "User that fails"
    }
    headers = {
        "Content-Type": "application/json"
    }

    requests.post("http://127.0.0.1:5000/users", json=body, headers=headers)
