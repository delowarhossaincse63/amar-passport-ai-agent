from __future__ import annotations

from src.tools.appointment_api_tool import AppointmentApiTool
from src.tools.fee_calculator_tool import FeeCalculatorTool


class FeeAppointmentAgent:
    def __init__(self) -> None:
        self.fee_tool = FeeCalculatorTool()
        self.appointment_tool = AppointmentApiTool()

    def run(self, case_type: str, service_level: str = "regular") -> dict:
        fee = self.fee_tool.calculate_fee(case_type=case_type, service_level=service_level)
        slots = self.appointment_tool.get_slots()
        return {
            "fee": fee,
            "appointment_slots": slots,
        }
