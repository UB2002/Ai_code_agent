def Prompt(language: str, cwe: str, code: str) -> str:
    return f"""
    
    Now You are the security focused AI agen fix issues in the code and cross check it 
    language : {language}
    CWE : {cwe}

    code that needs to be fixed 
    code : {code}

    1. requirements this is the thing that you need to do return only the json ouput in the 
    following way JSON structure you need to follow

    {{
        "fixed_code" : "<fixed code >",
        "diff": "unified diff ",
        "explanation": "<why and how> "
    }}
    
    2. The diff must follow unified diff format (--- original / +++ 
       fixed)

    3. The explanation should be short and understandable 

    ### Output

    """
