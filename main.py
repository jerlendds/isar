import os

# import ipdb

source_paths = [
    "/media/jerlends/fb21cc72-c5c3-4486-855b-fd52e9e0a272",
    "/media/jerlends/Samsung_T5/Data Recovery/",
]


def scan_for_directories(directories):
    """Yield all recup_dir directories in passed list
        in format {"dirint": int, "path": str}

    Args:
        directories (list): list of path(s) to recup_dir folders
    """
    for path in directories:
        path_str = path
        for entry in os.scandir(path_str):
            try:
                yield entry.path
            except ValueError:
                print("Unexpected directory format")


files_list = ["file:///", "b'file:///", "b'file:///'"]


def scan_for_files(directory):
    for path in os.listdir(directory):
        yield os.path.join(directory, path)


def get_files(directories):
    """Recover metadata from files"""
    for directory in directories:
        yield from scan_for_files(directory)


def recover_metadata(directories):
    for each_file in get_files(directories):
        with open(each_file, "rb") as f:
            first_line = f.readline()
            detect_meta = str(first_line[:8])
            if detect_meta in files_list:
                # noqa   index 0 = unknown file, index 1 = name of unknown file
                yield (each_file, first_line)


def parse_metadata(old_files_current_location):
    for each_file in old_files_current_location:
        files = each_file[1][22:].decode().split('/')
        meta_time = files[-1].split(' ')[-1].split(',')
        mtime = meta_time[0].replace("{", "")
        mtime = mtime.replace('"mtime":', '')
        ctime = meta_time[1]
        ctime = ctime.replace('"ctime":', '')
        clean_last_element = files[-1].split(' ')
        files.pop(-1)
        files.append(clean_last_element[0])
        files = "/".join(files)
        yield { "lost_name": files, "mtime": mtime, "ctime": ctime, "current_location": each_file[0] } # noqa


for x in parse_metadata(recover_metadata(scan_for_directories(source_paths))):
    print(x, '\n\n')
