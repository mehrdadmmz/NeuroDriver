import json

# The Storage class is a simple class that writes the chromosomes to a JSON file.
class Storage:
    def __init__(self, filename):
        self.filename = filename

    def save(self, chromosomes):
        with open(self.filename, 'w') as file:
            json.dump({"chromosomes": chromosomes}, file)  # serialize the chromosomes to a json file

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return data["chromosomes"]
        except Exception as e:  # something went wrong while loading the file, return an empty list
            print(f"Error loading file: {e}")
            return []

