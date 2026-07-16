# THIS PROJECT IS ARCHIVED

Intel will not provide or guarantee development of or support for this project, including but not limited to, maintenance, bug fixes, new releases or updates. Patches to this project are no longer accepted by Intel. If you have an ongoing need to use this project, are interested in independently developing it, or would like to maintain patches for the community, please create your own fork of the project.

<!-- image -->

#### Build and explore efficient retrieval-augmented generative models and applications

PyPI - Version PyPI - Downloads :round\_pushpin: Installation • :rocket: Components • :books: Examples • :red\_car: Getting Started • :pill: Demos • :pencil2: Scripts • :bar\_chart: Benchmarks

fast **RAG** is a research framework for ***efficient*** and ***optimized*** retrieval augmented generative pipelines, incorporating state-of-the-art LLMs and Information Retrieval. fastRAG is designed to empower researchers and developers with a comprehensive tool-set for advancing retrieval augmented generation.

Comments, suggestions, issues and pull-requests are welcomed! :heart:

[!IMPORTANT] Now compatible with Haystack v2+. Please report any possible issues you find.

## :mega: Updates

- **2024-05** : fastRAG V3 is Haystack 2.0 compatible :fire:
- **2023-12** : Gaudi2 and ONNX runtime support; Optimized Embedding models; Multi-modality and Chat demos; [REPLUG](https://arxiv.org/abs/2301.12652) text generation.
- **2023-06** : ColBERT index modification: adding/removing documents; see [IndexUpdater](libs/colbert/colbert/index_updater.py) .
- **2023-05** : [RAG with LLM and dynamic prompt synthesis example](examples/rag-prompt-hf.ipynb) .
- **2023-04** : Qdrant `DocumentStore` support.

## Key Features

- **Optimized RAG** : Build RAG pipelines with SOTA efficient components for greater compute efficiency.
- **Optimized for Intel Hardware** : Leverage [Intel extensions for PyTorch (IPEX)](https://github.com/intel/intel-extension-for-pytorch) , [🤗 Optimum Intel](https://github.com/huggingface/optimum-intel) and [🤗 Optimum-Habana](https://github.com/huggingface/optimum-habana) for *running as optimal as possible* on Intel® Xeon® Processors and Intel® Gaudi® AI accelerators.
- **Customizable** : fastRAG is built using [Haystack](https://github.com/deepset-ai/haystack) and HuggingFace. All of fastRAG's components are 100% Haystack compatible.

## :rocket: Components

For a brief overview of the various unique components in fastRAG refer to the [Components Overview](components.md) page.

| ***LLM Backends***                                                                                 |                                                          |
|----------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| [Intel Gaudi Accelerators](components.md#fastrag-running-llms-with-habana-gaudi-(dl1)-and-gaudi-2) | *Running LLMs on Gaudi 2*                                |
| [ONNX Runtime](components.md#fastrag-running-llms-with-onnx-runtime)                               | *Running LLMs with optimized ONNX-runtime*               |
| [OpenVINO](components.md#fastrag-running-quantized-llms-using-openvino)                            | *Running quantized LLMs using OpenVINO*                  |
| [Llama-CPP](components.md#fastrag-running-rag-pipelines-with-llms-on-a-llama-cpp-backend)          | *Running RAG Pipelines with LLMs on a Llama CPP backend* |
| ***Optimized Components***                                                                         |                                                          |
| [Embedders](scripts/optimizations/embedders/README.md)                                             | Optimized int8 bi-encoders                               |
| [Rankers](scripts/optimizations/reranker_quantization/quantization.md)                             | Optimized/sparse cross-encoders                          |
| ***RAG-efficient Components***                                                                     |                                                          |
| [ColBERT](components.md#ColBERT-v2-with-PLAID-Engine)                                              | Token-based late interaction                             |
| [Fusion-in-Decoder (FiD)](components.md#Fusion-In-Decoder)                                         | Generative multi-document encoder-decoder                |
| [REPLUG](components.md#REPLUG)                                                                     | Improved multi-document decoder                          |
| [PLAID](components.md#ColBERT-v2-with-PLAID-Engine)                                                | Incredibly efficient indexing engine                     |

## :round\_pushpin: Installation

Preliminary requirements:

- **Python** 3.8 or higher.
- **PyTorch** 2.0 or higher.

To set up the software, install from `pip` or clone the project for the bleeding-edge updates. Run the following, preferably in a newly created virtual environment:

```
pip install fastrag
```

### Extra Packages

There are additional dependencies that you can install based on your specific usage of fastRAG:

```
# Additional engines/components
pip install fastrag[intel]               # Intel optimized backend [Optimum-intel, IPEX]
pip install fastrag[openvino]            # Intel optimized backend using OpenVINO
pip install fastrag[elastic]             # Support for ElasticSearch store
pip install fastrag[qdrant]              # Support for Qdrant store
pip install fastrag[colbert]             # Support for ColBERT+PLAID; requires FAISS
pip install fastrag[faiss-cpu]           # CPU-based Faiss library
pip install fastrag[faiss-gpu]           # GPU-based Faiss library
```

To work with the latest version of fastRAG, you can install it using the following command:

```
pip install .
```

### Development tools

```
pip install .[dev]
```

## License

The code is licensed under the [Apache 2.0 License](LICENSE) .

## Disclaimer

This is not an official Intel product.