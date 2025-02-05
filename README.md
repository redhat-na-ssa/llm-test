### Dataset

Download `3_5M-GPT3_5-Augmented.parquet` from (link)[https://huggingface.co/datasets/Open-Orca/OpenOrca]
pipenv install duckdb
python3 convert_openorca

### Triton

# create and configure GPU machineset
git clone https://github.com/redhat-na-ssa/hobbyist-guide-to-rhoai.git
# edit scripts/library/ocp.sh to deploy g6.12xlarge
./hobbyist-guide-to-rhoai/scripts/setup.sh -s 3

# create triton deployment
oc new-project triton-test
oc create cm configpb --from-file model_repository/vllm_model/config.pbtxt 
oc create cm modelfile --from-file model_repository/vllm_model/1/model.json 
oc create -f triton/deployment.yaml  # edit the hugging face token
oc expose deploy triton-instruct-llama
oc expose svc triton-instruct-llama 

# test
pipenv install locust
python3 single_question.py  # make sure single prompt response is coherent
locust	# load test
