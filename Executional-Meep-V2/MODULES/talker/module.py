"""
manages meep output.
keeps the sentences and select when, and in which order they will be sent.
"""
from utilities import JsonInterface
import asyncio
import os

buffer = JsonInterface(os.path.join(os.getcwd(), "MODULES", "talker", "buffer.json"))

def say(meep, sentence):
    """
    action
    adds a sentence to the buffer
    """
    buffer.get()["sentences"].append(sentence)
    buffer.save()

async def fetch_talk(meep, function_keyword):
    """
    action
    fetch data from a function and use talker to say that data
    """
    if " : " in function_keyword:
        data = await meep.FETCH(function_keyword)
    else:
        data = await meep.FETCH("any : %s" % function_keyword)
    meep.EXECUTE("talker : say", data)

def buffer_length(meep):
    """
    getter 
    gets the sentence buffers length
    """
    return len( buffer.get("sentences"))

async def on_buffer(meep):
    """
    listener
    when the buffer is not empty
    sends a message from the buffer - to discord
    """
    while True:
        while buffer_length(meep) == 0:
            await asyncio.sleep(1)

        message = buffer.get("sentences")[0]
        buffer.get("sentences").pop(0)
        buffer.save()

        meep.EXECUTE("discord : easy send", message)

