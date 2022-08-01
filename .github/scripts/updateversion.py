import sys
import json
import pathlib
import os

def main():
    print(f"Running main() in updateversion.py with argument {sys.argv[1]}")
    
    year, month, day = sys.argv[1].split('.')

    root_folder = [p for p in pathlib.Path(__file__).parents if p.name == 'pyscript'][0]
    print(root_folder)
    print(os.listdir(root_folder))
    version_file =  root_folder / 'pyscriptjs' / 'src' / 'version_info.json'
    print(version_file)

    with open(version_file, 'r') as fp:
        version_data = json.load(fp)
    
    version_data['year'] = int(year)
    version_data['month'] = int(month)
    version_data['day'] = int(day)

    print(f"After update, {version_data= }")

    with open(version_file, 'w') as fp:
        json.dump(version_data, fp, indent=2)

if __name__ == '__main__':
    main()