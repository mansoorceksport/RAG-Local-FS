import os

def load_markdown_files(base_path="data/employees"):
    data = {}

    for filename in os.listdir(base_path):
        if filename.endswith(".md"):
            key = filename.replace(".md", "")
            with open(os.path.join(base_path, filename), "r") as file:
                data[key] = file.read()

    return data

if __name__ == "__main__":
    employees = load_markdown_files()
    print("Loaded employees:", list(employees.keys()))