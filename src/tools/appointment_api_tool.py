from __future__ import annotations
from datetime import datetime, timedelta


class AppointmentApiTool:
    def get_slots(self, location: str = "Dhaka", days: int = 5) -> list[dict]:
        slots = []
        start = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        for day in range(days):
            appointment_date = start + timedelta(days=day)
            slots.append(
                {
                    "location": location,
                    "datetime": appointment_date.isoformat(),
                    "available": True,
                }
            )
        return slots
