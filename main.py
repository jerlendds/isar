"""This file is under construction!"""



import os
import re
import time

testing_paths = [
    "/media/jerlends/Samsung_T5/Data Recovery/",
    "/media/jerlends/fb21cc72-c5c3-4486-855b-fd52e9e0a272",
]

if __name__ == "__main__":
    print(
        f"Sorry, this software isn't ready for release yet. If you're interested in contributing please fork and make a PR. Thanks \n\n To recover metadata use the recover_metadata function and pass in the sort directories function with testing_paths. \n\n\n ATTEMPTING META DATA RECOVERY FROM {testing_paths}"
    )
    time.sleep(8)

def scan_for_directories(directories):
    """Yield all recup_dir directories in passed list in format {"dirint": int, "path": str}

    Args:
        directories (list): list of path(s) to directory that contains recup_dir folders
    """
    for path in directories:
        path_str = path
        for entry in os.scandir(path_str):
            # * basename provides everything after last slash
            cleaned_path = os.path.basename(entry.path).split(".")[1]
            try:
                cleaned_path = int(cleaned_path)
                yield {"dirint": cleaned_path, "path": entry.path}
            except ValueError:
                print("Unexpected directory format:", cleaned_path)
                if (
                    input(
                        f'Do you want to include "{cleaned_path}" in the search? (y/n)'
                    ).lower()
                    == "y"
                ):
                    yield {"dirint": cleaned_path, "path": entry.path}


def sort_directories(directories, is_descending=False):
    """Yield all directories in ascending order

    Args:
        directories (list): path string(s) to directory that contains recup_dir folders
    [Optional]:
        is_decending (bool): if true yield descending
    """
    directory_generator = scan_for_directories(directories)
    mylist = []
    for directory in directory_generator:
        mylist.append(directory)
    sorted_list = sorted(mylist, key=lambda k: k["dirint"], reverse=is_descending)
    yield from sorted_list


def scan_for_files(directory):
    for path in os.listdir(directory):
        yield os.path.join(directory, path)


def get_files(directories):
    """Recover metadata from files"""
    for directory in directories:
        yield from scan_for_files(directory["path"])


files_list = ["file:///", "b'file:///", "b'file:///'"]


def recover_metadata(directories):
    metadata_files_count = 0
    for each_file in get_files(directories):
        with open(each_file, "rb") as f:
            first_line = f.readline()
            detect_meta = str(first_line[:8])
            if detect_meta in files_list:
                metadata_files_count += 1
                print(
                    metadata_files_count,
                    "\n",
                    first_line,
                    "\n\n",
                    each_file,
                    "\n\n\n\n",
                )


recover_metadata(sort_directories(testing_paths, True))


def sort_metadata():
    """Remove known system files and organize by mtime or ctime"""
    pass



