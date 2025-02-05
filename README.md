### Dataset

Download `3_5M-GPT3_5-Augmented.parquet` from [link](https://huggingface.co/datasets/Open-Orca/OpenOrca)

```
pipenv install duckdb
python3 convert_openorca
```

### Triton on RHEL

Install nvidia container toolkit [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-yum-or-dnf)
Configure [CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html#generating-a-cdi-specification)

Substitute the hugging face token

```
podman run -e HF_TOKEN='' --security-opt=label=disable --device nvidia.com/gpu=all -it --net=host --rm -p 8001:8001 --shm-size=1G --ulimit memlock=-1 --ulimit stack=67108864 -v ${PWD}:/work -w /work nvcr.io/nvidia/tritonserver:24.12-vllm-python-py3 tritonserver --model-repository ./model_repository
```

Smoke test

```
curl -X POST <url>/v2/models/vllm_model/generate -d '{"text_input": "What is Triton Inference Server?", "parameters": {"stream": false, "temperature": 0}}'
```


### Triton on OCP

#### create and configure GPU machineset
`git clone https://github.com/redhat-na-ssa/hobbyist-guide-to-rhoai.git`
edit scripts/library/ocp.sh to deploy g6.12xlarge
`./hobbyist-guide-to-rhoai/scripts/setup.sh -s 3`

#### create triton deployment
```
oc new-project triton-test
oc create cm configpb --from-file model_repository/vllm_model/config.pbtxt 
oc create cm modelfile --from-file model_repository/vllm_model/1/model.json 
oc create -f triton/deployment.yaml  # edit the hugging face token
oc expose deploy triton-instruct-llama
oc expose svc triton-instruct-llama 
```

### Testing (for both RHEL and OCP)
```
pipenv install locust
python3 single_question.py  # make sure single prompt response is coherent
locust	# load test
```
