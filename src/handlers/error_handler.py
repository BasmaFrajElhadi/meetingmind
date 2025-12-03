import logging
import traceback
from pathlib import Path
from functools import wraps

# Ensure logs directory exists
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("MeetingMind")
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(LOG_DIR / "error.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class MeetingMindError(Exception):
    """
    MeetingMindError is a custom exception class specifically designed
    for the MeetingMind system.

    It allows distinguishing project-specific errors from generic exceptions.

    Responsibilities:
    - Represent errors unique to MeetingMind functionalities.
    - Provide a clear message describing the error.
    """

    def __init__(self, message="An error occurred in MeetingMind"):
        """
        Initialize MeetingMindError.

        Args:
            message (str):
                A descriptive message for the exception.
                Defaults to "An error occurred in MeetingMind".
        """
        super().__init__(message)
        self.message = message



def handle_errors(user_message="An unexpected error occurred"):
    """
    Decorator to handle exceptions for a function.

    Catches all exceptions, logs them, and returns a structured dictionary
    with an error message. Specifically handles MeetingMindError separately.

    Args:
        user_message (str): User-friendly message to return for generic exceptions.

    Returns:
        Callable: Wrapped function that handles exceptions and logs them.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except MeetingMindError as e:
                logger.error(f"MeetingMindError: {e.message}")
                return {"status": "error", "message": e.message}
            except Exception as e:
                logger.error(traceback.format_exc())
                return {"status": "error", "message": f"{user_message}: {str(e)}"}
        return wrapper
    return decorator

def format_streamlit_error(error_message: str):
    """
    Format an error message for display in Streamlit UI.

    Args:
        error_message (str): Raw error message.

    Returns:
        str: Formatted error message suitable for Streamlit.
    """
    return f"🚨 System error: {error_message}"
