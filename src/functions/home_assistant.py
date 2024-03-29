import requests

home_assistant_url = "HOME_ASSISTANT_URL"
access_token = "ACCESS_TOKEN"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


def ha_turn_on_light(entity_id):

    service_endpoint = f"{home_assistant_url}/api/services/light/turn_on"

    data = {
        "entity_id": entity_id
    }

    response = requests.post(service_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False

def ha_turn_off_light(entity_id):

    service_endpoint = f"{home_assistant_url}/api/services/light/turn_off"

    data = {
        "entity_id": entity_id
    }

    response = requests.post(service_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False

def ha_change_light_color(entity_id, r, g, b):
    service_endpoint = f"{home_assistant_url}/api/services/light/turn_on"

    data = {
        "entity_id": entity_id,
        "rgb_color": [r, g, b]
    }

    response = requests.post(service_endpoint, json=data, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False
    
