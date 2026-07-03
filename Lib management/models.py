"""
models.py
Demonstrates: OOP (classes/objects, inheritance, polymorphism, encapsulation,
abstraction), custom exceptions, basic data types, operators.
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
# CUSTOM EXCEPTIONS
# (Exception Handling + Inheritance: custom exceptions inherit from Exception)
# ============================================================

class BookNotFoundError(Exception):
    """Raised when a requested title does not exist in the catalog."""
    pass


class BookUnavailableError(Exception):
    """Raised when a book exists but has zero copies left."""
    pass


# ============================================================
# ABSTRACTION
# LibraryItem is an Abstract Base Class - it can never be instantiated
# directly. It forces every subclass to implement get_details().
# ============================================================

class LibraryItem(ABC):

    def __init__(self, title, category):
        # ENCAPSULATION: leading underscore marks these as "private" -
        # outside code is expected to go through properties, not touch
        # these directly.
        self._title = title          # str  (basic data type)
        self._category = category    # str

    @property
    def title(self):
        return self._title

    @property
    def category(self):
        return self._category

    @abstractmethod
    def get_details(self):
        """Every subclass MUST override this. Enforced by ABC."""
        raise NotImplementedError

    def __str__(self):
        return self.get_details()


# ============================================================
# INHERITANCE: Book inherits from LibraryItem
# ============================================================

class Book(LibraryItem):

    def __init__(self, title, category, copies):
        super().__init__(title, category)   # reuse the parent constructor
        self._copies = copies                # int (basic data type)

    @property
    def copies(self):
        return self._copies

    @copies.setter
    def copies(self, value):
        # ENCAPSULATION: validation is centralized here instead of being
        # repeated everywhere copies gets changed.
        if value < 0:
            raise ValueError("Copies cannot be negative")
        self._copies = value

    def is_available(self):
        return self._copies > 0          # bool (basic data type), comparison operator

    def get_details(self):
        return f"{self._title} | Category: {self._category} | Copies: {self._copies}"


# ============================================================
# INHERITANCE + POLYMORPHISM
# EBook inherits from Book but overrides behaviour completely.
# Calling get_details()/is_available() on a Book vs an EBook runs
# DIFFERENT code even though the calling code looks identical -
# that's polymorphism.
# ============================================================

class EBook(Book):

    def __init__(self, title, category, download_link):
        super().__init__(title, category, copies=float("inf"))  # float (basic data type)
        self._download_link = download_link

    def is_available(self):
        return True   # overridden: an eBook is never "out of stock"

    def get_details(self):
        return f"{self._title} (eBook) | Category: {self._category} | Link: {self._download_link}"


# ============================================================
# Member - a regular class, no inheritance needed here
# ============================================================

class Member:

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self._borrowed_books = []   # list: ordered, mutable, allows duplicates

    def borrow(self, title):
        self._borrowed_books.append(title)

    def give_back(self, title):
        if title in self._borrowed_books:
            self._borrowed_books.remove(title)

    @property
    def borrowed_books(self):
        # returns a TUPLE: an immutable snapshot so outside code can't
        # accidentally mutate the member's real record
        return tuple(self._borrowed_books)


# ============================================================
# Transaction - one issue/return event
# ============================================================

class Transaction:

    FINE_PER_DAY = 5   # class attribute shared by all Transaction objects

    def __init__(self, book_title, member_name, issue_date, due_date):
        self.book_title = book_title
        self.member_name = member_name
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = None
        self.returned = False       # bool

    def mark_returned(self):
        self.returned = True
        self.return_date = datetime.now()

    def calculate_fine(self):
        """Operators: subtraction (via timedelta), comparison, multiplication."""
        if self.return_date is None:
            return 0
        days_late = (self.return_date - self.due_date).days   # arithmetic
        if days_late > 0:
            return days_late * Transaction.FINE_PER_DAY        # multiplication operator
        return 0
