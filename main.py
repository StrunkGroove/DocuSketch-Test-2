import datetime
import subprocess
from urllib import request, error


class MonitoringMemory:
    critical_used_memory = 70 # %
    path_log = './MonitoringMemoryScript.log'
    api_alarm_path = 'http://127.0.0.1:8000/alarm'

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
        url = f'{cls.api_alarm_path}?used_memory={used_memory}'
        try:
            request.urlopen(url)
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