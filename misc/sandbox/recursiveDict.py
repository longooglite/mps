import MPSCore.utilities.recursiveDictionary as rc

d = rc.RecursiveDictionary({'foo': {'bar': 42},"someList":[{"a":1,"b":1}]})
d.rec_update({'foo': {'baz': 36},"someList":[{"a":3}]})
print d
