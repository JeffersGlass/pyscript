import sys
import json

def main():
    print(f"Running main() in updateversion.py with argument {sys.argv[1]}")
    
    year, month, day = sys.argv[1].split('.')

    with open('version_info.json', 'r') as fp:
        version_data = json.load(fp)
    
    version_data['year'] = int(year)
    version_data['month'] = int(month)
    version_data['day'] = int(day)

    print(f"After update, {version_data= }")

    with open('version_info.json', 'w') as fp:
        json.dump(version_data, fp, indent=2)

if __name__ == '__main__':
    main()