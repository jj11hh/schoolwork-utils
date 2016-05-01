import random

def make_child(male,female):
    child=""

    if len(male)!=len(female):
        raise ValueError

    for i in range(len(male)):
        if male[i].isupper():
            child+=male[i]
            child+=female[i]
        else:
            child+=female[i]
            child+=male[i]
    return child
def make_p(pure):
    pure=pure.upper()
    result=[]
    if pure=="":return result
    if len(pure)==1:return [pure[0],pure[0].lower()]
    for c in pure[0],pure[0].lower():
        result.extend([c+i for i in make_p(pure[1:])])
    return result
def make_all_children(listofp):
    children=[]
    k=0
    for p1 in listofp:
        for j in range(k,len(listofp)):
            t=make_child(p1,listofp[j])
            if not t in children:
                children.append(t)
        k+=1
    return children
        
def make_record(pure):
    pure=pure.upper()
    male=""
    female=""
    child=""
    for c in list(pure):
        if random.randint(0,1):
            male+=c.lower()
        else:
            male+=c
        if random.randint(0,1):
            female+=c.lower ()
        else:
            female+=c
        if male[-1]==c:
            child+=male[-1]
            child+=female[-1]
        else:
            child+=female[-1]
            child+=male[-1]

    return (male,female,child)

def make_total(records):
    pure=records[0][0].upper()
    listofp=make_p(pure)
    all_children=make_all_children(listofp)
    fathers=dict([(a,[]) for a in listofp])
    mothers=dict([(a,[]) for a in listofp])
    children=dict([(a,[]) for a in all_children])

    total={"mother":dict([(a,0) for a in listofp]),
           "father":dict([(a,0) for a in listofp]),
           "child":dict([(a,0) for a in all_children])}

    for record in records:
        for father in fathers.iterkeys():
            if father==record[0]:
                fathers[father].append(1)
                total["father"][father]+=1
            else:fathers[father].append(0)
        for mother in mothers.iterkeys():
            if mother==record[1]:
                mothers[mother].append(1)
                total["mother"][mother]+=1
            else:mothers[mother].append(0)
        for child in children.iterkeys():
            if child==record[2]:
                children[child].append(1)
                total["child"][child]+=1
            else:children[child].append(0)
            
    return (fathers,mothers,children,total)
    
def sprint_records(records):
    pure=records[0][0].upper()
    listofp=make_p(pure)
    all_children=make_all_children(listofp)
    fathers,mothers,children,total=make_total(records)
    
    page=""
    
    bar=""
    for p in listofp:
        bar+=" "+p

    bar="Number |"+bar+" |"+bar+" | "+" ".join(all_children)
    page+= bar+"\n"
    page+="="*len(bar)+"\n"

    for i in range(len(records)):
        line="No."+" "*(4-len(str(i+1)))+str(i+1)+"|"
        for father in listofp:
            line+=" "+str(fathers[father][i])+" "*(len(pure)-1)
        line+=" |"
        for mother in listofp:
            line+=" "+str(mothers[mother][i])+" "*(len(pure)-1)
        line+=" |"
        for child in all_children:
            line+=" "+str(children[child][i])+" "*(len(pure)*2-1)
        page+=line+"\n"

    page+="="*len(bar)+"\n"

    page+="Total: "+bar[7:]+"\n"

    line="       |"
    for father in listofp:
        line+=" "+str(total["father"][father])
    line+=" |"
    for mother in listofp:
        line+=" "+str(total["mother"][mother])
    line+=" |"
    for child in all_children:
        line+=" "+str(total["child"][child])
    page+=line+"\n"
    
    return page
    
    
def sprint_records_as_html(records):
    pure=records[0][0].upper()
    listofp=make_p(pure)
    all_children=make_all_children(listofp)
    fathers,mothers,children,total=make_total(records)
    
    page=""
    
    bar=""
    for p in listofp:
        bar+="<th>"+p+"</th>\n"

    bar="<tr>"+"<th>Number</th>\n"+bar+bar+"<th>"+"</th>\n<th>".join(all_children)+"</th>\n</tr>\n"
    page+=bar+"\n"

    for i in range(len(records)):
        line="<td>"+str(i+1)+"</td>"
        for father in listofp:
            line+="<td>"+str(fathers[father][i])+"</td>\n"
        for mother in listofp:
            line+="<td>"+str(mothers[mother][i])+"</td>\n"
        for child in all_children:
            line+="<td>"+str(children[child][i])+"</td>\n"
        page+=line.join(["<tr>","</tr>"])+"\n"
    page+="<tr>"+"Total:".join(["<th>","</th>\n"])+bar[19:]+"\n"
    line="<td></td>"
    for father in listofp:
        line+="<td>"+str(total["father"][father])+"</td>\n"
    for mother in listofp:
        line+="<td>"+str(total["mother"][mother])+"</td>\n"
    for child in all_children:
        line+="<td>"+str(total["child"][child])+"</td>\n"
    page+="<tr>"+line+"</tr>\n"
    
    return "<html><body><table border=\"1\">"+page+"</table></body></html>"

def make_n_records(count,genes):
    records=[]
    for i in range(count):
        records.append(make_record(genes))
    return records
        
 
