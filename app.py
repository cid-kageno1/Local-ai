from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

app = Flask(__name__)

# 1. Model Selection (135M is instant, 1.7B is much smarter but slower)
model_id = "HuggingFaceTB/SmolLM-135M-Instruct"

print("Loading model to RAM... please wait.")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Create the AI pipeline
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route('/')
def home():
    return "AI Flask API is Online. Use /chat (POST) or /test (GET)."

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is responding!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")

        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Format prompt for the Instruct model
        chat_style_prompt = f"<|user|>\n{user_prompt}<|assistant|>\n"
        
        # Generate response
        output = pipe(chat_style_prompt, max_new_tokens=150, temperature=0.7, do_sample=True)
        response_text = output[0]['generated_text'].split("<|assistant|>\n")[-1]

        return jsonify({
            "status": "success",
            "model": model_id,
            "response": response_text.strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use port 7860 for Hugging Face or 5000 for local phone testing
    app.run(host='0.0.0.0', port=7860)
