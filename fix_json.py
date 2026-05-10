import json

# Read the file
with open('template.json', 'r') as f:
    text = f.read()

# Replace all unescaped newlines inside the string
import re

# Find the content between "template": " and ", "template_format" 
pattern = r'("template":\s*")(.*?)("\s*,\s*"template_format")'
match = re.search(pattern, text, re.DOTALL)

if match:
    # Get the raw string content
    raw_content = match.group(2)
    # properly escape backslashes first, then newlines, then quotes
    escaped = raw_content.replace("\\\\n", "\n") # reset our previous broken attempts
    escaped = escaped.replace("\\n", "\n")
    escaped = escaped.replace("\n", "\\n")
    escaped = escaped.replace("\"", "\\\"")
    
    # Put it back together
    new_text = text[:match.start(2)] + escaped + text[match.end(2):]
    
    with open('template.json', 'w') as f:
        f.write(new_text)
    
    print("Trying to parse...")
    try:
        with open('template.json', 'r') as f:
            data = json.load(f)
        print("Success! JSON is valid.")
    except Exception as e:
        print(f"Failed: {e}")
else:
    print("Could not find pattern.")
