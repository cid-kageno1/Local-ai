# My Local AI Flask API
An offline AI API running SmolLM. No API keys required.

## How to run locally (Termux/PC)
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Send a request:
   ```bash
   curl -X POST http://localhost:7860/chat -H "Content-Type: application/json" -d '{"prompt": "Hello!"}'
