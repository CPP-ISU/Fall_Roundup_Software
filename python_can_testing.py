import cantools
db = cantools.database.load_file('Tractor.dbc')
#print(db.messages[0].signals)
bindings=[None] * 0xFFFFFF
#print(len(bindings))
for msg in db.messages:
    #print(f"Message: {msg}")
    id=msg.frame_id
    SA=id&0xFF
    if id==0xFE:
        bindings[id&0xFFFF00:id&0xFFFF00+0xFF]=msg
    else:    
        bindings[id&0xFFFFFF]=msg



print(bindings[0xff9376])

