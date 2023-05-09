import re

testRegex = re.compile(r"\$\{([^}]*)\}")

testString = "Hello ${name}, my name is ${name} and I am ${age} years old."

print(testRegex.findall(testString))
