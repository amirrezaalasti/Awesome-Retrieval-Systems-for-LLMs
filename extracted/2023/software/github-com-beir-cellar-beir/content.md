# 

<!-- image -->

GitHub release

<!-- image -->

Build

<!-- image -->

License

<!-- image -->

Open In Colab

<!-- image -->

Downloads

<!-- image -->

Open Source

<!-- image -->

#### [Paper | Installation | Quick Example | Datasets | Wiki | Hugging Face](https://openreview.net/forum?id=wCu6T5xFjeJ)

### 

<!-- image -->

<!-- image -->

<!-- image -->

### 

<!-- image -->

## :beers: What is it?

**BEIR** is a **heterogeneous benchmark** containing diverse IR tasks. It also provides a **common and easy framework** for evaluation of your NLP-based retrieval models within the benchmark. For **an overview** , checkout our **new wiki** page: [https://github.com/beir-cellar/beir/wiki](https://github.com/beir-cellar/beir/wiki) . For **models and datasets** , checkout out **Hugging Face (HF)** page: [https://huggingface.co/BeIR](https://huggingface.co/BeIR) .

For more information, checkout out our publications:

- [BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://openreview.net/forum?id=wCu6T5xFjeJ) (NeurIPS 2021, Datasets and Benchmarks Track)
- [Resources for Brewing BEIR: Reproducible Reference Models and an Official Leaderboard](https://dl.acm.org/doi/10.1145/3626772.3657862) (SIGIR 2024 Resource Track)

## :beers: Installation

Install via pip:

```
pip install beir
```

If you want to build from source, use:

```
$ git clone https://github.com/beir-cellar/beir.git
$ cd beir
$ pip install -e .
```

Tested with python versions 3.9+

## :beers: Features

- Preprocess your own IR dataset or use one of the already-preprocessed 17 benchmark datasets
- Wide settings included, covers diverse benchmarks useful for both academia and industry
- Evaluates well-known retrieval architectures (lexical, dense, sparse and reranking-based)
- Add and evaluate your own model in a easy framework using different state-of-the-art evaluation metrics

## :beers: Quick Example

For other example codes, please refer to our [**Examples and Tutorials**](https://github.com/beir-cellar/beir/wiki/Examples-and-tutorials) Wiki page.

**Quick Example with Sentence-BERT**

```
from beir import util, LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES

import logging
import pathlib, os

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

#### Download scifact.zip dataset and unzip the dataset
dataset = "scifact"
url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

#### Provide the data_path where scifact has been downloaded and unzipped
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

#### Load the SBERT model and retrieve using cosine-similarity
model = DRES(models.SentenceBERT("Alibaba-NLP/gte-modernbert-base"), batch_size=16)

retriever = EvaluateRetrieval(model, score_function="cos_sim") # or "dot" for dot product
results = retriever.retrieve(corpus, queries)

#### Evaluate your model with NDCG@k, MAP@K, Recall@K and Precision@K  where k = [1,3,5,10,100,1000]
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")

### If you want to save your results and runfile (useful for reranking)
results_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "results")
os.makedirs(results_dir, exist_ok=True)

#### Save the evaluation runfile & results
util.save_runfile(os.path.join(results_dir, f"{dataset}.run.trec"), results)
util.save_results(os.path.join(results_dir, f"{dataset}.json"), ndcg, _map, recall, precision, mrr)
```

**Quick Example with LoRA &amp; vLLM**

First install peft, vllm &amp; accelerate using the following installations:

```
pip install peft
pip install accelerate
pip install vllm
```

```
from beir import util, LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES

import logging
import pathlib, os

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

#### Download scifact.zip dataset and unzip the dataset
dataset = "scifact"
url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

#### Provide the data_path where scifact has been downloaded and unzipped
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

#### You can also merge the LoRA model weights into the original base model for faster inference.
#### Checkout: https://github.com/beir-cellar/beir/blob/main/examples/retrieval/evaluation/dense/evaluate_lora_vllm.py

#### Load the vLLM embed model and retrieve using cosine-similarity
model = DRES(
    models.VLLMEmbed(
        model_path="Qwen/Qwen2.5-7B",
        lora_name_or_path="rlhn/Qwen2.5-7B-rlhn-400K",
        max_length=512,
        lora_r=16,
        pooling="eos",
        append_eos_token=True,
        normalize=True,
        prompts={"query": "query: ", "passage": "passage: "},
        convert_to_numpy=True
    ),
    batch_size=128,
)

retriever = EvaluateRetrieval(model, score_function="cos_sim") # or "dot" for dot product
results = retriever.encode_and_retrieve(corpus, queries, encode_output_path="./qwen_embeddings/")

#### Evaluate your model with NDCG@k, MAP@K, Recall@K and Precision@K  where k = [1,3,5,10,100,1000]
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")

### If you want to save your results and runfile (useful for reranking)
results_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "results")
os.makedirs(results_dir, exist_ok=True)

#### Save the evaluation runfile & results
util.save_runfile(os.path.join(results_dir, f"{dataset}.run.trec"), results)
util.save_results(os.path.join(results_dir, f"{dataset}.json"), ndcg, _map, recall, precision, mrr)
```

**Quick Example with HuggingFace**

if you use `encode\_and\_retrieve()` make sure you install faiss with `pip install faiss-cpu`.

```
from beir import util, LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES

import logging
import pathlib, os

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

#### Download scifact.zip dataset and unzip the dataset
dataset = "scifact"
url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

#### Provide the data_path where scifact has been downloaded and unzipped
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

#### Load the Huggingface model and retrieve using cosine-similarity
query_prompt = "Instruct: Given a question, retrieve relevant documents that best answer the question\nQuery: "

model = DRES(
    models.HuggingFace(
        model_path="intfloat/e5-mistral-7b-instruct",
        max_length=512,
        pooling="eos",
        append_eos_token=True,
        normalize=True,
        prompts={"query": query_prompt, "passage": ""},
        attn_implementation="flash_attention_2",
        torch_dtype="bfloat16"
    ),
    batch_size=128,
)

retriever = EvaluateRetrieval(model, score_function="cos_sim") # or "dot" for dot product
results = retriever.encode_and_retrieve(corpus, queries, encode_output_path="./embeddings/")

#### Evaluate your model with NDCG@k, MAP@K, Recall@K and Precision@K  where k = [1,3,5,10,100,1000]
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")

### If you want to save your results and runfile (useful for reranking)
results_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "results")
os.makedirs(results_dir, exist_ok=True)

#### Save the evaluation runfile & results
util.save_runfile(os.path.join(results_dir, f"{dataset}.run.trec"), results)
util.save_results(os.path.join(results_dir, f"{dataset}.json"), ndcg, _map, recall, precision, mrr)
```

**Quick Example with APIs, e.g. Cohere**

Install Cohere API using `pip install cohere` &amp; if you are using `encode_and_retrieve()` install faiss with `pip install faiss-cpu` .

```
from beir import util, LoggingHandler
from beir.retrieval import apis
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES

import logging
import pathlib, os

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

#### Download scifact.zip dataset and unzip the dataset
dataset = "scifact"
url = f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

#### Provide the data_path where scifact has been downloaded and unzipped
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

cohere_api_key = os.getenv("COHERE_API_KEY")
#### Load the Cohere API Embed model and retrieve using cosine-similarity
model = DRES(
    apis.CohereEmbedAPI(
        api_key=cohere_api_key, 
        model_path="embed-v4.0", 
        normalize=True, 
        torch_dtype="float32"
    ),
    batch_size=96,
)

retriever = EvaluateRetrieval(model, score_function="cos_sim") # or "dot" for dot product
results = retriever.encode_and_retrieve(corpus, queries, encode_output_path="./cohere/embeddings/")

#### Evaluate your model with NDCG@k, MAP@K, Recall@K and Precision@K  where k = [1,3,5,10,100,1000]
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")

### If you want to save your results and runfile (useful for reranking)
results_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "results")
os.makedirs(results_dir, exist_ok=True)

#### Save the evaluation runfile & results
util.save_runfile(os.path.join(results_dir, f"{dataset}.run.trec"), results)
util.save_results(os.path.join(results_dir, f"{dataset}.json"), ndcg, _map, recall, precision, mrr)
```

## :beers: Available Datasets

Command to generate md5hash using Terminal: `md5sum filename.zip` . You can view all datasets available [**here**](https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/) or on [**Hugging Face**](https://huggingface.co/BeIR) . `msmarco train dev test 444067daf65d982533ea17ebd59501e4 trec-covid test ce62140cb23feb9becf6270d0d1fe6d1 nfcorpus train dev test a89dba18a62ef92f7d323ec890a0d38d bioasq train test nq train test d4d3d2e48787a744b6f6e691ff534307 hotpotqa train dev test f412724f78b0d91183a0e86805e16114 fiqa train dev test 17918ed23cd04fb15047f73e6c3bd9d9 signal1m test trec-news test robust04 test arguana test 8ad3e3c2a5867cdced806d6503f29b99 webis-touche2020 test 46f650ba5a527fc69e0a6521c5a23563 cqadupstack test 4e41456d7df8ee7760a7f866133bda78 quora dev test 18fb154900ba42a600f84b839c173167 dbpedia-entity dev test c2a39eb420a3164af735795df012ac2c scidocs test 38121350fc3a4d2f48850f6aff52e4a9 fever train dev test 5a818580227bfb4b35bb6fa46d9b6c03 climate-fever test 8b66f0a9126c521bae2bde127b4dc99d scifact train test 5f7d1de60b170fc8027bb7898e2efca1`

| Dataset   | Website   | BEIR-Name   | Public?   | Type   | Queries   | Corpus   | Rel D/Q   | Down-load   | md5   |
|-----------|-----------|-------------|-----------|--------|-----------|----------|-----------|-------------|-------|
| MSMARCO   | Homepage  |             |           |        |           |          |           |             |       |

| ✅   |
|-----|

| 6,980   | 8.84M   | 1.1   | Link   |
|---------|---------|-------|--------|

| ✅   |
|-----|

| 50   | 171K   | 493.5   | Link   |
|------|--------|---------|--------|

| ✅   |
|-----|

| 323   | 3.6K   | 38.2   | Link   |
|-------|--------|--------|--------|

| ❌   |
|-----|

| 500   | 14.91M   | 4.7   | No   | How to Reproduce?   |
|-------|----------|-------|------|---------------------|

| ✅   |
|-----|

| 3,452   | 2.68M   | 1.2   | Link   |
|---------|---------|-------|--------|

| ✅   |
|-----|

| 7,405   | 5.23M   | 2.0   | Link   |
|---------|---------|-------|--------|

| ✅   |
|-----|

| 648   | 57K   | 2.6   | Link   |
|-------|-------|-------|--------|

| ❌   |
|-----|

| 97   | 2.86M   | 19.6   | No   | How to Reproduce?   |
|------|---------|--------|------|---------------------|

| ❌   |
|-----|

| 57   | 595K   | 19.6   | No   | How to Reproduce?   |
|------|--------|--------|------|---------------------|

| ❌   |
|-----|

| 249   | 528K   | 69.9   | No   | How to Reproduce?   |
|-------|--------|--------|------|---------------------|

| ✅   |
|-----|

| 1,406   | 8.67K   | 1.0   | Link   |
|---------|---------|-------|--------|

| ✅   |
|-----|

| 49   | 382K   | 19.0   | Link   |
|------|--------|--------|--------|

| ✅   |
|-----|

| 13,145   | 457K   | 1.4   | Link   |
|----------|--------|-------|--------|

| ✅   |
|-----|

| 10,000   | 523K   | 1.6   | Link   |
|----------|--------|-------|--------|

| ✅   |
|-----|

| 400   | 4.63M   | 38.2   | Link   |
|-------|---------|--------|--------|

| ✅   |
|-----|

| 1,000   | 25K   | 4.9   | Link   |
|---------|-------|-------|--------|

| ✅   |
|-----|

| 6,666   | 5.42M   | 1.2   | Link   |
|---------|---------|-------|--------|

| ✅   |
|-----|

| 1,535   | 5.42M   | 3.0   | Link   |
|---------|---------|-------|--------|

| ✅   |
|-----|

| 300   | 5K   | 1.1   | Link   |
|-------|------|-------|--------|

## :beers: Additional Information

We also provide a variety of additional information in our [**Wiki**](https://github.com/beir-cellar/beir/wiki) page. Please refer to these pages for the following:

### Quick Start

- [Installing BEIR](https://github.com/beir-cellar/beir/wiki/Installing-beir)
- [Examples and Tutorials](https://github.com/beir-cellar/beir/wiki/Examples-and-tutorials)

### Datasets

- [Datasets Available](https://github.com/beir-cellar/beir/wiki/Datasets-available)
- [Multilingual Datasets](https://github.com/beir-cellar/beir/wiki/Multilingual-datasets)
- [Load your Custom Dataset](https://github.com/beir-cellar/beir/wiki/Load-your-custom-dataset)

### Models

- [Models Available](https://github.com/beir-cellar/beir/wiki/Models-available)
- [Evaluate your Custom Model](https://github.com/beir-cellar/beir/wiki/Evaluate-your-custom-model)

### Metrics

- [Metrics Available](https://github.com/beir-cellar/beir/wiki/Metrics-available)

### Miscellaneous

- [BEIR Leaderboard](https://github.com/beir-cellar/beir/wiki/Leaderboard)
- [Couse Material on IR](https://github.com/beir-cellar/beir/wiki/Course-material-on-ir)

## :beers: Disclaimer

Similar to Tensorflow [datasets](https://github.com/tensorflow/datasets) or Hugging Face's [datasets](https://github.com/huggingface/datasets) library, we just downloaded and prepared public datasets. We only distribute these datasets in a specific format, but we do not vouch for their quality or fairness, or claim that you have license to use the dataset. It remains the user's responsibility to determine whether you as a user have permission to use the dataset under the dataset's license and to cite the right owner of the dataset.

If you're a dataset owner and wish to update any part of it, or do not want your dataset to be included in this library, feel free to post an issue here or make a pull request!

If you're a dataset owner and wish to include your dataset or model in this library, feel free to post an issue here or make a pull request!

## :beers: Citing &amp; Authors

If you find this repository helpful, feel free to cite our publication [BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663) :

```
@inproceedings{
    thakur2021beir,
    title={{BEIR}: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models},
    author={Nandan Thakur and Nils Reimers and Andreas R{\"u}ckl{\'e} and Abhishek Srivastava and Iryna Gurevych},
    booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)},
    year={2021},
    url={https://openreview.net/forum?id=wCu6T5xFjeJ}
}
```

If you use any baseline score from the BEIR leaderboard, feel free to cite our publication [Resources for Brewing BEIR: Reproducible Reference Models and an Official Leaderboard](https://arxiv.org/abs/2306.07471)

```
@inproceedings{kamalloo:2024,
    author = {Kamalloo, Ehsan and Thakur, Nandan and Lassance, Carlos and Ma, Xueguang and Yang, Jheng-Hong and Lin, Jimmy},
    title = {Resources for Brewing BEIR: Reproducible Reference Models and Statistical Analyses},
    year = {2024},
    isbn = {9798400704314},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3626772.3657862},
    doi = {10.1145/3626772.3657862},
    abstract = {BEIR is a benchmark dataset originally designed for zero-shot evaluation of retrieval models across 18 different domain/task combinations. In recent years, we have witnessed the growing popularity of models based on representation learning, which naturally begs the question: How effective are these models when presented with queries and documents that differ from the training data? While BEIR was designed to answer this question, our work addresses two shortcomings that prevent the benchmark from achieving its full potential: First, the sophistication of modern neural methods and the complexity of current software infrastructure create barriers to entry for newcomers. To this end, we provide reproducible reference implementations that cover learned dense and sparse models. Second, comparisons on BEIR are performed by reducing scores from heterogeneous datasets into a single average that is difficult to interpret. To remedy this, we present meta-analyses focusing on effect sizes across datasets that are able to accurately quantify model differences. By addressing both shortcomings, our work facilitates future explorations in a range of interesting research questions.},
    booktitle = {Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval},
    pages = {1431-1440},
    numpages = {10},
    keywords = {domain generalization, evaluation, reproducibility},
    location = {Washington DC, USA},
    series = {SIGIR '24}
}
```

The main contributors of this repository are:

- [Nandan Thakur](https://github.com/Nthakur20) , Personal Website: [thakur-nandan.gitub.io](https://thakur-nandan.github.io/)

Contact person: Nandan Thakur, [nandant@gmail.com](mailto:nandant@gmail.com)

Don't hesitate to send us an e-mail or report an issue, if something is broken (and it shouldn't be) or if you have further questions.

This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.

## :beers: Collaboration

The BEIR Benchmark has been made possible due to a collaborative effort of the following universities and organizations:

- [UKP Lab, Technical University of Darmstadt](http://www.ukp.tu-darmstadt.de/)
- [University of Waterloo](https://uwaterloo.ca/)
- [Hugging Face](https://huggingface.co/)

## :beers: Contributors

Thanks go to all these wonderful collaborations for their contribution towards the BEIR benchmark:

| <!-- image -->  [**Nandan Thakur**](https://www.nandan-thakur.com/)   | <!-- image -->  [**Nils Reimers**](https://www.nils-reimers.de/)   | <!-- image -->  [**Iryna Gurevych**](https://www.informatik.tu-darmstadt.de/ukp/ukp_home/head_ukp/index.en.jsp)   | <!-- image -->  [**Jimmy Lin**](https://cs.uwaterloo.ca/~jimmylin/)   | <!-- image -->  [**Andreas Rücklé**](http://rueckle.net/)   | <!-- image -->  [**Abhishek Srivastava**](https://www.linkedin.com/in/abhesrivas)   |
|-----------------------------------------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------------|