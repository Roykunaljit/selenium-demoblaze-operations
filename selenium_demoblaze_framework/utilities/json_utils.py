# utilities/json_utils.py

import json
import os


class JSONUtils:
    @staticmethod
    def read_json_data(file_path):
        """
        Read data from a JSON file.
        Returns the parsed JSON content as a Python object (dict, list, etc.).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def write_json_data(file_path, data):
        """
        Write data to a JSON file with pretty formatting (indent=4).
        Creates parent directories if they don't exist.
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def update_json_value(file_path, key_path, new_value):
        """
        Update a nested value in a JSON file using dot notation (e.g., 'user.profile.name').
        Parameters:
            file_path (str): Path to the JSON file.
            key_path (str): Dot-separated key path (e.g., 'auth.username').
            new_value: The new value to assign.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        data = JSONUtils.read_json_data(file_path)

        keys = key_path.split('.')
        current = data

        # Traverse to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                raise KeyError(f"Key path '{key}' not found in JSON structure.")
            current = current[key]

        # Update the final key
        final_key = keys[-1]
        if final_key not in current:
            raise KeyError(f"Final key '{final_key}' not found in JSON structure.")

        current[final_key] = new_value

        # Write updated data back to file
        JSONUtils.write_json_data(file_path, data)