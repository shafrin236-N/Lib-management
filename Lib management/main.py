"""
main.py
Demonstrates: Basic I/O (input/print), Conditional statements,
Loops (while), Variable Scope (global vs local), Exception Handling.
"""

from library import Library
from models import BookNotFoundError, BookUnavailableError

library = Library()      # GLOBAL object - shared across every menu action

total_actions = 0         # GLOBAL variable (module-level scope)


def increment_actions():
    """
    VARIABLE SCOPE demo: 'global' tells Python to modify the module-level
    total_actions instead of creating a new LOCAL variable inside this
    function. Without the 'global' keyword this would raise an error
    (or silently create a separate local variable) on the += line.
    """
    global total_actions
    total_actions += 1


def show_menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1.  Check Availability")
    print("2.  Issue Book")
    print("3.  Return Book")
    print("4.  Search by Category")
    print("5.  Search by Name")
    print("6.  View All Categories")
    print("7.  View Full Catalog")
    print("8.  Add New Book")
    print("9.  Update Book")
    print("10. Remove Book")
    print("11. Low Stock Report")
    print("12. Total Outstanding Fines")
    print("13. Exit")


def main():
    while True:                      # LOOP: keeps the menu running
        show_menu()
        choice = input("Enter Choice: ")   # I/O: input

        if not choice.isdigit():
            print("Invalid Choice")
            continue

        choice = int(choice)          # LOCAL variable, shadows the string above
        increment_actions()

        try:
            if choice == 1:
                title = input("Enter Book Name: ")
                if title in library.books:
                    print(library.books[title].get_details())
                else:
                    print("Book Not Found")

            elif choice == 2:
                title = input("Enter Book Name: ")
                member = input("Enter Member Name: ")
                txn = library.issue_book(title, member)
                print("Book Issued Successfully. Due:", txn.due_date.date())

            elif choice == 3:
                title = input("Enter Book Name: ")
                member = input("Enter Member Name: ")
                fine = library.return_book(title, member)
                if fine > 0:
                    print(f"Book Returned. Overdue - Fine: {fine}")
                else:
                    print("Book Returned Successfully. No fine.")

            elif choice == 4:
                category = input("Enter Category: ")
                results = library.search_by_category(category)
                if results:
                    for b in results:
                        print("-", b.get_details())
                else:
                    print("No books found in this category.")

            elif choice == 5:
                keyword = input("Enter Book Name (or part of it): ")
                results = library.search_by_name(keyword)
                if results:
                    for b in results:
                        print("-", b.get_details())
                else:
                    print("No matching books found.")

            elif choice == 6:
                print("\nAvailable Categories:")
                for cat in sorted(library.list_categories()):
                    print("-", cat)

            elif choice == 7:
                print("\n===== FULL CATALOG =====")
                for title in sorted(library.all_titles()):
                    print("-", library.books[title].get_details())

            elif choice == 8:
                title = input("Enter New Book Name: ")
                category = input("Enter Category: ")
                copies = int(input("Enter Number of Copies: "))
                library.add_book(title, category, copies)
                print("Book Added Successfully")

            elif choice == 9:
                title = input("Enter Book Name to Update: ")
                new_category = input("New Category (blank to keep current): ").strip()
                new_copies = input("New Copies (blank to keep current): ").strip()
                library.update_book(
                    title,
                    category=new_category if new_category else None,
                    copies=int(new_copies) if new_copies else None
                )
                print("Book Updated Successfully")

            elif choice == 10:
                title = input("Enter Book Name to Remove: ")
                confirm = input(f"Are you sure you want to remove '{title}'? (y/n): ").strip().lower()
                if confirm == "y":
                    library.remove_book(title)
                    print("Book Removed Successfully")
                else:
                    print("Cancelled")

            elif choice == 11:
                print("\n===== LOW STOCK REPORT =====")
                found_any = False
                for book in library.low_stock_report():   # consuming a generator
                    print("-", book.get_details())
                    found_any = True
                if not found_any:
                    print("No books are low on stock.")

            elif choice == 12:
                print("Total outstanding fines across all members:", library.total_fines_outstanding())

            elif choice == 13:
                print(f"Thank You. Total actions this session: {total_actions}")
                break

            else:
                print("Invalid Choice")

        except BookNotFoundError as e:
            print("Error:", e)
        except BookUnavailableError as e:
            print("Error:", e)
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
