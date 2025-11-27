import os
import json
import re

def parse_frontmatter(content):
    parts = content.split('---')
    if len(parts) < 3:
        return {}, ""
    fm_str = parts[1]
    body = "---".join(parts[2:])
    fm = {}
    for line in fm_str.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            # Handle simple list [a, b]
            if val.startswith('[') and val.endswith(']'):
                val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(',')]
            # Handle unquoted strings
            elif not val.startswith('"') and not val.startswith("'"):
                val = val
            else:
                val = val.strip('"').strip("'")
            fm[key] = val
    return fm, body

adrs = []
root = "docs/architecture/design"
if os.path.exists(root):
    for filename in os.listdir(root):
        if filename.endswith(".md"):
            path = os.path.join(root, filename)
            with open(path, 'r') as f:
                content = f.read()
            fm, body = parse_frontmatter(content)
            adrs.append({
                "path": path,
                "frontmatter": fm,
                "body": body
            })

print(json.dumps({"files": adrs}, indent=2))
