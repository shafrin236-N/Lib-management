"""
file_handler.py
Demonstrates: File Handling (open/read/write/close via 'with'),
Exception Handling (try/except/finally).
No external modules needed - just Python's built-in open().
"""

BOOKS_FILE = "books_data.txt"
LOG_FILE = "transactions.log"


def save_books(books_dict):
    """
    Saves the catalog as plain text, one book per line, in the format:
    title|category|copies
    """
    try:
        with open(BOOKS_FILE, "w") as f:          # 'with' auto-closes the file
            for title, info in books_dict.items():
                f.write(f"{title}|{info['category']}|{info['copies']}\n")
    except IOError as e:
        print("Error saving data:", e)
    finally:
        # finally ALWAYS runs, whether or not an exception happened
        pass


def load_books():
    """Reads the plain text catalog back into a dict, or None if not found."""
    books_dict = {}
    try:
        with open(BOOKS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                title, category, copies = line.split("|")
                books_dict[title] = {"category": category, "copies": int(copies)}
        return books_dict if books_dict else None
    except FileNotFoundError:
        print("No saved data found - starting with default catalog.")
        return None


def log_transaction(message):
    """Append-only plain-text logging."""
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")


def read_log():
    """Reads the whole transaction log back as a list of lines."""
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []