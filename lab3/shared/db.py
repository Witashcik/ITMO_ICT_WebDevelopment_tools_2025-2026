from sqlalchemy import create_engine, text

from shared.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)


def get_or_create_parser_user_id() -> int:
    """Возвращает id технического пользователя для результатов парсинга."""
    with engine.begin() as connection:
        user_id = connection.execute(
            text('SELECT id FROM "user" WHERE username = :username'),
            {"username": "parser_bot"},
        ).scalar_one_or_none()

        if user_id is not None:
            return int(user_id)

        user_id = connection.execute(
            text(
                '''
                INSERT INTO "user" (username, email, hashed_password, is_active)
                VALUES (:username, :email, :hashed_password, true)
                RETURNING id
                '''
            ),
            {
                "username": "parser_bot",
                "email": "parser_bot@example.com",
                "hashed_password": "not-used-for-login",
            },
        ).scalar_one()

        return int(user_id)


def save_title_as_tag(title: str) -> int:
    """Сохраняет заголовок страницы в таблицу tag из базы ЛР1."""
    clean_title = title.strip() or "Untitled page"
    owner_id = get_or_create_parser_user_id()

    with engine.begin() as connection:
        saved_id = connection.execute(
            text(
                '''
                INSERT INTO tag (name, owner_id)
                VALUES (:name, :owner_id)
                RETURNING id
                '''
            ),
            {"name": clean_title, "owner_id": owner_id},
        ).scalar_one()

    return int(saved_id)
