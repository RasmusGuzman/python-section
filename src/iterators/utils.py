from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias, Generator, Iterator

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData(Iterable):
    def __init__(self, per_page: int = 3):
        self.per_page = per_page
        self.current_page = 1

    def __iter__(self) -> Generator[SomeRemoteData, None, None]:
        while True:
            page = request(Query(per_page=self.per_page, page=self.current_page))
            if page.next is None:
                break
            yield from page.results
            self.current_page = page.next


class Fibo(Iterator):
    def __init__(self, n: int):
        self.n = n
        self.current = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.n:
            raise StopIteration

        if self.current == 0:
            result = 0
        elif self.current == 1:
            result = 1
        else:
            result = self.a + self.b
            self.a, self.b = self.b, result

        self.current += 1
        return result
