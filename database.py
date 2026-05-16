import sqlite3

DB_NAME = "backup.db"

# ============================================================
# SHARED SQLITE CONNECTION
# ============================================================

_conn = sqlite3.connect(
    DB_NAME,
    check_same_thread=False
)

# Better concurrent behavior
_conn.execute(
    "PRAGMA journal_mode=WAL"
)

# Faster writes while remaining safe
_conn.execute(
    "PRAGMA synchronous=NORMAL"
)

# ============================================================
# TABLES
# ============================================================

# Tracks copied Telegram messages
_conn.execute("""
CREATE TABLE IF NOT EXISTS copied_messages (
    source_chat_id INTEGER,
    message_id     INTEGER,
    PRIMARY KEY(source_chat_id, message_id)
)
""")

# Tracks last synced message per source
_conn.execute("""
CREATE TABLE IF NOT EXISTS sync_state (
    source_chat_id  INTEGER PRIMARY KEY,
    last_message_id INTEGER
)
""")

# Tracks archived media files
_conn.execute("""
CREATE TABLE IF NOT EXISTS archived_files (
    normalized_name TEXT,
    file_size       INTEGER,
    PRIMARY KEY(normalized_name, file_size)
)
""")

# Generic settings table
_conn.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
)
""")

_conn.commit()

# ============================================================
# MESSAGE DEDUP
# ============================================================

def is_copied(
    source_chat_id: int,
    message_id: int
) -> bool:

    cur = _conn.execute(
        """
        SELECT 1
        FROM copied_messages
        WHERE source_chat_id=?
        AND message_id=?
        """,
        (source_chat_id, message_id)
    )

    return cur.fetchone() is not None


def mark_copied(
    source_chat_id: int,
    message_id: int
) -> None:

    _conn.execute(
        """
        INSERT OR IGNORE
        INTO copied_messages
        VALUES (?, ?)
        """,
        (source_chat_id, message_id)
    )

    _conn.commit()

# ============================================================
# SYNC STATE
# ============================================================

def get_last_message_id(
    source_chat_id: int
) -> int:

    cur = _conn.execute(
        """
        SELECT last_message_id
        FROM sync_state
        WHERE source_chat_id=?
        """,
        (source_chat_id,)
    )

    row = cur.fetchone()

    return row[0] if row else 0


def set_last_message_id(
    source_chat_id: int,
    message_id: int
) -> None:

    _conn.execute(
        """
        INSERT INTO sync_state
        (source_chat_id, last_message_id)
        VALUES (?, ?)

        ON CONFLICT(source_chat_id)
        DO UPDATE SET
        last_message_id=excluded.last_message_id
        """,
        (source_chat_id, message_id)
    )

    _conn.commit()

# ============================================================
# ARCHIVE DEDUP
# ============================================================

def file_exists(
    normalized_name: str,
    file_size: int
) -> bool:

    cur = _conn.execute(
        """
        SELECT 1
        FROM archived_files
        WHERE normalized_name=?
        AND file_size=?
        """,
        (normalized_name, file_size)
    )

    return cur.fetchone() is not None


def add_archived_file(
    normalized_name: str,
    file_size: int
) -> None:

    _conn.execute(
        """
        INSERT OR IGNORE
        INTO archived_files
        VALUES (?, ?)
        """,
        (normalized_name, file_size)
    )

    _conn.commit()

# ============================================================
# SETTINGS
# ============================================================

def get_setting(
    key: str
):

    cur = _conn.execute(
        """
        SELECT value
        FROM settings
        WHERE key=?
        """,
        (key,)
    )

    row = cur.fetchone()

    return row[0] if row else None


def set_setting(
    key: str,
    value: str
) -> None:

    _conn.execute(
        """
        INSERT INTO settings
        (key, value)
        VALUES (?, ?)

        ON CONFLICT(key)
        DO UPDATE SET
        value=excluded.value
        """,
        (key, value)
    )

    _conn.commit()
