import json

# Replace 'evaluation.json' with the path to your file if it's different
evaluation_file_path = '../data/evaluation_results_20240312-171029.json'


def read_evaluation_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def print_items_with_invalid_syntax(data):
    for item in data:  # As data is a list, we can iterate directly
        if not item.get('fine-tuned-gpt-3.5', {}).get('valid_syntax', True):
            print(item['fine-tuned-gpt-3.5']["diagram"])

def main():
    try:
        data = read_evaluation_file(evaluation_file_path)
        print_items_with_invalid_syntax(data)
    except FileNotFoundError:
        print(f"File not found: {evaluation_file_path}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from the file. Please check the file format.")

if __name__ == "__main__":
    main()
