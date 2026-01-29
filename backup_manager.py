import sys;
import subprocess;

class Logger:
    def __init__(self, log_path="/logs/backup_manager.log"):
        self.log_path = log_path

    def _write(self, level, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, 'a') as f:  
            f.write(f"[{timestamp}] [{level.upper()}] {message}\n")

    def info(self, message):
        self._write("INFO", message)

    def error(self, message):
        self._write("ERROR", message)

    def debug(self, message):
        self._write("DEBUG", message)

logger = Logger()


if len(sys.argv) < 2:
    exit(0)
def main():
    match sys.argv[1]:
        case "start":
            start_service()
        case "stop":
            print("stop")
        case "create":
            print("create")
        case "list":
            print("lise")
        case "delete":
            print("delete")
        case "backups":
            print("backups")
        case _:
            print("wrong arg")

def start_service():
    try:
        subprocess.Popen(["python3", "backup_service.py"], start_new_session=True)
        logger.info('backup_service started')
    except:
        logger.error("can't start backup_service")

if name == "__main__":
    main()
