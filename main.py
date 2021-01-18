testing_paths = ["/media/jerlends/fb21cc72-c5c3-4486-855b-fd52e9e0a272"]


import os

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


def recover_metadata(directories):
    """Recover metadata from iterable"""
    count = 0
    for directory in directories:
        count += 1
        for current_file in scan_for_files(directory["path"]):
            print(current_file)
            with open(current_file, "rb") as f:
                first_line = f.readline()
                if first_line[:4] == "file":
                    print(f"Metadata for {count} files found:", first_line[:40])



if __name__ == "__main__":
    print("Sorry, this software isn't ready for release yet. If you're interested in contributing please fork and make a PR. Thanks, Jordan")