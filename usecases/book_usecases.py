from typing import List, Optional
from domain.entities import Book
from domain.repositories import BookRepository

class ListBooksUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def execute(self) -> List[Book]:
        return self.book_repo.list_books()

class GetBookDetailUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def execute(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id)
