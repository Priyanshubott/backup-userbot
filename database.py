import sqlite3
        FROM copied_messages
        WHERE source_chat_id=?
        AND message_id=?
        """,
        (source_chat_id, message_id)
    )

    result = cur.fetchone()

    conn.close()

    return bool(result)


def mark_copied(source_chat_id, message_id):

    conn = get_db()

    conn.execute(
        """
        INSERT OR IGNORE INTO copied_messages
        VALUES (?, ?)
        """,
        (source_chat_id, message_id)
    )

    conn.commit()

    conn.close()


def get_last_message_id(source_chat_id):

    conn = get_db()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT last_message_id
        FROM sync_state
        WHERE source_chat_id=?
        """,
        (source_chat_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0


def set_last_message_id(source_chat_id, message_id):

    conn = get_db()

    conn.execute(
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

    conn.commit()

    conn.close()
