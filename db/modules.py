import rethinkdb as r

rcon = None
table = ""

def msgPusher(msgs):
    for msg in msgs:
        r.table(table).insert({
            "message": msg,
            "label": []
        }).run(rcon)
    return

def msgListGet():
    res = []
    for doc in r.table(table).pluck("message", "id").run(rcon):
        res.append(doc)
    return res

def classPusher(id, cls):
    hasID = r.table(table).filter(r.row['id']==id).count().run(rcon)
    if hasID > 0:
        r.table(table).get(str(id)).update({
            "label": r.row["label"].append(cls)
        }).run(rcon)
    return