def load_key_from_file(file_path: str):
    try:
        with open(file_path, "rb") as f:
            loaded_key = f.read()
        return loaded_key
    except Exception as e:
        return None