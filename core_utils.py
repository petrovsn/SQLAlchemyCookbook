import time
from functools import wraps

def performance_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print("Execution time:", end_time-start_time)
        return result
    return wrapper





def performance_timer_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = await func(*args, **kwargs)

        end = time.perf_counter()

        print(f"Execution time: {end - start}")

        return result

    return wrapper