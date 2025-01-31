from locust import HttpUser, task, run_single_user
import json
import random
import logging
import csv
import warnings

warnings.filterwarnings("ignore")

instr_host = ""
instr_url_gen = "/v2/models/vllm_model/generate"

lines = []
template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>||system||<|eot_id|><|start_header_id|>user<|end_header_id|>||user||<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
log_prompt = False
std_prompt = "Do not search internet for your answers. Generate only using the known vocabulary. Generate the response as fast as you can. Do not generate more than 3000 new tokens even if its asked. Adhere to the given rules and conditions."

with open('orca-1000.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sys_prompt = row['system'] + ' ' + std_prompt
        line = template.replace("||system||", sys_prompt).replace("||user||", row['user'])
        lines.append(line)

class InferUser(HttpUser):
              
    @task
    def instruct_generate(self):
        url = instr_host + instr_url_gen
        prompt = random.choice(lines)
        payload = {
            "text_input": prompt,
            "parameters" : {
                "max_tokens":500, "stream": False, "temperature": 0
            }
        }
        response = self.client.post(url=url, verify=False, data=json.dumps(payload), name="Instruct")
        if log_prompt == True or response.status_code != 200:
            logging.info("Url : " + url)
            if log_prompt == True:
                logging.info("Prompt : " + prompt)
            logging.info("Response Code : " + str(response.status_code))
            logging.info("Response : " + response.text)

if __name__ == "__main__":
    run_single_user(InferUser)

