import requests

def generate_response(user_input):
    API_URL="https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer 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"}

    response=requests.post(API_URL, headers=headers,json={
        "inputs":user_input,
    })
    
    if response.status_code==200:
        return response.json()[0]['generated_text']
    else:
        return "I'm listening. Go ahead !!"