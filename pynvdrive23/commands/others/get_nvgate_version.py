import psutil
from win32api import GetFileVersionInfo, LOWORD, HIWORD


def get_pid(processName):
    listOfProcessObjects = []

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time', 'exe'])
            # Check if process name contains the given name string.
            if pinfo['name']:
                if processName.lower() in pinfo['name'].lower():
                    listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return listOfProcessObjects


def get_version_number(filename):
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
    except (Exception,):
        return 'Unknown Version'


def get_nvgate_version():
    try:
        pid = get_pid('nvgate.exe')[0]
        path = pid['exe']
        version = get_version_number(path)
        version = str(version[0]) + '.' + str(version[1])
        return version
    except (Exception,):
        return '0.0'
