from datetime import datetime

class Logger:
    LOG_FILE = "jarvis.log"

    def log_action(self, user, action, target, result):

        timestamp = datetime.now().strftime("%Y-%m-%d %H: %M: %S")

        with open(self.LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {action} | Target: {target} | Result: {result}\n")

    def log_error(self, module, error):
        """
        Record Errors separately
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H: %M: %S")

        with open(self.LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] ERROR in {module}: {error}\n")

    def view_logs(self, lines=10):
        """
        Show recent logs
        """
        try:
            with open(self.LOG_FILE, "r") as f:
                all_lines = f.readlines()
                last_lines = all_lines[-lines:]
                for line in last_lines:
                    print(line.strip())
        except FileNotFoundError:
            print("NO logs yet")