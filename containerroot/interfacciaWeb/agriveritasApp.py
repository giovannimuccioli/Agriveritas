# # Llama3 w/ vLLM
# # Python

from vllm import LLM, SamplingParams

from huggingface_hub import notebook_login

import transformers
import sys


from flask import Flask, request, render_template
from flask.json import jsonify

from huggingface_hub import login
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

from pymilvus import connections, Collection, utility, FieldSchema, DataType, CollectionSchema

connections.connect("default", host="milvus-standalone", port="19530")   #host="milvus-standalone"




app = Flask(__name__)

# Set the Flask environment to development
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

# "/" è la home page
@app.route("/")
def home():
    return render_template("agriveritas.html")

import datetime


llm = None
bge_m3_ef = None

@app.route("/initInfo")
def get_init_info():
    current_date = datetime.date.today()
    print(type(current_date))
    last_update_date = current_date.strftime("%Y/%m/%d")

    return jsonify({"last_update_date": last_update_date})


@app.route("/IAresponse/<regione>")
def IAResponse(regione="noRegionSelected"):
    response_status = 0
    query = "Make a nice greetings message"
    response_text = manageSmartResponse(query)
    
    if(regione == "noRegionSelected"):
        response_status = 1
        response_text = "Seleziona prima una regione, altrimenti non riesco ad aiutarti al meglio!"
    
    response_data = {"status" : response_status, "message" : response_text}

    current_date = datetime.date.today()
    print(type(current_date))

    return jsonify(response_data)




def manageSmartResponse(query):
    print(query)
    return "CIAO"
    # sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
    
    # prompts = [
    #     query
    # ]
    # prompt_template="[INST] {prompt} [/INST]"
    # prompts = [prompt_template.format(prompt=prompt) for prompt in prompts]
    # outputs = llm.generate(prompts, sampling_params)
    # # Print the outputs.
    # for output in outputs:
    #     prompt = output.prompt
    #     generated_text = output.outputs[0].text
    #     print(f"Prompt: {prompt!r}, Generated text: {generated_text}")
    
    # return outputs[0].outputs[0].text


# # CACHE_DIR = 'cache'

# # transformers.logging.set_verbosity(transformers.logging.INFO)

# # HF_TOKEN = "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"
# # login(token=HF_TOKEN)

# # import os
# # import requests

# # def download_and_cache_bge_m3(cache_dir):
# #     model_name = 'BAAI/bge-m3'
# #     model_path = os.path.join(cache_dir, 'bge-m3')

# #     if not os.path.exists(model_path):
# #         # Create the cache directory if it doesn't exist
# #         os.makedirs(cache_dir, exist_ok=True)

# #         # Download the model
# #         url = f'https://huggingface.co/{model_name}/resolve/main/model.bin'
# #         response = requests.get(url, stream=True)

# #         # Save the model to the cache directory
# #         with open(model_path, 'wb') as f:
# #             for chunk in response.iter_content(chunk_size=8192):
# #                 f.write(chunk)

# #     return model_path

# Usage
# bge_m3_path = download_and_cache_bge_m3(CACHE_DIR)
import os
# Create the model download directory
model_dir = "./models"
os.makedirs(model_dir, exist_ok=True)

# Set the TRANSFORMERS_CACHE environment variable
os.environ["TRANSFORMERS_CACHE"] = model_dir

bge_m3_ef = BGEM3EmbeddingFunction(
    model_name='BAAI/bge-m3',
    device='cuda',
    use_fp16=True
)

# from langchain_community.llms import VLLM
# from transformers import AutoTokenizer
# import os

# HF_TOKEN = "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"
# model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
# login(token=HF_TOKEN)
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# terminators = [
#     tokenizer.eos_token_id,
#     tokenizer.convert_tokens_to_ids("<|eot_id|>")
# ]

# # Decrease gpu_memory_utilization
# gpu_memory_utilization = 0.7  # Try a lower value, e.g., 0.6

# # Enforce eager mode
# os.environ["TF_ENABLE_EAGER_EXECUTION"] = "1"

# # Reduce max_num_seqs
# max_num_seqs = 16  # Try a lower value, e.g., 8

# llm = VLLM(
#     model=model_id,
#     trust_remote_code=True,  # mandatory for hf models
#     max_new_tokens=512,
#     temperature=0.9,
#     gpu_memory_utilization=gpu_memory_utilization,
#     top_p=1.0,
#     top_k=10,
#     download_dir="./models",
#     use_beam_search=False,
#     dtype="auto",
#     stop=terminators,
#     vllm_kwargs={"enforce_eager": True}, #, "quantization": "awq", "max_model_len": 4096
# )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)