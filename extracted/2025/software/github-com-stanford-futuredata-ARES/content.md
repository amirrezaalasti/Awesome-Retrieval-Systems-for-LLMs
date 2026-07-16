## ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems

Table of Contents: [Installation](#section1) | [Requirements](#section2) | [Quick Start](#section3) | [Citation](#section4)

Static Badge

<!-- image -->

Static Badge

<!-- image -->

Static Badge

<!-- image -->

Open In Colab

<!-- image -->

Static Badge

<!-- image -->

ARES is a groundbreaking framework for evaluating Retrieval-Augmented Generation (RAG) models. The automated process combines synthetic data generation with fine-tuned classifiers to efficiently assess context relevance, answer faithfulness, and answer relevance, minimizing the need for extensive human annotations. ARES employs synthetic query generation and Prediction-Powered Inference (PPI), providing accurate evaluations with statistical confidence.

### 💬 Mini Q&amp;A

**What does ARES assess in RAG models?**

ARES conducts a comprehensive evaluation of Retrieval-Augmented Generation (RAG) models, assessing the systems for context relevance, answer faithfulness, and answer relevance. This thorough assessment ensures a complete understanding of the performance of the RAG system.

**How does ARES automate the evaluation process?**

ARES minimizes the need for human labeling by leveraging fine-tuned classifiers and synthetic data. Its PPI component, Prediction-Powered inference, refines evaluations considering model response variability and provides statistical confidence in the results. By using fine-tuned classifiers and synthetically generated data, ARES cuts down on human labeling needs while providing accurate assessments.

**Can ARES handle my custom RAG model?**

Yes, ARES is a model-agnostic tool that enables you to generate synthetic queries and answers from your documents. With ARES, you can evaluate these generated queries and answers from your RAG model. 

### ⚙️ Installation

 To install ARES, run the following commands: 

```
pip install ares-ai
```

*Optional: Initalize OpenAI or TogetherAI API key with the following command:*

```
export OPENAI_API_KEY= export TOGETHER_API_KEY=
```

### 📝 Requirements

To implement ARES for scoring your RAG system and comparing to other RAG configurations, you need three components:

- A human preference validation set of annotated query, document, and answer triples for the evaluation criteria (e.g. context relevance, answer faithfulness, and/or answer relevance). There should be at least 50 examples but several hundred examples is ideal.
- A set of few-shot examples for scoring context relevance, answer faithfulness, and/or answer relevance in your system
- A much larger set of unlabeled query-document-answer triples outputted by your RAG system for scoring

To get started with ARES, you'll need to set up your configuration. Below is an example of a configuration for ARES!

Copy-paste each step to see ARES in action!

### 📥 Download datasets

Use the following command to quickly obtain the necessary files for getting started! This includes the 'few\_shot\_prompt' file for judge scoring and synthetic query generation, as well as both labeled and unlabeled datasets.

```
wget https://raw.githubusercontent.com/stanford-futuredata/ARES/main/datasets/example_files/nq_few_shot_prompt_for_judge_scoring.tsv
wget https://raw.githubusercontent.com/stanford-futuredata/ARES/main/datasets/example_files/nq_few_shot_prompt_for_synthetic_query_generation.tsv
wget https://raw.githubusercontent.com/stanford-futuredata/ARES/main/datasets/example_files/nq_labeled_output.tsv
wget https://raw.githubusercontent.com/stanford-futuredata/ARES/main/datasets/example_files/nq_unlabeled_output.tsv
```

OPTIONAL: You can run the following command to get the full NQ dataset! (37.3 GB)

```
from ares import ARES
ares = ARES() 
ares.KILT_dataset("nq")

# Fetches NQ datasets with ratios including 0.5, 0.6, 0.7, etc.
# For purposes of our quick start guide, we rename nq_ratio_0.5 to nq_unlabeled_output and nq_labeled_output.
```

### 🚀 Quick Start - #1

To get started with ARES's PPI, you'll need to set up your configuration. Below is an example of a configuration for ARES!

Just copy-paste as you go to see ARES in action!

#### Step 1) Run the following to retrieve the UES/IDP scores with GPT3.5!

```
from ares import ARES

ues_idp_config = {
    "in_domain_prompts_dataset": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "unlabeled_evaluation_set": "nq_unlabeled_output.tsv", 
    "model_choice" : "gpt-3.5-turbo-0125"
} 

ares = ARES(ues_idp=ues_idp_config)
results = ares.ues_idp()
print(results)
# {'Context Relevance Scores': [Score], 'Answer Faithfulness Scores': [Score], 'Answer Relevance Scores': [Score]}
```

#### Step 2) Run the following to retrive ARES's PPI scores with GPT3.5!

```
ppi_config = { 
    "evaluation_datasets": ['nq_unlabeled_output.tsv'], 
    "few_shot_examples_filepath": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "llm_judge": "gpt-3.5-turbo-1106",
    "labels": ["Context_Relevance_Label"], 
    "gold_label_path": "nq_labeled_output.tsv", 
}

ares = ARES(ppi=ppi_config)
results = ares.evaluate_RAG()
print(results)
```

### 🚀 Quick Start - #2

#### Step 1) Run the following to see GPT 3.5's accuracy on the NQ unlabeled dataset!

```
from ares import ARES

ues_idp_config = {
    "in_domain_prompts_dataset": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "unlabeled_evaluation_set": "nq_unlabeled_output.tsv", 
    "model_choice" : "gpt-3.5-turbo-0125"
} 

ares = ARES(ues_idp=ues_idp_config)
results = ares.ues_idp()
print(results)
# {'Context Relevance Scores': [Score], 'Answer Faithfulness Scores': [Score], 'Answer Relevance Scores': [Score]}
```

#### Step 2) Run the following to see ARES's synthetic generation in action!

```
from ares import ARES

synth_config = { 
    "document_filepaths": ["nq_labeled_output.tsv"] ,
    "few_shot_prompt_filename": "nq_few_shot_prompt_for_synthetic_query_generation.tsv",
    "synthetic_queries_filenames": ["synthetic_queries_1.tsv"], 
    "documents_sampled": 6189
}

ares_module = ARES(synthetic_query_generator=synth_config)
results = ares_module.generate_synthetic_data()
print(results)
```

#### Step 3) Run the following to see ARES's training classifier in action!

```
from ares import ARES

classifier_config = {
    "training_dataset": ["synthetic_queries_1.tsv"], 
    "validation_set": ["nq_labeled_output.tsv"], 
    "label_column": ["Context_Relevance_Label"], 
    "num_epochs": 10, 
    "patience_value": 3, 
    "learning_rate": 5e-6,
    "assigned_batch_size": 1,  
    "gradient_accumulation_multiplier": 32,  
}

ares = ARES(classifier_model=classifier_config)
results = ares.train_classifier()
print(results)
```

Note: This code creates a checkpoint for the trained classifier. Training may take some time. You can download our jointly trained checkpoint on context relevance here!: [Download Checkpoint](https://drive.google.com/file/d/1INyHfZpsUsn5UEBLSRehI9AX08AI12Lt/view?usp=sharing)

#### Step 4) Run the following to see ARES's PPI in action!

```
from ares import ARES

ppi_config = { 
    "evaluation_datasets": ['nq_unlabeled_output.tsv'], 
    "checkpoints": ["Context_Relevance_Label_nq_labeled_output_date_time.pt"], 
    "rag_type": "question_answering", 
    "labels": ["Context_Relevance_Label"], 
    "gold_label_path": "nq_labeled_output.tsv", 
}

ares = ARES(ppi=ppi_config)
results = ares.evaluate_RAG()
print(results)

# Output Should be: 
""" 
Context_Relevance_Label Scoring
ARES Ranking
ARES Prediction: [0.6056978059262574]
ARES Confidence Interval: [[0.547, 0.664]]
Number of Examples in Evaluation Set: [4421]
Ground Truth Performance: [0.6]
ARES LLM Judge Accuracy on Ground Truth Labels: [0.789]
Annotated Examples used for PPI: 300
"""
```

### 🚀 Local Model Execution with vLLM

ARES supports [vLLM](https://github.com/vllm-project/vllm) , allowing for local execution of LLM models, offering enhanced privacy and the ability to operate ARES offline. Below are steps to vLLM for ARES's UES/IDP and PPI!

#### 1) UES/IDP w/ vLLM

```
from ares import ARES

ues_idp_config = {
    "in_domain_prompts_dataset": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "unlabeled_evaluation_set": "nq_unlabeled_output.tsv", 
    "model_choice": "meta-llama/Llama-2-13b-hf", # Specify vLLM model
    "vllm": True, # Toggle vLLM to True 
    "host_url": "http://0.0.0.0:8000/v1" # Replace with server hosting model followed by "/v1"
} 

ares = ARES(ues_idp=ues_idp_config)
results = ares.ues_idp()
print(results)
```

#### 2) PPI w/ vLLM

```
from ares import ARES

ppi_config = { 
    "evaluation_datasets": ['nq_unabeled_output.tsv'], 
    "few_shot_examples_filepath": "nq_few_shot_prompt_for_judge_scoring.tsv",
    "llm_judge": "meta-llama/Llama-2-13b-hf", # Specify vLLM model
    "labels": ["Context_Relevance_Label"], 
    "gold_label_path": "nq_labeled_output.tsv",
    "vllm": True, # Toggle vLLM to True 
    "host_url": "http://0.0.0.0:8000/v1" # Replace with server hosting model followed by "/v1"
}

ares = ARES(ppi=ppi_config)
results = ares.evaluate_RAG()
print(results)
```

For more details, refer to our [documentation](https://ares-ai.vercel.app/) .

## Results Replication

We include synthetic datasets for key experimental results in `synthetic_datasets` . The few-shot prompts used for generation and evaluation are included in `datasets` . We also include instructions for fine-tuning LLM judges in the paper itself. Please reach out to jonsaadfalcon@stanford.edu or manihani@stanford.edu if you have any further questions.

## Citation

To cite our work, please use the following Bibtex:

```
@misc{saadfalcon2023ares,
      title={ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems}, 
      author={Jon Saad-Falcon and Omar Khattab and Christopher Potts and Matei Zaharia},
      year={2023},
      eprint={2311.09476},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

# Appendix

### Machine requirements and setup when not using OpenAI API

**Machine requirements**

- Over ~100 GB of available disk space
- GPU
    - Should work: A100 (e.g. `Standard_NC24ads_A100_v4` on Azure)
    - Does not work:
        - Tested on 2023-12-17 with both `Standard_NC6s_v3` and `Standard_NC12s_v3` , and ran into this error: `torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 160.00 MiB (GPU 0; 15.77 GiB total capacity; 15.12 GiB already allocated; 95.44 MiB free; 15.12 GiB reserved in total by PyTorch)`

**Machine setup**

For example, on an Azure VM running Linux (ubuntu 20.04), you will need to do the following:

- Install conda
    - First set of commands (can copy-paste multiple lines)
        - wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86\_64.sh
        - chmod +x Miniconda3-latest-Linux-x86\_64.sh
        - ./Miniconda3-latest-Linux-x86\_64.sh -b
    - Second set of commands (can copy-paste multiple lines)
        - export PATH="~/miniconda3/bin:$PATH"
        - conda init
- Install gcc
    - sudo apt-get -y update
    - sudo apt-get -y upgrade
    - sudo apt-get -y install build-essential
    - sudo apt-get -y install libpcre3-dev
- Install NVIDIA drivers
    - sudo apt install ubuntu-drivers-common -y
    - sudo ubuntu-drivers autoinstall
    - sudo reboot
    - SSH in again and confirm the installation was successful by running `nvidia-smi`
- `cd` to ARES folder and follow the rest of the README