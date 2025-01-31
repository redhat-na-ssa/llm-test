import requests, json, csv

lines = []
template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>||system||<|eot_id|><|start_header_id|>user<|end_header_id|>||user||<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
log_prompt = False
std_prompt = "Do not search internet for your answers. Generate only using the known vocabulary. Generate the response as fast as you can. Do not generate more than 3000 new tokens even if its asked. Adhere to the given rules and conditions."

with open('sample_question.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sys_prompt = row['system'] + ' ' + std_prompt
        line = template.replace("||system||", sys_prompt).replace("||user||", row['user'])
        lines.append(line)

def post(url):
    prompt = lines[0]
    print(prompt)
    payload = {
        "text_input": line,
        "parameters" : {
            "max_tokens":500, "stream": False, "temperature": 0
        }
    }        
    response = requests.post(url, data=json.dumps(payload))

    if response.status_code == 200:
        print("POST request successful")
        print(response.text)
    else:
        print(f"POST request failed with status code: {response.status_code}")
    
if __name__ == "__main__":
    url = ""  # Replace with your API endpoint
    post(url)

