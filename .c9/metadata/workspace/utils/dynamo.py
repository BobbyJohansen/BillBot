{"filter":false,"title":"dynamo.py","tooltip":"/utils/dynamo.py","undoManager":{"mark":80,"position":80,"stack":[[{"start":{"row":12,"column":28},"end":{"row":12,"column":29},"action":"insert","lines":[" "],"id":2}],[{"start":{"row":12,"column":29},"end":{"row":12,"column":30},"action":"insert","lines":["a"],"id":3}],[{"start":{"row":12,"column":30},"end":{"row":12,"column":31},"action":"insert","lines":["s"],"id":4}],[{"start":{"row":12,"column":31},"end":{"row":12,"column":32},"action":"insert","lines":[" "],"id":5}],[{"start":{"row":12,"column":32},"end":{"row":12,"column":33},"action":"insert","lines":["s"],"id":6}],[{"start":{"row":12,"column":33},"end":{"row":12,"column":34},"action":"insert","lines":["t"],"id":7}],[{"start":{"row":12,"column":34},"end":{"row":12,"column":35},"action":"insert","lines":["r"],"id":8}],[{"start":{"row":2,"column":5},"end":{"row":2,"column":12},"action":"remove","lines":["AWSCore"],"id":9},{"start":{"row":2,"column":5},"end":{"row":2,"column":6},"action":"insert","lines":["a"]}],[{"start":{"row":2,"column":6},"end":{"row":2,"column":7},"action":"insert","lines":["w"],"id":10}],[{"start":{"row":2,"column":7},"end":{"row":2,"column":8},"action":"insert","lines":["s"],"id":11}],[{"start":{"row":2,"column":8},"end":{"row":2,"column":9},"action":"insert","lines":["c"],"id":12}],[{"start":{"row":2,"column":9},"end":{"row":2,"column":10},"action":"insert","lines":["o"],"id":13}],[{"start":{"row":2,"column":10},"end":{"row":2,"column":11},"action":"insert","lines":["r"],"id":14}],[{"start":{"row":2,"column":11},"end":{"row":2,"column":12},"action":"insert","lines":["e"],"id":15}],[{"start":{"row":1,"column":5},"end":{"row":1,"column":6},"action":"remove","lines":["H"],"id":16}],[{"start":{"row":1,"column":5},"end":{"row":1,"column":6},"action":"insert","lines":["h"],"id":17}],[{"start":{"row":1,"column":13},"end":{"row":1,"column":14},"action":"remove","lines":["I"],"id":18}],[{"start":{"row":1,"column":13},"end":{"row":1,"column":14},"action":"insert","lines":["i"],"id":19}],[{"start":{"row":1,"column":18},"end":{"row":1,"column":19},"action":"remove","lines":["H"],"id":20}],[{"start":{"row":1,"column":18},"end":{"row":1,"column":19},"action":"insert","lines":["h"],"id":21}],[{"start":{"row":1,"column":18},"end":{"row":1,"column":19},"action":"remove","lines":["h"],"id":22}],[{"start":{"row":1,"column":18},"end":{"row":1,"column":19},"action":"insert","lines":["H"],"id":23}],[{"start":{"row":23,"column":15},"end":{"row":39,"column":44},"action":"remove","lines":["That ^ is a bad thing 99% of the time...\\n\"","","        tables = buildDynamoTableList(getDynamodbConnection())","","        selectedTable = None","        while selectedTable == None:","            searchText = getInput(\"Enter part of the table or environment name you are looking for: \", str, \"\")","            possibleMatches = []","            for name in tables:","                if searchText in name:","                    possibleMatches.append(name)","            if len(possibleMatches) == 0:","                print \"No tables match that search...\"","                continue","            selectedTable = makeListChoice(possibleMatches, \"Select a table <-1 for new search>: \")","","        env = selectedTable.split(\"_\", 1)[0]"],"id":24}],[{"start":{"row":23,"column":15},"end":{"row":23,"column":16},"action":"insert","lines":["C"],"id":25}],[{"start":{"row":23,"column":16},"end":{"row":23,"column":17},"action":"insert","lines":["a"],"id":26}],[{"start":{"row":23,"column":17},"end":{"row":23,"column":18},"action":"insert","lines":["n"],"id":27}],[{"start":{"row":23,"column":18},"end":{"row":23,"column":19},"action":"insert","lines":["n"],"id":28}],[{"start":{"row":23,"column":19},"end":{"row":23,"column":20},"action":"insert","lines":["o"],"id":29}],[{"start":{"row":23,"column":20},"end":{"row":23,"column":21},"action":"insert","lines":["t"],"id":30}],[{"start":{"row":23,"column":21},"end":{"row":23,"column":22},"action":"insert","lines":[" "],"id":31}],[{"start":{"row":23,"column":22},"end":{"row":23,"column":23},"action":"insert","lines":["c"],"id":32}],[{"start":{"row":23,"column":23},"end":{"row":23,"column":24},"action":"insert","lines":["o"],"id":33}],[{"start":{"row":23,"column":24},"end":{"row":23,"column":25},"action":"insert","lines":["n"],"id":34}],[{"start":{"row":23,"column":25},"end":{"row":23,"column":26},"action":"insert","lines":["t"],"id":35}],[{"start":{"row":23,"column":25},"end":{"row":23,"column":26},"action":"remove","lines":["t"],"id":36}],[{"start":{"row":23,"column":25},"end":{"row":23,"column":26},"action":"insert","lines":["t"],"id":37}],[{"start":{"row":23,"column":26},"end":{"row":23,"column":27},"action":"insert","lines":["i"],"id":38}],[{"start":{"row":23,"column":27},"end":{"row":23,"column":28},"action":"insert","lines":["n"],"id":39}],[{"start":{"row":23,"column":28},"end":{"row":23,"column":29},"action":"insert","lines":["u"],"id":40}],[{"start":{"row":23,"column":29},"end":{"row":23,"column":30},"action":"insert","lines":["e"],"id":41}],[{"start":{"row":23,"column":30},"end":{"row":23,"column":31},"action":"insert","lines":["."],"id":42}],[{"start":{"row":23,"column":31},"end":{"row":23,"column":32},"action":"insert","lines":["."],"id":43}],[{"start":{"row":23,"column":32},"end":{"row":23,"column":33},"action":"insert","lines":["."],"id":44}],[{"start":{"row":23,"column":33},"end":{"row":23,"column":34},"action":"insert","lines":["."],"id":45}],[{"start":{"row":23,"column":34},"end":{"row":23,"column":35},"action":"insert","lines":["\""],"id":46}],[{"start":{"row":23,"column":35},"end":{"row":24,"column":0},"action":"insert","lines":["",""],"id":47},{"start":{"row":24,"column":0},"end":{"row":24,"column":8},"action":"insert","lines":["        "]}],[{"start":{"row":24,"column":8},"end":{"row":24,"column":9},"action":"insert","lines":["e"],"id":48}],[{"start":{"row":24,"column":9},"end":{"row":24,"column":10},"action":"insert","lines":["x"],"id":49}],[{"start":{"row":24,"column":10},"end":{"row":24,"column":11},"action":"insert","lines":["i"],"id":50}],[{"start":{"row":24,"column":11},"end":{"row":24,"column":12},"action":"insert","lines":["t"],"id":51}],[{"start":{"row":24,"column":12},"end":{"row":24,"column":13},"action":"insert","lines":["("],"id":52}],[{"start":{"row":24,"column":13},"end":{"row":24,"column":14},"action":"insert","lines":["-"],"id":53}],[{"start":{"row":24,"column":14},"end":{"row":24,"column":15},"action":"insert","lines":["1"],"id":54}],[{"start":{"row":24,"column":15},"end":{"row":24,"column":16},"action":"insert","lines":[")"],"id":55}],[{"start":{"row":1,"column":0},"end":{"row":1,"column":34},"action":"remove","lines":["from helpers.inputHelpers import *"],"id":56}],[{"start":{"row":0,"column":9},"end":{"row":1,"column":0},"action":"remove","lines":["",""],"id":57}],[{"start":{"row":19,"column":33},"end":{"row":19,"column":34},"action":"remove","lines":["t"],"id":58}],[{"start":{"row":19,"column":32},"end":{"row":19,"column":33},"action":"remove","lines":["r"],"id":59}],[{"start":{"row":19,"column":31},"end":{"row":19,"column":32},"action":"remove","lines":["a"],"id":60}],[{"start":{"row":19,"column":30},"end":{"row":19,"column":31},"action":"remove","lines":["p"],"id":61}],[{"start":{"row":19,"column":29},"end":{"row":19,"column":30},"action":"remove","lines":["_"],"id":62}],[{"start":{"row":19,"column":28},"end":{"row":19,"column":29},"action":"remove","lines":["v"],"id":63}],[{"start":{"row":19,"column":27},"end":{"row":19,"column":28},"action":"remove","lines":["n"],"id":64}],[{"start":{"row":19,"column":26},"end":{"row":19,"column":27},"action":"remove","lines":["e"],"id":65}],[{"start":{"row":19,"column":26},"end":{"row":19,"column":34},"action":"insert","lines":["ENV_PART"],"id":66}],[{"start":{"row":16,"column":33},"end":{"row":16,"column":34},"action":"remove","lines":["e"],"id":67}],[{"start":{"row":16,"column":32},"end":{"row":16,"column":33},"action":"remove","lines":["m"],"id":68}],[{"start":{"row":16,"column":31},"end":{"row":16,"column":32},"action":"remove","lines":["a"],"id":69}],[{"start":{"row":16,"column":30},"end":{"row":16,"column":31},"action":"remove","lines":["n"],"id":70}],[{"start":{"row":16,"column":29},"end":{"row":16,"column":30},"action":"remove","lines":["."],"id":71}],[{"start":{"row":16,"column":28},"end":{"row":16,"column":29},"action":"remove","lines":["v"],"id":72}],[{"start":{"row":16,"column":27},"end":{"row":16,"column":28},"action":"remove","lines":["n"],"id":73}],[{"start":{"row":16,"column":26},"end":{"row":16,"column":27},"action":"remove","lines":["e"],"id":74}],[{"start":{"row":16,"column":26},"end":{"row":16,"column":27},"action":"insert","lines":["E"],"id":75}],[{"start":{"row":16,"column":27},"end":{"row":16,"column":28},"action":"insert","lines":["N"],"id":76}],[{"start":{"row":16,"column":28},"end":{"row":16,"column":29},"action":"insert","lines":["V"],"id":77}],[{"start":{"row":16,"column":29},"end":{"row":16,"column":30},"action":"insert","lines":["."],"id":78}],[{"start":{"row":16,"column":30},"end":{"row":16,"column":31},"action":"insert","lines":["N"],"id":79}],[{"start":{"row":16,"column":31},"end":{"row":16,"column":32},"action":"insert","lines":["A"],"id":80}],[{"start":{"row":16,"column":32},"end":{"row":16,"column":33},"action":"insert","lines":["M"],"id":81}],[{"start":{"row":16,"column":33},"end":{"row":16,"column":34},"action":"insert","lines":["E"],"id":82}]]},"ace":{"folds":[],"scrolltop":180,"scrollleft":0,"selection":{"start":{"row":28,"column":28},"end":{"row":28,"column":28},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":11,"state":"qqstring3","mode":"ace/mode/python"}},"timestamp":1447784161420,"hash":"86c5be5026408c2c21f2c2fb3dfc6e211f247335"}