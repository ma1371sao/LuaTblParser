{
root = {
	"Test Pattern String",
	-- {"object with 1 member" = {"array with 1 element",},},
	{["object with 1 member"] = {"array with 1 element",},},
	{},
	[99] = -42,
	[98] = {{}},
	[97] = {{},{}},
	[96] = {{}, 1, 2, nil},
	[95] = {1, 2, {["1"] = 1}},
	[94] = { {["1"]=1, ["2"]=2}, {1, ["2"]=2}, ["3"] = 3 },
	true,
	false,
	nil,
	{
		["integer"]= 1234567890,
		real=-9876.543210,
		e= 0.123456789e-12,
		E= 1.234567890E+34,
		zero = 0,
		one = 1,
		space = " ",
		quote = "\"",
		backslash = "\\",
		controls = "\b\f\n\r\t",
		slash = "/ & \\",
		alpha= "abcdefghijklmnopqrstuvwyz",
		ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWYZ",
		digit = "0123456789",
		special = "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
		hex = "0x01230x45670x89AB0xCDEF0xabcd0xef4A",
		["true"] = true,
		["false"] = false,
		["nil"] = nil,
		array = {nil, nil,},
		object = {  },
		address = "50 St. James Street",
		url = "http://www.JSON.org/",
		comment = "// /* <!-- --",
		["# -- --> */"] = " ",
		[" s p a c e d " ] = {1,2 , 3

			,

			4 , 5        ,          6           ,7        },
		--[[[][][]  Test multi-line comments
			compact = {1,2,3,4,5,6,7},
	- -[luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"]
		= "A key can be any string"]]
	--         ]]
		compact = {1,2,3,4,5,6,7},
		luatext = "{\"object with 1 member\" = {\"array with 1 element\"}}",
		quotes = "&#34; (0x0022) %22 0x22 034 &#x22;",
		["\\\"\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"]
		= "A key can be any string"
	},
	0.5 ,31415926535897932384626433832795028841971693993751058209749445923.
	,
	3.1415926535897932384626433832795028841971693993751058209749445923
	,

	1066


	,"rosebud"

}}