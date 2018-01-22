class PyLuaTblParser():

    """
    Shijie Ma
    Dec 19, 2017
    """
    
    def __init__(self):
        self.dict = {}
        self.ch = ''
        self.pos = 0
        self.pre = -1
        self.strExp = ''
        self.transTable = {'\a': r'\a', '\b': r'\b', '\f': r'\f', '\n': r'\n',
                         '\r': r'\r', '\t': r'\t', '\v': r'\v', '\\': r'\\',
                         '\'': r'\'','\"': r'\"', '[': r'\[', ']': r'\]'}
        self.dict_stack = [0]
        self.indent_num = 4

    def eraseComment(self, s):
        erasedStr = ''
        numQm = 0
        start = -1
        end = 0
        i = 0
        while i < len(s):
            if numQm == 0:
                if s[i] == '\"':
                    numQm += 1
                elif i + 1 < len(s) and s[i:i+2] == '--':
                    start = i
                    erasedStr += s[end:start]
                    if i + 3 < len(s) and s[i:i+4] == '--[[':
                        end = s.find(']]', i)
                        if end == -1: 
                            end = len(s)
                        else: 
                            end += 2
                    else:
                        end = s.find('\n', i)
                        if end == -1:
                            end = len(s)
                        else:
                            end += 1
                    i = end - 1
            else:
                if s[i] == '\"' and s[i - 1] != '\\':
                    numQm -= 1
            i += 1
        erasedStr += s[end:len(s)]
        return erasedStr

    def str_to_num(self, s):
        """
        used to transfer string s to int or float
        if failed, throw exception
        """

        err_msg = '\"' + s + '\" cannot be converted to a number'
        try:
            num_int = int(s,0)
        except:
            try:
                num_float = float(s)
            except:
                raise Exception(err_msg)
            else:
                return num_float
        else:
            return num_int
    
    def parseToken(self):
        char = self.nxtCh()
        token_str = ""
        while char and (char.isalnum() or char == '_'):
            token_str += char
            char = self.nxtCh()
        if char is not None:
            self.pos -= 1
        return token_str
 
    def parseLuaStrWithEqualNum(self, equal_num):
        ret_string = ''
        char = self.nxtCh()
        while True:
            if char is None:
                raise Exception('invalid lua xstring')
            elif char == ']':
                tem_str, i = ']', equal_num
                nxtCh = self.nxtCh()
                while nxtCh is not None:
                    if i == 0:
                        break
                    if nxtCh != '=':
                        break
                    i -= 1
                    tem_str += nxtCh
                    nxtCh = self.nxtCh()
                if i == 0 and nxtCh == ']':
                     return ret_string
                elif nxtCh is None:
                    raise Exception('invalid lua xstring')
                else:
                    ret_string += tem_str
                    char = nxtCh
                    continue
            if char == '\\':
                char += '\\'
            ret_string += char
            char = self.nxtCh()
       

    #return (return_string with "" and boolean indicating if it is good lua string)
    #lua string ::= [[...]] | [=[...]=] | ..
    def parseLuaStr(self):
        prev, at = self.pre, self.pos
        char = self.nxtCh()
        if char != '[':#char ==  '['
            raise Exception('lua string error')
        char = self.nxtCh()
        equal_num = 0
        while char == '=':
            equal_num += 1
            char = self.nxtCh()
            if char is None:
                break
        if char == '[':
            # if we are not a xstring, then a ParerError will be raised
            text = self.parseLuaStrWithEqualNum(equal_num)
            return '"' + text + '"', True
        self.pre, self.pos = prev, at
        return '', False

    def parseHex(self):
        intStr = ''
        hex_digit_str = "aAbBcCdDeEfF"
        while self.ch and (self.ch.isdigit() or self.ch in hex_digit_str):
            intStr += self.ch;  
            self.nxtCh()
        return intStr

    def makeDigit(self):
        num_str = ''
        if self.parseCh('-'):
            num_str = '-'
            num_str += self.nxtCh()
        num_str += self.parseDigits()
        is_int = True
        if num_str == '0' and self.ch in ['x','X']:
            num_str += self.ch
            self.nxtCh()
            num_str += self.nxtCh()
            num_str += self.parseHex()
        else:
            if self.parseCh('.'):
                is_int = False
                num_str += '.'
                num_str += self.nxtCh()
                num_str += self.parseDigits()
            if self.ch and self.ch in ['e', 'E']:
                is_int = False
                num_str += self.ch
                self.nxtCh()
                if self.ch and self.ch  in ('+', '-'):
                    num_str += self.ch
                    self.nxtCh()
                num_str += self.nxtCh()
                num_str += self.parseDigits()
        try:
            if is_int:
                return int(num_str)
            else:
                return float(num_str)
        except:
            pass
   
    #digit string 's correctness is hanled by str_to_num function.
    def parseDigit(self):
        ret_str = ''
        char = self.ch
        if char.isdigit():
            ret_str += self.parseDigits()
            if ret_str == '0' and self.ch in ['x','X']:
                ret_str += self.ch
                self.nxtCh()
                ret_str += self.parseHex()
            else :
                ret_str += self.parseDigits()
        elif char in '+-':
            ret_str += char
            self.nxtCh()
            ret_str += self.parseDigits()
        char = self.ch
        if char == '.':
            ret_str += char
            self.nxtCh()
            ret_str += self.parseDigits()
        char = self.ch
        if char in 'eE':
            ret_str += char
            self.nxtCh()
            nxtCh = self.ch
            if nxtCh.isdigit():
                ret_str += self.parseDigits()
            elif nxtCh in '+-':
                ret_str += nxtCh
                self.nxtCh()
                ret_str += self.parseDigits()
        try:
            self.str_to_num(ret_str)
        except:
            raise Exception("digitError")
        
        self.pos -= 1 #next char point to the char next to digit array
        return ret_str
   
    def parseExp(self):
        char = self.nextValidCh()
        if char == '{':
            self.preValidCh()
            table_str,_,_ =  self.parseTable()
            return table_str
        
        elif char in '\'\"':
            return self.parseBracket(char)
        elif char.isdigit() or char in '-+.':
            return self.parseDigit()
        elif char.isalpha() or char == '_':
            self.preValidCh()
            token_str = self.parseToken()
            return token_str
        elif char == '[':
            self.preValidCh()
            str,lua_ok = self.parseLuaStr()
            if lua_ok:
                return str
            else:
                raise Exception("lua Error")
             
        raise Exception("expresion Error")

    def isKeyValid(self, key):
        n = len(key)
        if n == 0 :
            return False
        if not (key[0].isalpha() or  key[0] == '_'):
            return False
        for char in key[1:]:
            if not (char.isalnum() or char == '_'):
                return False
        return True
           
    def parseFields(self):
        '''
        field ::= '[' former ']' '=' later | expr1 '=' later | later, return (expr1,later)
        '''
        field_str = ''
        former = None 
        later = ''
        char = self.nextValidCh()
        if char == '[':
            self.pos -= 1
            xstr, ok = self.parseLuaStr()
            if ok:  # we get a xstring
                later += xstr
                field_str = later
            else:
                self.nxtCh()
                key = self.parseExp()
                nxtCh = self.nextValidCh()
                if nxtCh == ']':
                    former = key
                    if self.nextValidCh() != '=':
                        raise Exception('invalid table field')
                    later = self.parseExp()
                    field_str = '[' + former + ']' + '= ' + later
                else:
                    raise Exception('invalid table field_str')
        else:
            self.preValidCh()
            former = self.parseExp()
            validCh = self.nextValidCh()
            if validCh == '=':
                if not self.isKeyValid(former):
                    raise Exception('invalid variable name : ' + former)
                later = self.parseExp()
                field_str = former + '= ' + later
            elif validCh is not None:
                self.preValidCh()
                former, later = None, former
                field_str = later
            else:
                raise Exception('invalid table field_str')

        char = self.nextValidCh()
        if char not in ',;}':
            raise Exception('syntax error near \"' + later + '\"')
        else:
            self.pos -= 1
        return field_str, (self.parseKey(former), self.parseExpr(later))

    
    # return (tableString, [(expr_key_1,expr_value_1),(expr_key_2,expr_value_2).. ]) 
    def parseTable(self):
        '''
        tableconstructor ::= `{? [fieldlist] `}?
        fieldlist ::= field {fieldsep field} [fieldsep]
        field ::= `[? exp `]? `=? exp | Name `=? exp | exp
        fieldsep ::= `,? | `;?
        '''
        table_str = '{'
        expresions = []
        char = self.nextValidCh()
        if char != '{':
            raise Exception('table error ')
        while True:
            char = self.nextValidCh()
            if char is None:
                raise Exception('a table must end with \'}\'')
            elif char == '}':
                break
            else:
                self.preValidCh()
                field_text, field_expr = self.parseFields()
                table_str += field_text
                expresions.append( field_expr)
            char = self.nextValidCh()
            if char in ',;':
                if self.nextValidCh() == '}':
                    break
                self.pos -= 1
            elif char == '}':
                break
            else:
                raise Exception('table error')
            table_str += ','
        table_str += '}'
        containers,dump_str = self.getContainer(expresions)
        return table_str,containers,dump_str 

    def isStringSymmetry(self, s):
        n = len(s)
        if n >1:
            return  s[0] in '\'\"' and s[n-1] in '\'\"' and s[0] == s[n-1]
        else:
            return False

    def nextValidCh(self):
        self.skipBlank()
        temp = self.pos
        while self.skipComment():
            self.skipBlank()
            temp = self.pos
        self.pre = temp
        return self.nxtCh()

    def preValidCh(self):
        self.pos = self.pre
        if self.pos == -1:
            raise Exception('Bug in back valid char')

    def parseCh(self, char):
        if self.ch and char == self.ch:
            self.nxtCh()
            self.ch = self.strExp[self.pos]
            return True
        return False

    #return the current one, index ++
    def nxtCh(self):
        if self.pos >= len(self.strExp):
            self.ch = None
            return None
        self.ch = self.strExp[self.pos]
        self.pos += 1
        return self.ch

    def skipComment(self):
        if self.parseCh('-'):
            if self.parseCh('-'):
                self.do_skipComment()
                return True
            else:
                self.pos -= 1
        else:
            return False

    def parseBracket(self, endChar):
        ret_str = '"'
        mark = endChar
        while True:
            char = self.nxtCh()
            if char is None:
                raise Exception('a string must end with \' or \"')
            elif char == mark:
                break
            elif char in '\'\"':
                ret_str += '\\' + char
            elif char == '\\': 
                ret_str += '\\' + self.nxtCh()
            else:
                ret_str += char
        ret_str += '"'
        return ret_str

    def skipLines(self, num):
        char = self.nxtCh()
        while char is not None:
            if char in '\'\"':
                self.pos -= 1
                self.parseBracket(char)
            elif char == ']':
                nxtCh = self.nxtCh()
                count = num
                while nxtCh == '=' and count >0:
                    count -=1
                    self.nxtCh()
                if  (count == 0 and self.ch == ']') or nxtCh is None:
                    return
                elif nxtCh == ']':
                    continue
            char = self.nxtCh()
        
            
    def do_skipComment(self):
        if self.parseCh('['):
            bracket_num = 0
            while self.ch and self.parseCh("="):
                bracket_num+= 1
            if self.parseCh('['):
                self.skipLines(bracket_num)
            else:
                self._skip_line()
        else:
            char = self.nxtCh()
            while char and char!= '\n':
                char = self.nxtCh()

   
    def parseKey(self, index):
        if index == None:
            return None
        # the table index must be a string or a number
        n = len(index)
        if self.isStringSymmetry(index):
            return self.parseStr(index[1:n-1])
        else:
            try:
                return self.str_to_num(index)
            except:
                return index
               
    def parseExpr(self, expr):
        if expr == 'true':
            return True
        elif expr == 'false':
            return False
        elif expr == 'nil':
            return None
        if len(expr) > 0 and expr[0] == '{':  # tabl
            table_parser =  PyLuaTblParser()
            table_parser.strExp = expr
            _,expr_str,_ = table_parser.parseTable()
            return expr_str
        else:
            return self.parseKey(expr)

    def parseStr(self, str):
        charMap = dict((v, k) for k, v in self.transTable.iteritems())
        ret = ''
        n, index = len(str), 0
        while index < n:
            if str[index] == '\\':
                test_idx = index + 1
                if test_idx < n:
                    nxtCh = str[test_idx]
                    if nxtCh.isdigit():
                        char_str, max_leng = '', 3
                        while nxtCh.isdigit():
                            char_str += nxtCh
                            test_idx += 1
                            if test_idx < n:
                                nxtCh = str[test_idx]
                            else:
                                break
                            max_leng -= 1
                            if max_leng == 0:
                                break
                        char = int(char_str)
                        if char > 255:
                            raise Exception('char error')
                        ret +=  chr(char)
                    
                    else:
                        if charMap.has_key('\\' + nxtCh):
                            ret += charMap['\\' + nxtCh]
                        else:
                            ret += ('\\' + '\\' + nxtCh)
                    index = test_idx
                    
                else:
                    ret += '\\'
                    break
            else:
                ret += str[index]
            index += 1
        return ret

    def getContainer(self, expression_list):
        dct = dict((k,v) for (k,v) in expression_list if k is not None and v is not None)
        lst = [v for (k,v) in expression_list if k is None]
        if len(dct) == 0:
            return lst,'{' + ','.join([self.valDump(item) for item in lst]) + '}'
        elif len(lst) == 0:
            cpy_stack = self.dict_stack
            self.dict_stack = [0]
            self.indent_num = 4
            ret_str = dct,self.dictDump(dct)
            self.dict_stack = cpy_stack
            return ret_str
        else:
            for i in range(len(lst)):
                if lst[i] is not None:
                    dct[i+1] = lst[i]
            cpy_stack = self.dict_stack
            self.dict_stack = [0]
            self.indent_num = 4
            ret_str = dct,self.dictDump(dct)
            self.dict_stack = cpy_stack
            return ret_str

    def load(self, s):
        self.dict.clear()
        #s = self.eraseComment(s)
        parser = PyLuaTblParser()
        parser.strExp = s
        _,self.dict,self.dump_str = parser.parseTable()
        self.scan(self.dict)

    """
    scan the dictionary and delete the items whoes key is not a string or a number and whose value is None
    """
    def scan(self, target):
        if isinstance(target, list):
            self.scanList(target)
        elif isinstance(target, dict):
            self.scanDict(target)

    def scanList(self, targetList):
        for i in targetList:
            if isinstance(i, list):
                self.scanList(i)
            elif isinstance(i, dict):
                self.scanDict(i)

    def scanDict(self, targetDict):
        for i in targetDict:
            if not isinstance(i, (int, float, str)) or targetDict[i] == None:
                del targetDict[i]
            elif isinstance(targetDict[i], list):
                self.scanList(targetDict[i])
            elif isinstance(targetDict[i], dict):
                self.scanDict(targetDict[i])

    def loadLuaTable(self, f):
        """
        load lua table from input string f(file path)
        """
        file_object = open(f, 'r')
        try:
            str_luaTable = file_object.read()
        except:
            raise Exception('read file: ' + '\"' + f + '\"' + ' failed')
        else:
            file_object.close()
        #print 'string from loadLuaTable:'
        #print str_luaTable
        self.load(str_luaTable)

    def dump(self):
        """
        return lua table string expression according to self.dict
        """
        return self.dump_str

    def dumpLuaTable(self, f):
        """
        write lua table string obtained from self.dict to the input file path(f)
        """
        str_luaTable = self.dump()
        file_object = open(f, 'w')
        try:
            file_object.write(str_luaTable)
        except:
            raise Exception('write file: ' + '\"' + f + '\"' + ' failed')
        else:
            file_object.close()

    def charDump(self, c):
        if self.transTable.has_key(c):
            return self.transTable[c]
        return c

    def dictDump(self, dct):
        length = len(dct)
        keys = dct.keys()
        if self.indent_num > 0:
            is_indented = True
        else:
            is_indented = False
        last_indent = self.dict_stack[len(self.dict_stack) - 1]
        ret = ' '*(last_indent) +'{'
        if length == 1:
            key = keys[0]
            ret += self.keyDump(key) + '='
            if is_indented:
                ret += ' '
            ret += self.valDump(dct[key])
        elif length != 0:
            new_indent = last_indent + self.indent_num
            self.dict_stack.append(new_indent)
            stringVec = []
            for key in keys:
                key_string = ''
                if is_indented:
                    key_string += '\n'
                key_string += ' '*(new_indent) + self.keyDump(key) + '='
                if is_indented:
                    key_string += ' '
                key_string += self.valDump(dct[key])
                stringVec.append(key_string)
            ret += ','.join(stringVec)
            if is_indented:
                ret += '\n'
            ret += ' '*(last_indent)
            self.dict_stack.pop()
        ret += '}'
        return ret

    def valDump(self, value):
        if isinstance(value, bool):
            if value:
                return 'true'
            else:
                return 'false'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return r'"' + ''.join([self.charDump(c) for c in value]) + r'"'
        elif isinstance(value, list):
            cpy_stack = self.dict_stack
            self.dict_stack = [0]
            self.indent_num = 4
            ret_str =  '{' + ','.join([self.valDump(item) for item in value]) + '}'
            self.dict_stack = cpy_stack
            return ret_str
        elif isinstance(value, dict):
            return self.dictDump(value)
        else:
            return 'nil'

    def keyDump(self, index):
        if isinstance(index, (float, int)):
            return '[' + str(index) + ']'
        elif isinstance(index, str):
            return r'["'  + ''.join([self.charDump(c) for c in index]) + r'"]'
        else:
            return Exception('the table index must be a string or a number')

    def skipBlank(self):
        char = self.nxtCh()
        while char is not None and char.isspace():
            char = self.nxtCh()
        if char is not None:
            self.pos -= 1

    def parseDigits(self):
        intStr = ''
        while self.ch and self.ch.isdigit():
            intStr += self.ch;    
            self.nxtCh()
        return intStr

    def loadDict(self, d):
        self.scan(d)
        cpy_stack = self.dict_stack
        self.dict_stack = [0]
        self.indent_num = 4
        s = self.dictDump(d)
        self.dict_stack = cpy_stack
        self.load(s)
    
    def copyDict(self, source):
        """
        copy the data from source to dict
        """
        if isinstance(source, dict):
            targetDict = {}
            for i in source:
                if isinstance(i, (int, float, str)) and source[i] != None:
                    if isinstance(source[i], (int, float, str, bool)):
                        targetDict[i] = source[i]
                    elif isinstance(source[i], list):
                        targetDict[i] = self.copyDict(source[i])
                    elif isinstance(source[i], dict):
                        targetDict[i] = self.copyDict(source[i])
                    else:
                        raise Exception('Error: lua table format error')
            return targetDict
        elif isinstance(source, list):
            targetList = []
            for i in source:
                if i == None:
                    targetList.append(None)
                elif isinstance(i, (int, float, str, bool)):
                    targetList.append(i)
                elif isinstance(i, list):
                    targetList.append(self.copyDict(i))
                elif isinstance(i, dict):
                    targetList.append(self.copyDict(i))
            return targetList

    def dumpDict(self):
        """
        return a dictionary who has the data in self.dict
        """
        copiedDict = self.copyDict(self.dict)
        #print copiedDict
        return copiedDict

    def __setitem__(self, key, value):
        self.dict[key] = value
        self.loadDict(self.dict)
        #print '__setitem__'

    def __getitem__(self, item):
        #print '__getitem__'
        if isinstance(self.dict, list):
            n = len(self.dict)
            if not isinstance(item, int) or item < 1 or item > n:
                raise Exception('table index out of range')
            else:
                return self.dict[item-1]
        else:
            return self.dict[item]

    def update(self, d):
        if isinstance(self.dict, dict):
            self.dict.update(d)
            self.loadDict(self.dict)
        else:
            raise Exception('list not support the update from a dict')

