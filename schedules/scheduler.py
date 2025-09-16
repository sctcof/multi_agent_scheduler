# schedules/scheduler.py
import asyncio
import threading
from typing import Callable, Any

class Scheduler:
    def __init__(self):
        self.tasks = []

    async def run_later(self, delay: int, func: Callable, *args):
        await asyncio.sleep(delay)
        return func(*args)

    def schedule_async(self, delay: int, func: Callable, *args):
        def run():
            asyncio.run(self.run_later(delay, func, *args))

        thread = threading.Thread(target=run)
        thread.start()
        self.tasks.append(thread)