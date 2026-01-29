import datetime
import tarfile
import os
from time import sleep

BACKUP_SCHEDULER_FILE = "backup_schedules.txt"
BACKUP_SERVICE_LOG = "./logs/backup_service.log"
if os.path.exists('./logs') is False:
    os.mkdir('./logs')
if os.path.exists('./backups') is False:
    os.mkdir('./backups')
class Logger:
    def __init__(self, log_path=BACKUP_SERVICE_LOG):
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

while True:
   try:
      with open(BACKUP_SCHEDULER_FILE, "r") as f:
         schedules = f.readlines()
         for schedule in schedules:
            parts = schedule.split(';')
            schedule_time_str = parts[1].strip()
            schedule_file = parts[0].strip()
            schedule_backup = parts[2].strip()
            if datetime.datetime.now().strftime("%H:%M") == schedule_time_str:
               logger.info(f"Starting backup for {schedule_file} to {schedule_backup}")
               try:
                  with tarfile.open(f"backups/{schedule_backup}.tar", "w") as tar:
                     tar.add(schedule_file, arcname=os.path.basename(schedule_file))
                  logger.info(f"Backup completed for {schedule_file} to {schedule_backup}")
               except Exception as e:
                  logger.error(f"Backup failed for {schedule_file} to {schedule_backup}: {e}")
   except:
      logger.error(f"can't find {BACKUP_SCHEDULER_FILE}")
   sleep(45)
   

   
