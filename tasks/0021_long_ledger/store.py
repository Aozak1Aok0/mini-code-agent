from models import Entry


class Store:
    def __init__(self, entries=None):
        self._entries = list(entries or [])

    def add(self, entry: Entry) -> None:
        self._entries.append(entry)

    def entries(self) -> list[Entry]:
        return list(self._entries)

    def __len__(self) -> int:
        return len(self._entries)
