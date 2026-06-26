from __future__ import annotations

import asyncio
from urllib.parse import urlparse

import aiohttp
import asyncpg
from bs4 import BeautifulSoup

from common_parser import DATABASE_URL, HEADERS, URLS, now, print_parser_result


def get_title_from_html(html: str, url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    if title_tag and title_tag.text.strip():
        return " ".join(title_tag.text.split())
    return urlparse(url).netloc or url


async def get_or_create_parser_user_id(connection: asyncpg.Connection) -> int:
    row = await connection.fetchrow('SELECT id FROM "user" WHERE username = $1', "parser_bot")
    if row:
        return int(row["id"])

    user_id = await connection.fetchval(
        '''
        INSERT INTO "user" (username, email, hashed_password, is_active)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        ''',
        "parser_bot",
        "parser_bot@example.com",
        "not-used-in-lab2",
        True,
    )
    return int(user_id)


async def save_title_to_database(pool: asyncpg.Pool, title: str, url: str) -> int:
    safe_title = title[:200]
    name = f"{safe_title} | parsed from {url}"
    name = name[:255]

    async with pool.acquire() as connection:
        user_id = await get_or_create_parser_user_id(connection)
        tag_id = await connection.fetchval(
            'INSERT INTO tag (name, owner_id) VALUES ($1, $2) RETURNING id',
            name,
            user_id,
        )
        return int(tag_id)


async def parse_and_save(url: str, http_session: aiohttp.ClientSession, db_pool: asyncpg.Pool):
    try:
        async with http_session.get(url, timeout=15) as response:
            response.raise_for_status()
            html = await response.text()

        title = get_title_from_html(html, url)
        saved_id = await save_title_to_database(db_pool, title, url)
        return url, title, saved_id, None
    except Exception as exc:
        return url, "", None, str(exc)


async def main_async() -> None:
    started_at = now()

    async with aiohttp.ClientSession(headers=HEADERS) as http_session:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
        try:
            tasks = [parse_and_save(url, http_session, db_pool) for url in URLS]
            results = await asyncio.gather(*tasks)
        finally:
            await db_pool.close()

    elapsed = now() - started_at
    print_parser_result("asyncio + aiohttp", results, elapsed)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
