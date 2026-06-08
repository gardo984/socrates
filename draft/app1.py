
import requests
import json

url = "http://localhost:11434/api/generate"
payload = dict(
    model="llama3.2",
    prompt="tell me a fun fact",
)

rsp = requests.post(url, json=payload, stream=True)

if rsp.status_code == 200:
    print(f"Generated Text:", end="", flush=True)
    for line in rsp.iter_lines():
        if line:
            decoded_line = line.decode("utf8")
            result = json.loads(decoded_line)
            generated_text = result.get("response", "")
            print(generated_text, end="", flush=True)
        else:
            print("Error:", rsp.status_code, rsp.text)
