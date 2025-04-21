from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# Class Book (SRP)
@dataclass
class Book:
    title: str
    author: str
    year: int

    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.year})"


# Book validation (ISP)
class BookValidator(ABC):
    @abstractmethod
    def validate_book(self, book: Book) -> bool:
        pass


class SimpleBookValidator(BookValidator):
    """Simple implementation of book validation"""

    def validate_book(self, book: Book) -> bool:
        return bool(
            book.title.strip() and book.author.strip() and 0 < book.year <= 2024
        )


# Defining library operations (ISP)
class LibraryInterface(ABC):
    @abstractmethod
    def add_book(self, book: Book) -> bool:
        pass

    @abstractmethod
    def remove_book(self, title: str) -> bool:
        pass

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        pass


# Implementation of library operations (OCP)
class Library(LibraryInterface):
    def __init__(self, validator: BookValidator) -> None:
        self._books: List[Book] = []
        self._validator = validator

    def add_book(self, book: Book) -> bool:
        if not self._validator.validate_book(book):
            return False
        self._books.append(book)
        return True

    def remove_book(self, title: str) -> bool:
        initial_length = len(self._books)
        self._books = [book for book in self._books if book.title != title]
        return len(self._books) < initial_length

    def get_all_books(self) -> List[Book]:
        return self._books.copy()


# Class depending on abstractions (DIP)
class LibraryManager:
    def __init__(self, library: LibraryInterface) -> None:
        self._library = library

    def add_book(self, title: str, author: str, year: str) -> None:
        try:
            book = Book(title=title, author=author, year=int(year))
            if self._library.add_book(book):
                logger.info(f"Added book: {book}")
            else:
                logger.info("Failed to add book: invalid data")
        except ValueError:
            logger.info("Failed to add book: invalid year format")

    def remove_book(self, title: str) -> None:
        if self._library.remove_book(title):
            logger.info(f"Removed book: {title}")
        else:
            logger.info(f"Book not found: {title}")

    def show_books(self) -> None:
        books = self._library.get_all_books()
        if not books:
            logger.info("Library is empty")
            return

        logger.info("Library books:")
        for book in books:
            logger.info(f"- {book}")


def main() -> None:
    # Initialize with concrete implementations
    library = Library(SimpleBookValidator())
    manager = LibraryManager(library)

    while True:
        command = input("Enter command (add, remove, show, exit): ").strip().lower()

        match command:
            case "add":
                title = input("Enter book title: ").strip()
                author = input("Enter book author: ").strip()
                year = input("Enter book year: ").strip()
                manager.add_book(title, author, year)
            case "remove":
                title = input("Enter book title to remove: ").strip()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                break
            case _:
                logger.info("Invalid command. Please try again.")


if __name__ == "__main__":
    main()