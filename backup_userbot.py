import asyncio
        )

    # ========================================================

    elif cmd == "/status":

        uptime = format_time(
            time.time() - stats["started_at"]
        )

        await message.reply(
            f"📊 STATUS\n\n"
            f"Processed: {stats['processed']}\n"
            f"Copied: {stats['copied']}\n"
            f"Skipped: {stats['skipped']}\n"
            f"Errors: {stats['errors']}\n"
            f"FloodWaits: {stats['floodwaits']}\n\n"
            f"Sources: {len(SOURCE_CHANNELS)}\n"
            f"Destinations: {len(DEST_CHANNELS)}\n"
            f"Paused: {clone_paused}\n"
            f"Delay: {COPY_DELAY}s\n\n"
            f"Uptime: {uptime}"
        )

# ============================================================
# MAIN
# ============================================================

async def main():

    await app.start()

    logger.info(
        "Starting Backup Userbot..."
    )

    logger.info(
        f"Sources: {SOURCE_CHANNELS}"
    )

    logger.info(
        f"Destinations: {DEST_CHANNELS}"
    )

    await sync_peers()

    # initial catchup

    for source in SOURCE_CHANNELS:

        try:

            await app.get_chat(source)

            logger.info(
                f"Resolved source: {source}"
            )

        except Exception as e:

            logger.error(
                f"Source failed: {source} | {e}"
            )

    # background recovery loop

    asyncio.create_task(
        catchup_loop()
    )

    logger.info(
        "Userbot fully operational"
    )

    await pyrogram.idle()

    await app.stop()

# ============================================================
# RUN
# ========
