from asyncio import sleep

TENSORFLOW = True

if TENSORFLOW: #les instances des interfaces doivent etres fournies par meep
    import interfaces.spacy_word2vec #les pipelines ne sont pas instanciees, donc peuvent etre importees une fois ici; 


async def dire_pas_de_fonction(meep):
    #GET CONTENT ======================
    logs = meep.mem.get_logs()
    #TEST CONTENT =====================
    name = ""
    for log in logs:
        if "pas de fonction" in log['tags']:
            name = log['variable']
            break
    #INTERACT AND OUTPUT ==============
    if name == "":
        print('pas de log avec le tag "pas de fonction"')
    else:
        print(f"on n'a pas ecrit la fonction pour aller avec la bulle ''{name}''")
    return []

#======================================================================

async def message_sur_discord(meep):    
    return ['Yes']

async def dire_word2vec_pas_resultat(meep):
    discord = meep.interfaces['Discord']
    print("word2vec ne trouve pas de resultat")

async def envoyer_sur_discord(meep):
    discord = meep.interfaces['Discord']
    message = discord.temporary_message_history[-1]['content'] #str

    if TENSORFLOW:
        response = interfaces.spacy_word2vec.phrase_proche(message)
    else:
        response = message

    for id, name in discord.identifiers.get()["users"].items():
        if "Rouf" in name:
            await discord.send(id, 'message : '+response, userid=True)
            break
    return []

async def faut_il_envoyer(meep):
    return ['Yes']

async def choisir_une_reponse(meep):
    return []

async def veut_envoyer_message(meep):
    return ['Yes']

