## Contriever: Unsupervised Dense Information Retrieval with Contrastive Learning

This repository contains pre-trained models, code for pre-training and evaluation for our paper [Unsupervised Dense Information Retrieval with Contrastive Learning](https://arxiv.org/abs/2112.09118) .

We use a simple contrastive learning framework to pre-train models for information retrieval. Contriever, trained without supervision, is competitive with BM25 for R@100 on the BEIR benchmark. After finetuning on MSMARCO, Contriever obtains strong performance, especially for the recall at 100.

We also trained a multilingual version of Contriever, mContriever, achieving strong multilingual and cross-lingual retrieval performance.

## Getting started

Pre-trained models can be loaded through the HuggingFace transformers library:

```
from src.contriever import Contriever
from transformers import AutoTokenizer

contriever = Contriever.from_pretrained("facebook/contriever") 
tokenizer = AutoTokenizer.from_pretrained("facebook/contriever") #Load the associated tokenizer:
```

Then embeddings for different sentences can be obtained by doing the following:

```
sentences = [
    "Where was Marie Curie born?",
    "Maria Sklodowska, later known as Marie Curie, was born on November 7, 1867.",
    "Born in Paris on 15 May 1859, Pierre Curie was the son of Eugène Curie, a doctor of French Catholic origin from Alsace."
]

inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
embeddings = model(**inputs)
```

Then similarity scores between the different sentences are obtained with a dot product between the embeddings:

```
score01 = embeddings[0] @ embeddings[1] #1.0473
score02 = embeddings[0] @ embeddings[2] #1.0095
```

## Pre-trained models

The following pre-trained models are available:

- *contriever* : pre-trained on CC-net and English Wikipedia without any supervised data,
- *contriever-msmarco* : contriever with fine-tuning on MSMARCO,
- *mcontriever* : pre-trained on 29 languages using data from CC-net,
- *mcontriever-msmarco* : mcontriever with fine-tuning on MSMARCO.

```
from src.contriever import Contriever

contriever = Contriever.from_pretrained("facebook/contriever") 
contriever_msmarco = Contriever.from_pretrained("facebook/contriever-msmarco")
mcontriever = Contriever.from_pretrained("facebook/mcontriever")
mcontriever_msmarco = Contriever.from_pretrained("facebook/mcontriever-msmarco")
```

## Evaluation

### Question answering retrieval

NaturalQuestions and TriviaQA data can be downloaded from the FiD repository https://github.com/facebookresearch/fid . The NaturalQuestions data slightly differs from the data provided in the DPR repository: we use the answers provided in the original NaturalQuestions data while DPR apply a post-processing step, which affects the tokenization of words.

Retrieval is performed on the set of Wikipeda passages used in DPR. Download passages:

```
wget https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz
```

Generate passage embeddings:

```
python generate_passage_embeddings.py \
    --model_name_or_path facebook/contriever \
    --output_dir contriever_embeddings  \
    --passages psgs_w100.tsv \
    --shard_id 0 --num_shards 1 \
```

Alternatively, download passage embeddings pre-computed with Contriever or Contriever-msmarco:

```
wget https://dl.fbaipublicfiles.com/contriever/embeddings/contriever/wikipedia_embeddings.tar
wget https://dl.fbaipublicfiles.com/contriever/embeddings/contriever-msmarco/wikipedia_embeddings.tar
```

Retrieve top-100 passages:

```
python passage_retrieval.py \
    --model_name_or_path facebook/contriever \
    --passages psgs_w100.tsv \
    --passages_embeddings "contriever_embeddings/*" \
    --data nq_dir/test.json \
    --output_dir contriever_nq \
```

This leads to the following results:

| Model              | NaturalQuestions   | NaturalQuestions   | NaturalQuestions   | TriviaQA   | TriviaQA   | TriviaQA   |
|--------------------|--------------------|--------------------|--------------------|------------|------------|------------|
|                    | R@5                | R@20               | R@100              | R@5        | R@20       | R@100      |
| Contriever         | 47.8               | 67.8               | 82.1               | 59.4       | 67.8       | 83.2       |
| Contriever-msmarco | 65.7               | 79.6               | 88.0               | 71.3       | 80.4       | 85.7       |

### BEIR

Scores on the BEIR benchmark can be reproduced using [beireval.py](beireval.py) .

```
python beireval.py --model_name_or_path contriever-msmarco --dataset scifact
```

The Touche-2020 dataset has been update in BEIR, thus results will differ if the current version is used.

| nDCG@10            |   Avg |   MSMARCO |   TREC-Covid |   NFCorpus |   NaturalQuestions |   HotpotQA |   FiQA |   ArguAna |   Tóuche-2020 |   Quora |   CQAdupstack |   DBPedia |   Scidocs |   Fever |   Climate-fever |   Scifact |
|--------------------|-------|-----------|--------------|------------|--------------------|------------|--------|-----------|---------------|---------|---------------|-----------|-----------|---------|-----------------|-----------|
| Contriever         |  37.7 |      20.6 |         27.4 |       31.7 |               25.4 |       48.1 |   24.5 |      37.9 |          19.3 |    83.5 |          28.4 |      29.2 |      14.9 |    68.2 |            15.5 |      64.9 |
| Contriever-msmarco |  46.6 |      40.7 |         59.6 |       32.8 |               49.8 |       63.8 |   32.9 |      44.6 |          23.0 |    86.5 |          34.5 |      41.3 |      16.5 |    75.8 |            23.7 |      67.7 |

| R@100              |   Avg |   MSMARCO |   TREC-covid |   NFCorpus |   NaturalQuestions |   HotpotQA |   FiQA |   ArguAna |   Tóuche-2020 |   Quora |   CQAdupstack |   DBPedia |   Scidocs |   Fever |   Climate-fever |   Scifact |
|--------------------|-------|-----------|--------------|------------|--------------------|------------|--------|-----------|---------------|---------|---------------|-----------|-----------|---------|-----------------|-----------|
| Contriever-msmarco |  59.6 |      67.2 |         17.2 |       29.4 |               77.1 |       70.4 |   56.2 |      90.1 |          22.5 |    98.7 |          61.4 |      45.3 |      36.0 |    93.6 |            44.1 |      92.6 |
| Contriever-msmarco |  67.0 |      89.1 |         40.7 |       30.0 |               92.5 |       77.7 |   65.6 |      97.7 |          29.4 |    99.3 |          66.3 |      54.1 |      37.8 |    94.9 |            57.4 |      94.7 |

## Multilingual evaluation

We evaluate mContriever on Mr. Tydi v1.1 and a cross-lingual retrieval setting derived from MKQA. You will find below steps to reproduce our results on these datasets.

### Mr. TyDi v1.1

For multilingual evaluation on Mr. TyDi v1.1, we download datasets from https://github.com/castorini/mr.tydi and convert them to the BEIR format using (data\_scripts/convertmrtydi2beir.py)[data\_scripts/convertmrtydi2beir]. Evaluation on Swahili can be performed by doing the following:

Download data:

```
wget https://git.uwaterloo.ca/jimmylin/mr.tydi/-/raw/master/data/mrtydi-v1.1-swahili.tar.gz -P mrtydi
tar -xf mrtydi/mrtydi-v1.1-swahili.tar.gz -C mrtydi
gzip -d mrtydi/mrtydi-v1.1-swahili/collection/docs.jsonl.gz
```

Convert data:

```
python data_scripts/convertmrtydi2beir.py mrtydi/mrtydi-v1.1-swahili mrtydi/mrtydi-v1.1-swahili
```

Evaluation:

```
python beireval.py --model_name_or_path facebook/mcontriever --dataset mrtydi/mrtydi-v1.1-swahili --normalize_text
```

| MRR@100             |   ar |   bn |   en |   fi |   id |   ja |   ko |   ru |   sw |   te |   th |   avg |
|---------------------|------|------|------|------|------|------|------|------|------|------|------|-------|
| mContriever         | 27.3 | 36.3 |  9.2 | 21.1 | 23.5 | 19.5 | 22.3 | 17.5 | 38.3 | 22.5 | 37.2 |  25.0 |
| mContriever-msmarco | 43.4 | 42.3 | 27.1 | 25.1 | 42.6 | 32.4 | 34.2 | 36.1 | 51.2 | 37.4 | 40.2 |  38.4 |
| + Mr. TyDi          | 72.4 | 67.2 | 56.6 | 60.2 | 63.0 | 54.9 | 55.3 | 59.7 | 70.7 | 90.3 | 67.3 |  65.2 |

| R@100               |   ar |   bn |   en |   fi |   id |   ja |   ko |   ru |   sw |   te |   th |   avg |
|---------------------|------|------|------|------|------|------|------|------|------|------|------|-------|
| mContriever         | 82.0 | 89.6 | 48.8 | 79.6 | 81.4 | 72.8 | 66.2 | 68.5 | 88.7 | 80.8 | 90.3 |  77.2 |
| mContriever-msmarco | 88.7 | 91.4 | 77.2 | 88.1 | 89.8 | 81.7 | 78.2 | 83.8 | 91.4 | 96.6 | 90.5 |  87.0 |
| + Mr. TyDi          | 94.0 | 98.6 | 92.2 | 92.7 | 94.5 | 88.8 | 88.9 | 92.4 | 93.7 | 98.9 | 95.2 |  93.6 |

### Cross-lingual MKQA

Here our goal is to measure how well retrievers are to retrieve relevant documents in English Wikipedia given a query in another language. For this we use MKQA and evaluate if the answer is in the retrieved documents based on the DPR evaluation script.

Download data:

```
wget https://raw.githubusercontent.com/apple/ml-mkqa/master/dataset/mkqa.jsonl.gz
```

Preprocess data:

```
python data_scripts/preprocess_xmkqa.py mkqa.jsonl xmkqa
```

Generate embeddings:

```
python generate_passage_embeddings.py \
    --model_name_or_path facebook/mcontriever \
    --output_dir mcontriever_embeddings  \
    --passages psgs_w100.tsv \
    --shard_id 0 --num_shards 1 \
    --lowercase --normalize_text \
```

Alternatively, download passage embeddings pre-computed with mContriever or mContriever-msmarco:

```
wget https://dl.fbaipublicfiles.com/contriever/embeddings/mcontriever/wikipedia_embeddings.tar
wget https://dl.fbaipublicfiles.com/contriever/embeddings/mcontriever-msmarco/wikipedia_embeddings.tar
```

Retrieve passages and compute retrieval accuracy:

```
python passage_retrieval.py \
    --model_name_or_path facebook/mcontriever \
    --passages psgs_w100.tsv \
    --passages_embeddings "mcontriever_embeddings/*" \
    --data "xmkqa/*.jsonl" \
    --output_dir mcontriever_xmkqa \
    --lowercase --normalize_text \
```

| R@100               |   avg |   en |   ar |   fi |   ja |   ko |   ru |   es |   sv |   he |   th |   da |   de |   fr |   it |   nl |   pl |   pt |   hu |   vi |   ms |   km |   no |   tr |   zh-cn |   zh-hk |   zh-tw |
|---------------------|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|---------|---------|---------|
| mContriever         |  49.2 | 65.3 | 43.0 | 43.1 | 47.1 | 44.8 | 51.8 | 37.2 | 54.5 | 44.7 | 51.4 | 49.3 | 49.0 | 50.2 | 56.7 | 61.7 | 44.4 | 54.5 | 47.7 | 45.1 | 56.7 | 27.8 | 50.2 | 44.3 |    54.3 |    51.9 |    52.5 |
| mContriever-msmarco |  65.6 | 75.6 | 53.3 | 66.6 | 60.4 | 55.4 | 64.7 | 70.0 | 70.8 | 59.6 | 63.5 | 72.0 | 66.6 | 70.1 | 70.3 | 71.4 | 68.8 | 68.5 | 66.7 | 67.8 | 71.6 | 37.8 | 71.5 | 68.7 |    64.1 |    64.5 |    64.3 |

| R@20                |   avg |   en |   ar |   fi |   ja |   ko |   ru |   es |   sv |   he |   th |   da |   de |   fr |   it |   nl |   pl |   pt |   hu |   vi |   ms |   km |   no |   tr |   zh-cn |   zh-hk |   zh-tw |
|---------------------|-------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|---------|---------|---------|
| mContriever         |  31.4 | 50.2 | 26.6 | 26.7 | 29.4 | 27.9 | 32.7 | 20.7 | 37.6 | 22.2 | 31.1 | 31.2 | 31.2 | 30.7 | 38.6 | 45.1 | 25.1 | 37.6 | 28.3 | 27.3 | 39.6 | 15.7 | 33.2 | 26.5 |    35.0 |    32.7 |    32.5 |
| mContriever-msmarco |  53.9 | 67.2 | 40.1 | 55.1 | 46.2 | 41.7 | 52.3 | 59.3 | 60.0 | 45.6 | 52.0 | 62.0 | 54.8 | 59.3 | 59.4 | 60.9 | 58.1 | 56.9 | 55.2 | 55.9 | 60.9 | 26.2 | 61.0 | 56.7 |    50.9 |    51.9 |    51.2 |

## Training

### Data pre-processing

We perform pre-training on data from CCNet and Wikipedia. Contriever, the English monolingual model, is trained on English data from Wikipedia and CCNet. mContriever, the multilingual model, is pre-trained on 29 languages using data from CCNet. After converting data into a text file, we tokenize and chunk it into multiple sub-files using the [`data_scripts/tokenization_script.sh`](data_scripts/tokenization_script.sh) . The different chunks are then loaded separately by the different processes in a distributed job. For mContriever, we use the option `--normalize_text` to preprocess data, this normalize certain common caracters that are not present in mBERT tokenizer.

### Training

[`train.py`](train.py) provides the code for the contrastive training phase of Contriever.

For Contriever, the English monolingual model, we use the following options on 32 gpus:

```
python train.py \
        --retriever_model_id bert-base-uncased --pooling average \
        --augmentation delete --prob_augmentation 0.1 \
        --train_data "data/wiki/ data/cc-net/" --loading_mode split \
        --ratio_min 0.1 --ratio_max 0.5 --chunk_length 256 \
        --momentum 0.9995 --moco_queue 131072 --temperature 0.05 \
        --warmup_steps 20000 --total_steps 500000 --lr 0.00005 \
        --scheduler linear --optim adamw --per_gpu_batch_size 64 \
        --output_dir /checkpoint/gizacard/contriever/xling/contriever \
```

For mContriever, the multilingual model, we use the following options on 32 gpus:

```
TDIR=encoded-data/bert-base-multilingual-cased/
TRAINDATASETS="${TDIR}fr_XX ${TDIR}en_XX ${TDIR}ar_AR ${TDIR}bn_IN ${TDIR}fi_FI ${TDIR}id_ID ${TDIR}ja_XX ${TDIR}ko_KR ${TDIR}ru_RU ${TDIR}sw_KE ${TDIR}hu_HU ${TDIR}he_IL ${TDIR}it_IT ${TDIR}km_KM ${TDIR}ms_MY ${TDIR}nl_XX ${TDIR}no_XX ${TDIR}pl_PL ${TDIR}pt_XX ${TDIR}sv_SE ${TDIR}te_IN ${TDIR}th_TH ${TDIR}tr_TR ${TDIR}vi_VN ${TDIR}zh_CN ${TDIR}zh_TW ${TDIR}es_XX ${TDIR}de_DE ${TDIR}da_DK"

python train.py \
        --retriever_model_id bert-base-multilingual-cased --pooling average \
        --train_data ${TRAINDATASETS} --loading_mode split \
        --ratio_min 0.1 --ratio_max 0.5 --chunk_length 256 \
        --momentum 0.999 --moco_queue 32768 --temperature 0.05 \
        --warmup_steps 20000 --total_steps 500000 --lr 0.00005 \
        --scheduler linear --optim adamw --per_gpu_batch_size 64 \
        --output_dir /checkpoint/gizacard/contriever/xling/mcontriever \
```

The full training script used on our slurm cluster are available in the [`example_scripts`](example_scripts) folder.

## References

If you find this repository useful, please consider giving a star and citing this work:

[1] G. Izacard, M. Caron, L. Hosseini, S. Riedel, P. Bojanowski, A. Joulin, E. Grave [*Unsupervised Dense Information Retrieval with Contrastive Learning*](https://arxiv.org/abs/2112.09118)

```
@misc{izacard2021contriever,
      title={Unsupervised Dense Information Retrieval with Contrastive Learning}, 
      author={Gautier Izacard and Mathilde Caron and Lucas Hosseini and Sebastian Riedel and Piotr Bojanowski and Armand Joulin and Edouard Grave},
      year={2021},
      url = {https://arxiv.org/abs/2112.09118},
      doi = {10.48550/ARXIV.2112.09118},
}
```

## License

See the [LICENSE](LICENSE) file for more details.