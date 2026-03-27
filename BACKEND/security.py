class Security:
    PROTECTED_PROCESSES = [
        'system',
        'svchost',
        'winlogon',
        'csrss',
        'services',
        'lsass',
        'wininit',
        'smss'
    ]

    ALLOWED_COMMANDS = [
        'cpu',
        'ram',
        'battery',
        'disk',
        'processes',
        'weather',
        'hello',
        'voice'
    ]

    DANGEROUS_COMMANDS = ['kill', 'open']

    def validate_command(self, user_input):
        """
        Check if a command is safe to execute.
        Returns (is_safe, message)
        """
        parts = user_input.split()
        if not parts:
            return False, "Empty command"

        base = parts[0].lower()

        if base not in self.ALLOWED_COMMANDS and base not in self.DANGEROUS_COMMANDS:
            return False, f"Command '{base}' not recognized"

        return True, "Command allowed"

    def validate_kill_target(self, process_name):
        """
        Check if process is safe to kill
        Returns (is_safe, message)
        """
        if not process_name or process_name in ['*', '.', 'all']:
            return False, "Invalid process name"

        for protected in self.PROTECTED_PROCESSES:
            if protected in process_name.lower():
                return False, f"Cannot kill protected system process: {protected}"

        return True, "Target appears safe"

    def confirm_dangerous_action(self, command, target=None):
        """
        Ask for confirmation before execution
        """
        if target:
            print(f"\n WARNING: You are about to {command} '{target}'")
        else:
            print(f"\n WARNING: You are about to run '{command}'")

        response = input("Type 'yes' to confirm: ").lower()
        return response == 'yes'

_security = Security()

def validate_command(user_input):
    return _security.validate_command(user_input)

def validate_kill_target(process_name):
    return _security.validate_kill_target(process_name)

def confirm_dangerous_action(command, target=None):
    return _security.confirm_dangerous_action(command, target)