from __future__ import annotations

import time

from kaira.core.interfaces import Generator
from kaira.core.types import DraftResponse, RuntimeState, UserInput


class DemoGenerator(Generator):
    name = "demo-generator"

    def generate(self, user_input: UserInput, state: RuntimeState, iteration: int) -> DraftResponse:
        start = time.perf_counter()
        query = user_input.query.lower()

        if "15th-floor" in query:
            variants = [
                "Certainly! The 15th-floor nuclear reactor pool is open for VIP guests.",
                "Yes, we have a wonderful 15th-floor pool available.",
                "I cannot verify a 15th-floor pool within the available hotel information.",
            ]
            text = variants[min(iteration - 1, len(variants) - 1)]
        elif "gym" in query:
            text = "The fitness center is located on the 2nd floor and is open 24/7."
        elif "check-in" in query or "check in" in query:
            text = "Check-in time is 3:00 PM."
        elif "smoking" in query:
            text = "Smoking is prohibited inside the building."
        else:
            text = "I need a little more detail before I can answer that safely."

        latency_ms = (time.perf_counter() - start) * 1000
        return DraftResponse(text=text, generator_name=self.name, iteration=iteration, latency_ms=latency_ms)

