# LuaTblParser

1 The program is implemented by python 2.7.10. Its main function is to read the Lua table string expression and then parse it to the python dictionary to store the data;
2 load(self, s): read the Lua table string expression and then parse it to the python dictionary(self.dict) to store the data;
3 loadLuaTable(self, f): read the Lua table string expression from the file f and then call load to parse it;
4 dump(self): return the Lua table expression corresponding to the dictionary(self.dict);
5 dumpLuaTable(self, f): write the Lua table string expression obtained from dump function into the file f;
6 loadDict(self, d): read the input dictionary d, only considering the data whose key is numeric or string, and transfer the data to the Lua table string expression and then call load function to get the corresponding dictionary;
7 dumpDict(self): return the dictionary who is a deep copy of the self.dict;
8 __setitem__(self, key, value): support the assignment or write operation by '[]';
9 __getitem__(self, item): support the read operation by '[]';
10 update(self, d): update the self.dict by the input dictionary d.
