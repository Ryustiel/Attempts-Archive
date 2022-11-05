"""
controls actions using strict syntax rules
"""

from utilities import JsonInterface

MATCHES = JsonInterface("MODULES/basic_input_manager/matches.json")

def refresh_matches():
    MATCHES.load()

# ============================== MATCHING

def matcher(meep, input):
    """
    action
    does something with the input
    """
    if ' ! ' in input:
        statements = input.split(' ! ')
        meep.EXECUTE(statements[0], statements[1])
    else:
        meep.EXECUTE(input)
    return
    for match in MATCHES.get()["matches"]:
        if input == match[0]:
            meep.EXECUTE(match[0])

    # else routes to conversation module

# ============================== EXECUTE SEMANTICS

async def find_function(meep, instruction, category):
    """
    getter
    searches for the most similar function (to the instruction) by looking at its name and description.
    """
    function_strings = await meep.FETCH("module : generate_option_list", category=category)
    rankings = await meep.FETCH("general : list matcher", instruction, function_strings)
    
    single_function_string = rankings[0][0]
    new_instruction = ""
    for character in single_function_string:
        if character == "|": # isolates the "function call" part of the string
            break
        new_instruction += character

    print('FOUND FUNCTION "%s" %s/1 similar to instruction "%s"' % (new_instruction, round(rankings[0][1], 2), instruction))
    return new_instruction

async def search_exec(meep, instruction, search_category=""):
    """
    action
    searches the most similar function (to the instruction) and executes it.
    if the function is a getter, uses fetch talk to display its result
    """
    new_instruction = await meep.FETCH("basic input manager : find function", instruction, search_category)
    category = await meep.FETCH("modules : get function category", new_instruction)

    if category == "listener":
        print('SEARCH EXEC : couldnt execute "%s" because it was a listener' % instruction)
    elif category == "action":
        meep.EXECUTE(new_instruction)
    else:
        meep.EXECUTE("talker : fetchtalk", new_instruction)

async def search_return(meep, instruction):
    """
    getter
    gets the result of the function which resembles the instruction the most
    """
    new_instruction = await meep.FETCH("basic input manager : find function", instruction, category="getter")
    return await meep.FETCH(new_instruction)


