from datetime import datetime, timezone

from app import storage

STATUSES = ("free", "occupied", "out_of_order")


class UnknownStatus(Exception):
    pass


def list_lockers():
    return storage.load_all()


def get_locker(locker_id):
    return storage.get(locker_id)


def set_status(locker_id, status):
    if status not in STATUSES:
        raise UnknownStatus(status)
    payload = {
        "id": locker_id,
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    return storage.put(locker_id, payload)


def occupancy_rate():
    lockers = storage.load_all()
    if not lockers:
        return 0.0
    occupied = sum(1 for l in lockers.values() if l.get("status") == "occupied")
    return round(occupied / len(lockers) * 100, 2)
