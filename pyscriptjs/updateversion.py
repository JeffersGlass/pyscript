import json
import os
import pathlib
import re
import sys


def update_version_info() -> None:

    root_folder = [
        p for p in pathlib.Path(os.getcwd()).parents if p.name == "pyscript"
    ][0]
    version_file = root_folder / "pyscriptjs" / "src" / "version_info.json"

    try:
        with open(version_file, "r") as fp:
            version_data = json.load(fp)
    except FileNotFoundError:
        version_data = {}

    # Get release level from script argument
    release_level = sys.argv[1]

    # Get git tag info from script argument
    git_data = re.split(r"[\.-]", sys.argv[2])
    print(f"{git_data= }")

    version_data["major"] = int(git_data[0])
    version_data["minor"] = int(git_data[1])
    version_data["patch"] = int(git_data[2])
    version_data["releaselevel"] = str(release_level)
    version_data["serial"] = int(git_data[3])
    version_data["commit"] = str(git_data[4])

    root_folder = [
        p for p in pathlib.Path(os.getcwd()).parents if p.name == "pyscript"
    ][0]
    version_file = root_folder / "pyscriptjs" / "src" / "version_info.json"

    with open(version_file, "w") as fp:
        json.dump(version_data, fp, indent=2)

    print(f"After update, {version_data= }")


if __name__ == "__main__":
    print(f"updateversion.py running with arguments {sys.argv}")

