"""
library.py
Demonstrates: Lists, Tuples, Dictionaries, Sets, Functions, Loops,
Functional Programming (lambda, map, filter, list/set comprehensions),
Generators (memory-efficient streaming), Mutability.
"""

from datetime import datetime, timedelta

from models import Book, EBook, Member, Transaction, BookNotFoundError, BookUnavailableError
from file_handler import save_books, load_books, log_transaction

DUE_DAYS = 14                 # module-level constant (global scope)
LOW_STOCK_THRESHOLD = 1


class Library:

    def __init__(self):
        self.books = {}          # DICT: title -> Book/EBook object
        self.members = {}        # DICT: member_id -> Member object
        self.transactions = []   # LIST: every issue/return event, in order
        self._load_or_seed()

    # --------------------------------------------------------
    # Setup / persistence
    # --------------------------------------------------------

    def _load_or_seed(self):
        data = load_books()
        if data:
            for title, info in data.items():
                self.books[title] = Book(title, info["category"], info["copies"])
        else:
            # default starter catalog (LIST of TUPLES, unpacked in a loop)
            defaults = [
                ("Python Programming", "Programming", 5),
                ("Data Structures", "Computer Science", 3),
                ("Machine Learning", "Artificial Intelligence", 2),
                ("Operating Systems", "Computer Science", 4),
                ("Web Development", "Programming", 6),
                ("Deep Learning", "Artificial Intelligence", 2),
            ]
            for title, category, copies in defaults:      # loop + tuple unpacking
                self.books[title] = Book(title, category, copies)

            self.books["Intro to AI (eBook)"] = EBook(
                "Intro to AI (eBook)", "Artificial Intelligence",
                "https://example.com/ai-ebook"
            )

    def persist(self):
        # dict comprehension: build a plain-data dict from our Book objects,
        # skipping EBooks (they have no finite copy count to save)
        data = {
            title: {"copies": book.copies, "category": book.category}
            for title, book in self.books.items()
            if not isinstance(book, EBook)
        }
        save_books(data)

    # --------------------------------------------------------
    # CRUD
    # --------------------------------------------------------

    def add_book(self, title, category, copies):
        if title in self.books:
            raise ValueError(f"'{title}' already exists")
        self.books[title] = Book(title, category, copies)
        self.persist()

    def remove_book(self, title):
        if title not in self.books:
            raise BookNotFoundError(f"'{title}' not found")
        del self.books[title]
        self.persist()

    def update_book(self, title, category=None, copies=None):
        if title not in self.books:
            raise BookNotFoundError(f"'{title}' not found")
        book = self.books[title]
        if category:
            book._category = category
        if copies is not None:
            book.copies = copies    # goes through the property setter -> validated
        self.persist()

    # --------------------------------------------------------
    # Issue / Return
    # --------------------------------------------------------

    def issue_book(self, title, member_name):
        if title not in self.books:
            raise BookNotFoundError(f"'{title}' not found")

        book = self.books[title]
        if not book.is_available():
            raise BookUnavailableError(f"'{title}' has no copies available")

        if not isinstance(book, EBook):
            book.copies -= 1          # arithmetic operator, mutates the object

        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=DUE_DAYS)
        txn = Transaction(title, member_name, issue_date, due_date)
        self.transactions.append(txn)     # list mutation

        log_transaction(f"ISSUED  | {title} -> {member_name} | {issue_date.date()}")
        self.persist()
        return txn

    def return_book(self, title, member_name):
        # generator expression + next(): finds the first matching open
        # transaction without building an intermediate list in memory
        txn = next(
            (t for t in self.transactions
             if t.book_title == title and t.member_name == member_name and not t.returned),
            None
        )
        if txn is None:
            raise ValueError("No matching issued record found for that book/member")

        txn.mark_returned()
        if title in self.books and not isinstance(self.books[title], EBook):
            self.books[title].copies += 1

        fine = txn.calculate_fine()
        log_transaction(
            f"RETURNED| {title} <- {member_name} | {txn.return_date.date()} | Fine: {fine}"
        )
        self.persist()
        return fine

    # --------------------------------------------------------
    # Search & reporting (functional programming showcase)
    # --------------------------------------------------------

    def search_by_category(self, category):
        # filter() + lambda
        return list(filter(lambda b: b.category.lower() == category.lower(), self.books.values()))

    def search_by_name(self, keyword):
        # list comprehension
        return [b for b in self.books.values() if keyword.lower() in b.title.lower()]

    def list_categories(self):
        # set comprehension -> automatically de-duplicates categories
        return {b.category for b in self.books.values()}

    def all_titles(self):
        # map() + lambda
        return list(map(lambda b: b.title, self.books.values()))

    def sorted_by_copies(self):
        # sorted() + lambda key -> another functional-programming pattern
        physical = [b for b in self.books.values() if not isinstance(b, EBook)]
        return sorted(physical, key=lambda b: b.copies)

    def low_stock_report(self):
        """
        GENERATOR FUNCTION (uses 'yield').
        Memory-management concept: instead of building a whole list of
        low-stock books in memory, this streams them out one at a time.
        """
        for book in self.books.values():
            if not isinstance(book, EBook) and book.copies <= LOW_STOCK_THRESHOLD:
                yield book

    def total_fines_outstanding(self):
        # map + lambda + sum -> pure functional-programming one-liner
        return sum(map(lambda t: t.calculate_fine(), self.transactions))
