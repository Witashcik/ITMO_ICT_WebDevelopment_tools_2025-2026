from __future__ import annotations

import os
from time import perf_counter
from urllib.parse import urlparse

import psycopg2
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@127.0.0.1:5433/time_manager_db",
)

URLS = [
    "https://example.com/",
    "https://www.python.org/",
    "https://fastapi.tiangolo.com/",
    "https://www.postgresql.org/",
    "https://docs.sqlalchemy.org/",
    "https://www.djangoproject.com/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Lab2Parser/1.0)",
}


def now() -> float:
    return perf_counter()


def get_title_from_html(html: str, url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    if title_tag and title_tag.text.strip():
        return " ".join(title_tag.text.split())
    return urlparse(url).netloc or url


def download_title(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return get_title_from_html(response.text, url)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def get_or_create_parser_user_id(connection) -> int:
    """Получает или создаёт технического пользователя для сохранения данных парсинга."""
    with connection.cursor() as cursor:
        cursor.execute('SELECT id FROM "user" WHERE username = %s', ("parser_bot",))
        row = cursor.fetchone()
        if row:
            return int(row[0])

        cursor.execute(
            '''
            INSERT INTO "user" (username, email, hashed_password, is_active)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            ''',
            (
                "parser_bot",
                "parser_bot@example.com",
                "not-used-in-lab2",
                True,
            ),
        )
        user_id = cursor.fetchone()[0]
        connection.commit()
        return int(user_id)


def save_title_to_database(title: str, url: str) -> int:
    """
    Сохраняет заголовок страницы в БД из ЛР1.

    В теме тайм-менеджера заголовки веб-страниц сохраняются как теги.
    Это не ломает схему ЛР1: таблица tag уже существует и связана с user.
    """
    safe_title = title[:200]
    description = f"parsed from {url}"
    name = f"{safe_title} | {description}"
    name = name[:255]

    connection = get_connection()
    try:
        user_id = get_or_create_parser_user_id(connection)
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO tag (name, owner_id) VALUES (%s, %s) RETURNING id',
                (name, user_id),
            )
            tag_id = cursor.fetchone()[0]
        connection.commit()
        return int(tag_id)
    finally:
        connection.close()


def parse_and_save(url: str) -> tuple[str, str, int | None, str | None]:
    """
    Загружает страницу, парсит title, сохраняет в БД и возвращает результат.
    Возвращает: url, title, id записи или текст ошибки.
    """
    try:
        title = download_title(url)
        saved_id = save_title_to_database(title, url)
        return url, title, saved_id, None
    except Exception as exc:
        return url, "", None, str(exc)


def print_parser_result(approach: str, results: list[tuple[str, str, int | None, str | None]], elapsed: float) -> None:
    print(f"Подход: {approach}")
    print(f"Количество URL: {len(results)}")
    for url, title, saved_id, error in results:
        if error:
            print(f"[ERROR] {url} -> {error}")
        else:
            print(f"[OK] {url} -> id={saved_id}, title={title}")
    print(f"Время выполнения: {elapsed:.6f} сек.")
