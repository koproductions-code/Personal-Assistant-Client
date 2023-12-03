from functions.home_assistant import *
from functions.classes import FunctionResponse
import os

def get_weather(city: str):
    return FunctionResponse(True, {"success": True, "info": "Temperature: 10 degrees, Status: Rain, City: {}".format(city)})

def turn_on_light(name: str):
    result = ha_turn_on_light("light."+name.lower().replace(" ", "_"))
    return FunctionResponse(True, {"success": result, "info": ""})

def change_light_color(name: str, r: int, g: int, b: int):
    result = ha_change_light_color("light."+name.lower().replace(" ", "_"), r, g, b)
    return FunctionResponse(True, {"success": result, "info": ""})

def turn_off_light(name: str):
    result = ha_turn_off_light("light."+name.lower().replace(" ", "_"))
    return FunctionResponse(True, {"success": result, "info": ""})

def turn_on_room_lights(room: str):
    if room.lower() == "bedroom":
        result = ha_turn_on_light("light.bedroom")
        return FunctionResponse(True, {"success": result, "info": ""})
    else:
        return FunctionResponse(True, {"success": False, "info": "This room does not exist."})

def turn_off_room_lights(room: str):
    if room.lower() == "bedroom":
        result = ha_turn_off_light("light.bedroom")
        return FunctionResponse(True, {"success": result, "info": ""})
    else:
        return FunctionResponse(True, {"success": False, "info": "This room does not exist."})

def shutdown_computer():
    os.system("sleep 10 && shutdown -h now &")
    return FunctionResponse(True, {"success": True, "info": "Planned shutdown in 15 seconds. Bye."})

def lock_computer():
    os.system("dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock")
    return FunctionResponse(False, {"success": True, "info": ""})