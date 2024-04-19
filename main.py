import datetime
import subprocess
import json
from urllib import error
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class MonitoringMemory:
    critical_used_memory = 20 # %
    path_log = './MonitoringMemoryScript.log'
    api_alarm_path = 'http://localhost:8080/api/v1/'

    @classmethod
    def main(cls) -> None:
        used_memory = cls._get_memory_used()
        if used_memory >= cls.critical_used_memory:
            cls._send_alarm(used_memory)

    @classmethod
    def _get_memory_used(cls) -> float:
        try:
            output = subprocess.check_output(['free', '-m']).decode('utf-8')
        except subprocess.CalledProcessError as e:
            cls._log(f"Error command 'free': {str(e)}")

        lines = output.split('\n')
        values = lines[1].split()

        total = values[1]
        used = values[2]
        return cls._count_memory_used(used, total)

    @classmethod
    def _send_alarm(cls, used_memory: float) -> None:
        data = {"used_memory": used_memory}
        headers = {'Content-Type': 'application/json'}
        req = Request(cls.api_alarm_path, json.dumps(data).encode(), headers=headers)
        try:
            urlopen(req)
        except error.URLError as e:
            cls._log(f'Error send alarm: {str(e)}')

    @classmethod
    def _log(cls, message: str) -> None:
        with open(cls.path_log, "a") as error_file:
            error_file.write(f'{cls._current_time()}: {message}\n')

    @staticmethod
    def _count_memory_used(used: str, total: str) -> float:
        return (float(used) / float(total)) * 100
    
    @staticmethod
    def _current_time() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


MonitoringMemory().main()