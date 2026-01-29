import sys
import subprocess
import datetime
import os

BACKUP_SCHEDULER_FILE = "backup_scheduler.txt"
BACKUP_MANAGER_LOG = "./logs/backup_manager.log"
class Logger:
    def __init__(self, log_path=BACKUP_MANAGER_LOG):
        self.log_path = log_path

    def _write(self, level, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, 'a') as f:  
            f.write(f"[{timestamp}] [{level.upper()}] {message}\n")

    def info(self, message):
        self._write("INFO", message)

    def error(self, message):
        self._write("ERROR", message)

    def debug(self, message):
        self._write("DEBUG", message)

logger = Logger()

def get_process_id():
    process = subprocess.run(
        'ps -Af | grep "python3 backup_service.py"',
        shell=True,
        capture_output=True,
        text=True
        )
    for line in process.stdout.splitlines():
        if "grep" not in line:
            return int(line.split()[1])
        return None

def start_service():
    try:
        if get_process_id() is not None:
            logger.error('backup_service is already running')
            return
        subprocess.Popen(["python3", "backup_service.py"], start_new_session=True)
        logger.info('backup_service started')
    except:
        logger.error("can't start backup_service")
        
def stop_service():
    pid = get_process_id()
    if pid is None:
        logger.error('backup_service is not running')
        return
    try:
        subprocess.run(['kill', str(pid)])
        logger.info('backup_service stopped')
    except:
        logger.error("can't stop backup_service")
        
def create_scheduler(schedule):
    schedule_parts = schedule.split(';')
    if len(schedule_parts) != 3:
        logger.error("malformed schedule: " + schedule)
        return
    try:
        (hour, minute) = schedule_parts[1].split(':')
        if not (hour.isdigit() and minute.isdigit()):
            logger.error("malformed schedule: " + schedule)
            return
    except:
        logger.error("malformed schedule: " + schedule)
        return
    try:
        with open(BACKUP_SCHEDULER_FILE, "a") as f:
            f.write(schedule + "\n")
    except:
        logger.error("can't create schedule: " + schedule)
        return
    logger.info("New schedule added: " + schedule)
    
def list():
    try:
        with open(BACKUP_SCHEDULER_FILE, "r") as f:
            schedules = f.readlines()
            for i, schedule in enumerate(schedules):
                print(f"{i+1}. {schedule.strip()}")
            logger.info("Show backups list")
    except:
        logger.error("can't find backup_schedules.txt")

def delete(idx):
    try:
        with open(BACKUP_SCHEDULER_FILE, "r") as f:
            schedules = f.readlines()
            if idx < 0 or idx > len(schedules)-1:
                logger.error("can't find schedule at index " + str(idx))
                return      
        schedules.pop(idx)
        with open(BACKUP_SCHEDULER_FILE, "w") as fw:
            fw.writelines(schedules)
        logger.info(f"Schedule at index {idx} deleted")
    except:
        logger.error(f"can't find {BACKUP_SCHEDULER_FILE}")

def backups():
    try:
        files = os.listdir("./backups")
        for file in files:
            print(file)
        logger.info("Show backups list")
    except:
        logger.error("can't find backups directory")
        
        
def main():
    match sys.argv[1]:
        case "start":
            start_service()
        case "stop":
            stop_service()
        case "create":
            if len(sys.argv) < 3:
                logger.error("no schedule provided")
                return
            create_scheduler(sys.argv[2])
        case "list":
            list()
        case "delete":
            if len(sys.argv) < 3:
                logger.error("no index provided")
                return
            try:
                index = int(sys.argv[2])
                delete(index)
            except:
                logger.error("index is not an integer: " + sys.argv[2])
                return
        case "backups":
            backups()
        case _:
            print("wrong arg")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("no arguments provided")
        exit(0)
    main()

