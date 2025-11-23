from fastapi import FastAPI
from model.fix import Fixrequest
from ai.call_model import LocalModel
from ai.prompt import Prompt
from utils.extract import extract_json_after_example_block

app = FastAPI()
model = LocalModel()


@app.get("/")
def main():
    return "hello world"


@app.post("/fix")
def local_fix(req: Fixrequest):

    prompt = Prompt(req.language, req.cwe, req.code)

    output, input_tokens, output_tokens = model.run_inference(prompt)
    # print("###" * 10)
    # print(output)
    # print("###" * 10)

    parsed = extract_json_after_example_block(output)

    if parsed is None:
        parsed = {"fixed_code": "", "diff": "", "explanation": ""}

    return {
        "fixed_code": parsed.get("fixed_code", ""),
        "diff": parsed.get("diff", ""),
        "explanation": parsed.get("explanation", ""),
        "model_used": "Qwen2.5 coder",
        "token_usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
    }

