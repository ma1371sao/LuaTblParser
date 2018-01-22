from PyLuaTblParser import *
#testing

a1 = PyLuaTblParser()
a2 = PyLuaTblParser()
a3 = PyLuaTblParser()

test_str = '{",,,",arr,ssr=nil,nil,ay = {0x6A,23,5,nil,},[",,,"]="ssr",dict = {mixed = {43,54.33,nil,false,9,string= "v\{}=alue",nil,},array = {3,6,4,},string = "value",},nil,}'
test_str1 = '{",,,",arr,ay = {0x6A,23,5,},dict = {mixed = {43,54.33,false,9,string= "v\{}=alue",},array = {3,6,4,},string = "value",},}'
test_str3 = ''
test_str4 = '{0xBEBADA,0xff,314.16e-2,0.31416E1,34e1,0x0.1E,0xA23p-4,0X1.921FB54442D18P+1}'
test_str5 = '{[10]={"r","sr",{1,2,3,},},22,33.5,dict={mixed={1,2,3},40.5,},13,nil,}'
test_str6 = '{root={"Test Pattern String",{["object with 1 member"] = {"array with 1 element",},},{},[99] = -42,},}'
#test_str8 = '{['root']={[96]={{},1,2,nil},[97]={{},{}},[98]={{}},[99]=-42,[4]=true,[5]=false,[1]='Test Pattern String',[8]=0.5,[9]=3.14159265359e+64,[10]=3.14159265359,[7]={['comment']='// /* <!-- --',['false']=false,['backslash']='\\\\',['one']=1,['quotes']='&#34; (0x0022) %22 0x22 034 &#x22;',['zero']=0,['integer']=1234567890,['array']={nil,nil},['# -- --> */']=' ',['special']='`1~!@#$%^&*()_+-={\\' ,]}|;.</>?',['compact']={1,2,3,4,5,6,7},['space']=' ',['hex']='0x01230x45670x89AB0xCDEF0xabcd0xef4A',['controls']='\\b\\f\\n\\r\\t',['slash']='/ & \\\\',['real']=-9876.54321,['digit']='0123456789',['E']=1.23456789e+34,['quote']='\\"',['object']={},['address']='50 St. James Street',['alpha']='abcdefghijklmnopqrstuvwyz',['\\\\\\"\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\\',./<>?']='A key can be any string',['true']=true,['luatext']='{\\"object with 1 member\\" = {\\"array with 1 element\\"}}',['e']=1.23456789e-13,['url']='http://www.JSON.org/',[' s p a c e d ']={1,2,3,4,5,6,7},['ALPHA']='ABCDEFGHIJKLMNOPQRSTUVWYZ'},[12]='rosebud',[2]={['object with 1 member']={'array with 1 element'}},[11]=1066,[3]={},[94]={[1]={['1']=1,['2']=2},['3']=3,[2]={[1]=1,['2']=2}},[95]={1,2,{['1']=1}}}}'
a1.load(test_str)
a1.loadLuaTable('testcaseraw.lua')
d1 = a1.dumpDict()
print 'd1: '
print d1

a2.loadDict(d1)
#print 'a2: '
#print a2.dict
a2.dumpLuaTable('input1.txt')
a3.loadLuaTable('input1.txt')
#print 'a3: '
#print a3.dict
d3 = a3.dumpDict()
print 'd3: '
print d3

print a1['root'][96]
a1[100] = 1
print 'a1.dict:'
print a1.dict

d = {1:2000}
a1.update(d)
print 'a1.dict:'
print a1.dict
