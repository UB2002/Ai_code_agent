from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "Qwen/Qwen2.5-coder-1.5B-Instruct"


class LocalModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, torch_dtype=torch.bfloat16, device_map="cpu"
        )

    def run_inference(self, prompt: str, max_new_tokens: int = 512):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        input_tokens = inputs.input_ids.shape[1]

        output_ids = self.model.generate(
            **inputs, max_new_tokens=max_new_tokens, do_sample=False
        )

        output_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        output_tokens = output_ids.shape[1] - input_tokens

        return output_text, input_tokens, output_tokens


if __name__ == "__main__":
    model = LocalModel()

    q = "what is ai"

    ans, input_text, outtoken = model.run_inference(q)

    print(ans)

    print("--" * 10, "\n\n")
    print(input_text)

    print("--" * 10, "\n\n")
    print(outtoken)
