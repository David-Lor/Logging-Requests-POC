import requests

if __name__ == '__main__':
    body = {
        "username": "User that fails"
    }
    headers = {
        "Content-Type": "application/json"
    }

    requests.post("http://localhost:5000/users", json=body, headers=headers)
