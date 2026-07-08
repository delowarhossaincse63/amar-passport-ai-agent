from __future__ import annotations


class FeeCalculatorTool:
    def calculate_fee(self, case_type: str, page_count: int = 36, service_level: str = "regular") -> dict:
        base_rates = {
            "new": 1500,
            "renewal": 1200,
            "lost": 1800,
            "minor": 1000,
        }
        service_multiplier = {
            "regular": 1.0,
            "express": 1.5,
            "super-express": 2.0,
        }

        base_fee = base_rates.get(case_type, 1500)
        multiplier = service_multiplier.get(service_level, 1.0)
        fee = int(base_fee * multiplier)
        return {
            "case_type": case_type,
            "page_count": page_count,
            "service_level": service_level,
            "amount": fee,
            "currency": "BDT",
        }
