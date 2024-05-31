import re

input_string = "tasdiklash kodi: 123456"

digits = re.findall(r'\d+', input_string)

output_string = ''.join(digits)

print(output_string)
