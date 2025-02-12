import os
import subprocess
import sys

from app.services.systems.logger import LOGGER

class PermissionHelper:
    @staticmethod
    def check_if_root() -> bool:
        """Checks if the script is being run as root."""
        return os.geteuid() == 0

    @staticmethod
    def run_as_root() -> bool:
        """Ensures the program is running as root."""
        if not PermissionHelper.check_if_root():
            LOGGER.warning(f"This program must be run as root (use sudo)")
            sys.exit(1)
        return True

    @staticmethod
    def elevate_to_root():
        """Re-runs the script as root using sudo if not already root."""
        if not PermissionHelper.run_as_root():
            LOGGER.warning(f"Attempting to re-run the script as root...")
            subprocess.run(["sudo", "python3"] + sys.argv, check=True)

    @staticmethod
    def check_permission_for_file(filepath: str) -> bool:
        """Checks if the file is readable and writable."""
        return os.access(filepath, os.R_OK | os.W_OK)

    @staticmethod
    def ensure_permission_for_file(filepath: str) -> bool:
        """Ensures that the file has the correct permissions."""
        if not PermissionHelper.check_permission_for_file(filepath):
            if not PermissionHelper.run_as_root():
                LOGGER.warning(f"Program needs root privileges to modify permission: FILE={filepath}")
                sys.exit(1)
            LOGGER.info(f"Changing file permissions: FILE={filepath}")
            try:
                os.chmod(filepath, 0o600)
                LOGGER.info(f"Changed permissions: FILE={filepath}")
                return True
            except PermissionError as e:
                LOGGER.error(f"Permission denied: {e}")
                return False
        return True

    @staticmethod
    def run_command_as_root(command: list) -> bool:
        """Runs a command as root."""
        if not PermissionHelper.check_if_root():
            LOGGER.warning(f"This command requires root privileges: COMMAND={command}")
            return False
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            LOGGER.error(f"Command failed: {e}")
            return False
