import json

def save_call_data(data, customer_id):
    filename = f"call_{customer_id}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved call to {filename}")
