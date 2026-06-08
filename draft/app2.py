

import ollama
from pprint import pprint

# to list
# rsp = ollama.list()

# to chat
# rsp = ollama.chat(
#     model="llama3.2",
#     messages=[
#         {"role": "user", "content": "why is the sky blue?"}
#     ],
#     stream=True,
# )
# for chunk in rsp:
#     print(chunk, end="", flush=True)

# pprint(rsp)

# to create a model
# modelfile = """
# PARAMETER temperature 0.3
# SYSTEM you are peter, and intelligent assistant known for providing clear, concise and informative answers to questions.
# """
# ollama.create(model="smartassistant", system=modelfile, from_="llama3.2")

# res = ollama.generate(model="smartassistant", prompt="what is your name")
# print(res["response"])

