import re
import copy

# >general
def pyfreadlines(filepath):
    with open(filepath,"r") as f:
        return f.readlines()

class parseitem:
    def __init__(self,left_item,right_items):
        self.left_item = left_item
        self.right_items = right_items
        self.dotpos = 0

    def __eq__(self,parseitem):
        if(len(self.right_items) != len(parseitem.right_items) or self.left_item != parseitem.left_item):
            return False
        for i in range(len(self.right_items)):
            if(self.right_items[i] != parseitem.right_items[i]):
                return False
        return True

    def getcurrent(self):
        return self.right_items[self.dotpos] if self.dotpos < len(self.right_items) else None

    def goto(self):
        self.dotpos += 1

    def equal(self,parseitem):
        return self.__eq__(parseitem)

class parsestate:
    def __init__(self,items):
        self.items = items
        self.transision = []

    def append_transision(self,state):
        self.transision.append(state)

    def equal(self,state):
        if(len(self.items) != len(state.items)):
            return False
        for i in range(len(self.items)):
            if(not self.items[i].equal(state.items[i])):
                return False
        return True

r = re.compile("[ 　\t\n\r]")
def remove_blank(st):
    return r.sub("",st)

def remove_blank_item(data):
    i = 0
    while i < len(data):
        data[i] = remove_blank(data[i])
        if(data[i] == ""):
            del data[i]
            continue
        i += 1
    return data

def split_rule(line):
    ret = line.split("->")
    if(len(ret) <= 1):
        return None
    return [remove_blank(ret[0]),remove_blank_item(ret[1].split(" "))]

def dict_insert(src,key,value=True):
    if(src.get(key) == None):
        src[key] = value

def generate_parsegrammer(data):
    ret = dict()
    for i in data:
        rt = split_rule(i)
        if(rt):
            dict_insert(ret,rt[0],[])
            ret[rt[0]].append(rt[1])
    return ret

def generate_items(grammer,first_item):
    if(type(first_item) != type([])):
        first_item = [first_item]

    items = first_item
    lefts = [i.getcurrent() for i in first_item if i.getcurrent()]
    i = 0
    while(i < len(lefts)):
        tgt = grammer.get(lefts[i])
        #再帰ルールのガード
        if(tgt):
            for j in tgt:
                items.append(parseitem(lefts[i],j))
                if(lefts[i] != j[0]):
                    lefts.append(j[0])
        
        i += 1
    return items

def generate_parsestate(grammer,first_item):
    return parsestate(generate_items(grammer,first_item))

def getcurrentrules(grammer,state):
    ret = dict()
    for i in state.items:
        nx = i.getcurrent()
        if(nx):
            newitem = copy.copy(i)
            if(ret.get(nx) == None):
                ret[nx] = []
            if(newitem not in ret[nx]):
                ret[nx].append(newitem)
    return ret

def generate_nextstate(grammer,state):
    rules = getcurrentrules(grammer,state)
    ret = []
    for i,j in rules.items():
        for k in range(len(j)):
            j[k].goto()
        ret.append(generate_parsestate(grammer,j))
    return ret

def duplicade_state(state1,state2):
    return state1.equal(state2)

def parsemain(filepath):
    data = pyfreadlines(filepath)
    grammer = generate_parsegrammer(data)
    parsestatelist = [generate_parsestate(grammer,parseitem("S",grammer["S"][0][0]))]
    cnt = 0
    while cnt < len(parsestatelist):
        nextstatelist = generate_nextstate(grammer,parsestatelist[cnt])
        for i in nextstatelist:
            flg = False
            for j in range(len(parsestatelist)):
                if(duplicade_state(i,parsestatelist[j])):
                    if(i not in parsestatelist[j].transision):
                        parsestatelist[j].append_transision(i)
                    flg = True
            if(not flg):
                parsestatelist.append(i)
                parsestatelist[cnt].append_transision(i)
        cnt += 1
    

# >goto


def generate_gototable(states):
    
if __name__ == "__main__":
    ret = parsemain("/home/takatama-a/myfile/c_cpp/test.txt")
