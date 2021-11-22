
import json


def read_from_json(data_path):
    with open(data_path) as f:
        json_data = json.load(f)
    return json_data


def main():
    res = read_from_json('./persons.json')


if __name__ == '__main__':
    main()
