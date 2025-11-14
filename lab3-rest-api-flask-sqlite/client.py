import requests

API = "http://127.0.0.1:5000"

def get_token(username, password):
    r = requests.post(f"{API}/token", json={
        "username": username,
        "password": password
    })
    return r.json().get("token")

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def get_items(token):
    return requests.get(f"{API}/items", headers=auth_headers(token)).json()

def add_item(token, item):
    return requests.post(f"{API}/items", json=item, headers=auth_headers(token)).json()

def update_item(token, item_id, item):
    return requests.put(f"{API}/items/{item_id}", json=item, headers=auth_headers(token)).json()

def delete_item(token, item_id):
    return requests.delete(f"{API}/items/{item_id}", headers=auth_headers(token)).json()

if __name__ == "__main__":
    token = get_token("admin", "1234")
    print("TOKEN:", token)

    print("\nADD ITEM:")
    print(add_item(token, {"id": 10, "name": "Arabica", "price": 100.25}))

    print("\nALL ITEMS:")
    print(get_items(token))

    print("\nUPDATE ITEM:")
    print(update_item(token, 10, {"name": "Arabica Premium", "price": 129.99}))

    print("\nDELETE ITEM:")
    print(delete_item(token, 10))
