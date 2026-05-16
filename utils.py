import re
import time

# ============================================================
# TIME FORMATTER
# ============================================================

def format_time(seconds):

    hours = int(seconds // 3600)

    seconds %= 3600

    minutes = int(seconds // 60)

    seconds %= 60

    return (
        f"{hours}h "
        f"{minutes}m "
        f"{int(seconds)}s"
    )

# ============================================================
# NORMALIZE FILENAMES
# ============================================================

def normalize_filename(name: str) -> str:

    name = name.lower()

    # remove extension
    name = re.sub(
        r'\.[a-z0-9]+$',
        '',
        name
    )

    # remove all non-alphanumeric chars
    name = re.sub(
        r'[^a-z0-9]',
        '',
        name
    )

    return name

# ============================================================
# IGNORE PATTERNS
# ============================================================

IGNORED_PATTERNS = [

    "sample",
    "trailer",
    "preview",
    "readme",
    "cover",
    "poster",
    "thumb",
    "thumbnail",
    ".txt",
    ".nfo",
]

# ============================================================
# FILE FILTER
# ============================================================

def should_ignore_file(name: str) -> bool:

    lowered = name.lower()

    for pattern in IGNORED_PATTERNS:

        if pattern in lowered:
            return True

    return False

# ============================================================
# MINIMUM FILESIZE
# ============================================================

MIN_FILE_SIZE = 5 * 1024 * 1024  # 5MB
