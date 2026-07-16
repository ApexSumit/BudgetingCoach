import cohere
from config import COHERE_API_KEY, LLM_MODEL, VISION_MODEL
import base64

co_v1 = cohere.Client(COHERE_API_KEY)
co_v2 = cohere.ClientV2(COHERE_API_KEY)

def generate(prompt, chat_history=None, image_path=None):
    """
    Generate response using text (and optionally an image).
    If image_path is provided, use vision model to extract info first,
    then feed it into the main conversation.
    """
    if image_path:
        # Extract info from bill using vision model
        extracted_text = analyze_image(image_path)
        # Prepend extracted info to prompt
        prompt = f"[Bill Analysis]\nThe user uploaded a bill. Here's what we extracted:\n{extracted_text}\n\nNow answer the user's question based on this and the rest of the conversation.\n\n{prompt}"

    # Main generation
    messages = []
    if chat_history:
        for msg in chat_history:
            role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
    messages.append({"role": "user", "content": prompt})

    # Use V2 chat if we are using a model that requires it (like command-a-plus)
    if "command-a-plus" in LLM_MODEL or "command-r7b" in LLM_MODEL:
        resp = co_v2.chat(model=LLM_MODEL, messages=messages, temperature=0.3)
        return resp.message.content[0].text
    else:
        # Fallback to V1 for older models like command-r-plus-08-2024 (still works)
        resp = co_v1.chat(model=LLM_MODEL, message=prompt, chat_history=messages[:-1] if messages else [], temperature=0.3)
        return resp.text

def analyze_image(image_path):
    """Send image to Cohere Vision model and return extracted text."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    # Cohere V2 chat with vision
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract all text, amounts, dates, vendor names, and any relevant financial information from this bill. Output in a structured format."
                },
                {
                    "type": "image",
                    "image": {"url": f"data:image/jpeg;base64,{image_data}"}
                }
            ]
        }
    ]
    resp = co_v2.chat(model=VISION_MODEL, messages=messages)
    return resp.message.content[0].text