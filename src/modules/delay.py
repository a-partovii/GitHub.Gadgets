import time
import random
from rich.live import Live
from rich.console import Console
console = Console()

def delay(message="", min=2, max=6):
    try:
        delay = random.randint(min, max)
        with Live(message, console=console, transient=True):
            with console.status(f"Waiting for delay: {delay} secends"):
                time.sleep(delay)
    # Error handeling
    except (TypeError, ValueError) as error:
        if not isinstance(min, int):
            min= 1
        elif not isinstance(max, int):
             max = 4
        elif min < 0:
            min = 0
        elif max < min:
            max = min + 1
        else:
            raise error
# -----------------------

def gap_handler(gap, variance_ratio=0.25):
    if gap <= 1:
        return 1
    gap_min = round(gap * variance_ratio - gap)
    gap_max = round(gap * variance_ratio + gap)
    return random.randint(gap_min, gap_max)

gap = 0
run_count = 0
def super_delay(message="", min=10, max=50, gap_og=8):
    global run_count, gap
    run_count += 1
    if gap == 0 :
        gap = gap_handler(gap_og, variance_ratio=0.25)
    
    if run_count == gap:
        delay(message, min, max)
        gap = gap_handler(gap_og, variance_ratio=0.25)
        run_count = 0
 # ---------------------------

def delay_and_super_delay(message="", min=5, max=15, super_min=10, super_max=50, super_gap=8):
    delay(message, min, max)
    super_delay(message, super_min, super_max, super_gap)


