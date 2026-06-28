"""Helpers for parsing uploaded transcript text and deriving metadata."""

import re
from collections import Counter

STOPWORDS = {
    "about", "after", "also", "been", "could", "from", "have", "into",
    "just", "like", "more", "some", "that", "their", "there", "these",
    "they", "this", "through", "very", "what", "when", "which", "with",
    "would", "thanks", "thank", "everyone", "hello", "meeting", "today",
    "please", "okay", "yeah", "right", "need", "needs", "going", "join",
    "joined", "joining", "discuss", "discussion", "said", "says",
    "good", "morning", "afternoon", "evening", "welcome", "let", "lets",
    "team", "project", "people", "work", "working", "think", "want",
    "will", "shall", "should", "make", "made", "using", "use",
}

GREETING_RE = re.compile(
    r"^(thanks\s+everyone|thank\s+you|hello|hi\s+everyone|good\s+(morning|afternoon|evening))",
    re.I,
)
SPEAKER_LABEL_RE = re.compile(r"[A-Za-z]+\s+[A-Za-z]+\s*:")
SINGLE_SPEAKER_RE = re.compile(r"^[A-Za-z]+\s*:")

NOUN_SUFFIXES = ("tion", "ment", "ness", "ity", "ance", "ence", "ing")

ACTION_TRIGGERS = (
    "will", "should", "need to", "follow up", "assign",
    "let's", "let us", "action", "by friday", "by monday", "next week",
)

TASK_PREFIX_RE = re.compile(
    r"^(we|i|the team|let's|let us)\s+(should|will|need to|can)\s+",
    re.I,
)


def title_from_filename(filename: str) -> str:
    """Convert a filename stem into a human-readable title."""
    stem = filename.rsplit(".", 1)[0].strip() if "." in filename else filename.strip()
    if not stem:
        return "Uploaded Meeting"
    normalized = re.sub(r"[_-]+", " ", stem)
    return normalized.title()


def parse_transcript_lines(content: str) -> list[tuple[str, str]]:
    """
    Parse transcript lines into (speaker, text).

    Expected format:
        Sarah Chen: Thanks everyone for joining.

    Lines without ':' are assigned to an Unknown speaker.
    """

    entries: list[tuple[str, str]] = []

    for line in content.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if ":" in stripped:
            speaker, text = stripped.split(":", 1)

            speaker = speaker.strip()
            text = text.strip()

            if speaker and text:
                entries.append((speaker, text))
                continue

        entries.append(("Unknown", stripped))

    return entries


def _strip_speaker_labels(text: str) -> str:
    """Remove speaker name prefixes from transcript text."""
    text = SPEAKER_LABEL_RE.sub("", text)
    return SINGLE_SPEAKER_RE.sub("", text)


def _is_greeting_sentence(sentence: str) -> bool:
    return bool(GREETING_RE.match(sentence.strip()))


def _build_excluded_names(participant_names: set[str] | None) -> set[str]:
    excluded = set(STOPWORDS)
    if not participant_names:
        return excluded
    for name in participant_names:
        for part in name.lower().split():
            excluded.add(part)
        excluded.add(name.lower().replace(" ", ""))
    return excluded


def _is_noun_like(word: str) -> bool:
    return any(word.endswith(suffix) for suffix in NOUN_SUFFIXES)


def extract_summary(
    text: str,
    participant_names: set[str] | None = None,
) -> str | None:
    """Generate a concise meeting summary using simple heuristics."""

    cleaned = _strip_speaker_labels(" ".join(text.split()))

    if not cleaned:
        return None

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", cleaned)
        if sentence.strip()
    ]

    content_sentences = [
        s for s in sentences
        if not _is_greeting_sentence(s) and len(s) >= 20
    ]

    if not content_sentences:
        content_sentences = [
            s for s in sentences if not _is_greeting_sentence(s)
        ]

    if not content_sentences:
        return None

    excluded = _build_excluded_names(participant_names)

    significant: list[str] = []
    for sentence in content_sentences:
        words = re.findall(r"[A-Za-z]{4,}", sentence.lower())
        for word in words:
            if word not in excluded:
                significant.append(word)

    if not significant:
        return (
            "This meeting covered several discussion points "
            "and agreed on next steps."
        )

    ranked = Counter(significant).most_common(8)
    topics = [word.capitalize() for word, _ in ranked]

    focus = ", ".join(topics[:3])
    summary = f"This meeting focused on {focus}."

    if len(topics) > 3:
        extra = ", ".join(topics[3:5])
        summary += (
            f" The team discussed {extra} and agreed on next steps."
        )
    else:
        summary += " The team discussed implementation priorities and agreed on next steps."

    return summary


def extract_key_topics(
    text: str,
    limit: int = 5,
    participant_names: set[str] | None = None,
) -> str | None:
    """
    Extract keyword topics using word frequency.

    Speaker names, greetings, and filler words are excluded.
    """

    text = _strip_speaker_labels(text)
    excluded = _build_excluded_names(participant_names)

    words = re.findall(r"[A-Za-z]{4,}", text.lower())

    scored: Counter[str] = Counter()
    for word in words:
        if word in excluded:
            continue
        score = 1
        if _is_noun_like(word):
            score = 2
        scored[word] += score

    if not scored:
        return None

    topics: list[str] = []
    seen: set[str] = set()

    for word, _ in scored.most_common():
        if word in seen:
            continue
        seen.add(word)
        topics.append(word.capitalize())
        if len(topics) >= limit:
            break

    if not topics:
        return None

    return ", ".join(topics)


def _clean_task(text: str) -> str:
    cleaned = TASK_PREFIX_RE.sub("", text.strip()).strip()
    cleaned = re.sub(r"^need to\s+", "", cleaned, flags=re.I)
    if cleaned.endswith("."):
        cleaned = cleaned[:-1]
    if cleaned:
        return cleaned[0].upper() + cleaned[1:]
    return text.strip()


def extract_action_items(
    entries: list[tuple[str, str]],
) -> list[tuple[str, str | None]]:
    """Extract action items from transcript entries using phrase heuristics."""

    seen: set[str] = set()
    items: list[tuple[str, str | None]] = []

    for speaker, text in entries:
        lower = text.lower()
        if not any(trigger in lower for trigger in ACTION_TRIGGERS):
            continue

        task = _clean_task(text)
        key = task.lower()
        if not task or key in seen:
            continue

        seen.add(key)
        assigned = speaker if speaker != "Unknown" else None
        items.append((task, assigned))

    return items


def distribute_transcript_timestamps(
    duration_minutes: int,
    count: int,
) -> list[int]:
    """
    Evenly distribute transcript timestamps across the meeting.

    Leaves approximately 2.5 minutes at the end so the final
    transcript entry isn't exactly at the meeting end.
    """

    if count == 0:
        return []

    total_seconds = duration_minutes * 60

    end_buffer_seconds = 150
    end_seconds = max(0, total_seconds - end_buffer_seconds)

    if count == 1:
        return [0]

    return [
        round(end_seconds * index / (count - 1))
        for index in range(count)
    ]
