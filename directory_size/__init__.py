import os
from math import log

from fman import DirectoryPaneCommand, show_status_message


def get_size(url):
    total_size = 0
    surl = url.replace("file://", '')
    for dirpath, dirnames, filenames in os.walk(surl):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.stat(fp).st_size
            except (OSError, FileNotFoundError):
                return "error computing size"

    units = ('%dB', '%dKB', '%.1fMB', '%.1fGB')
    if total_size <= 0:
        unit_index = 0
    else:
        unit_index = min(int(log(total_size, 1024)), len(units) - 1)
    unit = units[unit_index]
    base = 1024 ** unit_index
    return unit % (total_size / base)


class ShowDirSize(DirectoryPaneCommand):
    def __call__(self):
        chosenFiles = self.get_chosen_files()
        show_status_message(chosenFiles[0] + ": %s" % get_size(chosenFiles[0]), 2)
