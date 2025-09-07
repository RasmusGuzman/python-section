import datetime
import logging
from datetime import date
from typing import List, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


def parse_bulletin_links(
        html: str,
        start_date: date,
        end_date: date,
        base_url: str = "https://spimex.com"
) -> List[Tuple[str, date]]:
    """
    Извлекает ссылки на XLS-бюллетени из HTML с фильтрацией по дате.

    Args:
        html: HTML-контент страницы
        start_date: Начальная дата диапазона
        end_date: Конечная дата диапазона
        base_url: Базовый URL для относительных ссылок

    Returns:
        Список кортежей (URL, дата_файла)

    TODO:
        - Добавить кеширование результатов парсинга
        - Реализовать обработку ошибок HTTP при формировании URL
    """
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")
    return [
        result for link in links
        if (result := process_single_link(link, start_date, end_date, base_url)) is not None
    ]


def process_single_link(
        link: Tag,
        start_date: date,
        end_date: date,
        base_url: str
) -> Tuple[str, date] | None:
    """Обрабатывает одну ссылку, возвращает данные или None при ошибке."""
    href = extract_clean_href(link)

    if not is_valid_bulletin_link(href):
        return None

    file_date = parse_date_from_href(href)
    if not file_date or not is_date_in_range(file_date, start_date, end_date):
        return None

    return (build_full_url(href, base_url), file_date)


def extract_clean_href(link: Tag) -> str:
    """Извлекает и очищает href от параметров."""
    return link.get("href", "").split("?")[0]


def is_valid_bulletin_link(href: str) -> bool:
    """Проверяет соответствие шаблону ссылки на бюллетень."""
    return (
            href.startswith("/upload/reports/oil_xls/oil_xls_") and
            href.endswith(".xls") and
            len(href) > len("/upload/reports/oil_xls/oil_xls_") + 8
    )

def parse_date_from_href(href: str) -> date | None:
    """Парсит дату из формата YYYYMMDD в названии файла."""
    try:
        date_str = href.split("oil_xls_")[1][:8]
        return datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except (IndexError, ValueError, TypeError) as e:
        logger.warning(f"Invalid date format in {href}: {e}")
        return None


def is_date_in_range(
        file_date: date,
        start_date: date,
        end_date: date
) -> bool:
    """Проверяет попадание даты в заданный интервал."""
    return start_date <= file_date <= end_date


def build_full_url(href: str, base_url: str) -> str:
    """Собирает абсолютный URL из относительного пути."""
    return href if href.startswith(("http://", "https://")) else urljoin(base_url, href)
