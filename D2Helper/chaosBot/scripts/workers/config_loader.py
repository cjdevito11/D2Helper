import json

CONFIG_FILE = "../../config/multiload/loader_config.json"

# Default loader configuration
default_config = {
    "loaders": [
        {"name": "BO", "type": "BO", "Diablo II - BO": ""},
        {"name": "Enchant Sorc", "type": "Chant", "Diablo II - Chant": ""},
        {"name": "Summon Druid", "type": "CC", "Diablo II - CC": ""},
        {"name": "Fill 1", "type": "Fill", "Diablo II - Fill 1": ""},
        {"name": "Fill 2", "type": "Fill", "Diablo II - Fill 2": ""},
        {"name": "Fill 3", "type": "Fill", "Diablo II - Fill 3": ""},
        {"name": "Fill 4", "type": "Fill", "Diablo II - Fill 4": ""}
    ]
}

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        save_config(default_config)
        return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

if __name__ == "__main__":
    config = load_config()
    print("Current Config:")
    for loader in config["loaders"]:
        print(f"{loader['name']} - Type: {loader['type']} - Window: {loader['window_title']}")
