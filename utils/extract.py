import json
import re

def extract_json_after_example_block(text: str):

    txt = text.replace("\r\n", "\n")
    example_match = re.search(
        r"(^|\n)\s*(#{1,6}\s*)?Example\b.*\n", txt, flags=re.IGNORECASE
    )
    search_start = example_match.end() if example_match else 0

    fenced_pattern = re.compile(
        r"```json\s*(\{.*?\})\s*```", flags=re.DOTALL | re.IGNORECASE
    )

    json_block = fenced_pattern.search(txt, pos=search_start)
    if json_block:
        json_str = json_block.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:

            cleaned = json_str

            if "'" in cleaned and '"' not in cleaned:
                cleaned = cleaned.replace("'", '"')

            cleaned = re.sub(r",\s*([\]}])", r"\1", cleaned)

            try:
                return json.loads(cleaned)
            except:
                pass

    any_block = fenced_pattern.search(txt)
    if any_block:
        try:
            return json.loads(any_block.group(1).strip())
        except:
            pass
    objects = re.findall(r"\{(?:[^{}]|\{[^{}]*\})*\}", txt, flags=re.DOTALL)
    for obj in objects:
        try:
            return json.loads(obj)
        except:
            continue
    return None