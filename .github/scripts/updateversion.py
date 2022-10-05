import json
import os
import pathlib
import re
import subprocess
import sys


def update_version_info() -> None:
    print(f"Running main() in updateversion.py with arguments {sys.argv}")

    # Get release level from script argument
    release_level = sys.argv[1]

    version_data = {}
    git_data = get_git_data()

    version_data["major"] = int(git_data[0])
    version_data["minor"] = int(git_data[1])
    version_data["patch"] = int(git_data[2])
    version_data["releaselevel"] = release_level
    version_data["commit"] = int(git_data[3])

    root_folder = [
        p for p in pathlib.Path(os.getcwd()).parents if p.name == "pyscript"
    ][0]
    print(root_folder)
    print(os.listdir(root_folder))
    version_file = root_folder / "pyscriptjs" / "src" / "version_info.json"
    print(version_file)

    with open(version_file, "w") as fp:
        json.dump(version_data, fp, indent=2)

    print(f"After update, {version_data= }")


def get_git_data() -> list[str]:
    raw = subprocess.check_output(["git", "describe", "--tags"]).decode("ascii").strip()
    return re.split(".-", raw)


if __name__ == "__main__":
    update_version_info()
