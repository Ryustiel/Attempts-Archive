from datetime import datetime
import asyncio

def get_time(meep):
    """
    fetch
    gets datetime
    """
    return str(datetime.now())

def schedule(meep, intructionString: str, delay: float):
    """
    action
    executes the string after the delay
    individual instructions inside the instructionString must be separated by a [new line]
    """
    ...

def smart_queue(meep, listener: str, frequency: float, minFrequency: float=None, maxFrequency: float=None):
    """
    groups listeners into the same function call, to save processing power on asyncio
    """
    
    ...

global tick_stopper
tick_stopper = False
async def tick(meep):
    """
    action
    displays a message in the console every 5 seconds
    """
    global tick_stopper
    tick_stopper = False
    while not tick_stopper:
        await asyncio.sleep(5)
        meep.EXECUTE("talker : say", "timer ticking...")
    tick_stopper = False

def stop_ticking(meep):
    """
    action
    stops the ticking
    """
    global tick_stopper
    tick_stopper = True
    meep.EXECUTE("talker : say", "stopped ticking")