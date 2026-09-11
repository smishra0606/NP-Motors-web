class Library:
    def __init__(self, list_of_books, library_name):
        self.books = list_of_books
        self.name = library_name
        self.lend_dict = {}

    def display_books(self):
        print(f"\n--- Books in {self.name} ---")
        for book in self.books:
            print(f"- {book}")

    def lend_book(self, user, book):
        if book not in self.books:
            print("\nSorry, we do not have that book.")
        elif book in self.lend_dict:
            print(f"\nSorry, the book is currently borrowed by {self.lend_dict[book]}.")
        else:
            self.lend_dict[book] = user
            print("\nSuccess! You have borrowed the book.")

    def add_book(self, book):
        self.books.append(book)
        print("\nSuccess! Book has been added to the library.")

    def return_book(self, book):
        if book in self.lend_dict:
            self.lend_dict.pop(book)
            print("\nSuccess! Book has been returned.")
        else:
            print("\nError: This book is not currently borrowed.")

if __name__ == '__main__':
    books_list = ['Python Crash Course', 'Clean Code', 'Automate the Boring Stuff', 'Head First Python']
    my_library = Library(books_list, "Central Campus Library")

    while True:
        print(f"\nWelcome to the {my_library.name}. Please enter a choice:")
        print("1. Display available books")
        print("2. Borrow a book")
        print("3. Donate/Add a book")
        print("4. Return a book")
        print("5. Exit")
        
        user_choice = input("\nEnter choice (1-5): ")

        if user_choice == '1':
            my_library.display_books()

        elif user_choice == '2':
            book = input("Enter the name of the book you want to borrow: ")
            user = input("Enter your name: ")
            my_library.lend_book(user, book)

        elif user_choice == '3':
            book = input("Enter the name of the book you want to add: ")
            my_library.add_book(book)

        elif user_choice == '4':
            book = input("Enter the name of the book you want to return: ")
            my_library.return_book(book)

        elif user_choice == '5':
            print("\nThank you for using the library system. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a valid number.")