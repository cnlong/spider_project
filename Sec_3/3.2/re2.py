import re

content = "Hello 1234567 World_This is a Regex Demo"
result = re.match('^He.*(\d+).*Demo$', content)
print(result)
print(result.group(1))

result2 = re.match('^He.*?(\d+).*Demo$', content)
print(result2)
print(result2.group(1))