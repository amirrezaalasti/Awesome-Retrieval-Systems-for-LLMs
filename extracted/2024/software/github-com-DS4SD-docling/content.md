Docling

<!-- image -->

# Docling

DS4SD%2Fdocling | Trendshift

<!-- image -->

[arXiv](https://arxiv.org/abs/2408.09869) [Docs](https://docling-project.github.io/docling/) [PyPI version PyPI - Python Version](https://pypi.org/project/docling/) [uv](https://github.com/astral-sh/uv) [Ruff](https://github.com/astral-sh/ruff) [Pydantic v2](https://pydantic.dev/) [prek](https://pypi.org/project/prek/) [License MIT](https://opensource.org/licenses/MIT) [PyPI Downloads](https://pepy.tech/projects/docling) [Docling Actor](https://apify.com/vancura/docling) [Chat with Dosu](https://app.dosu.dev/097760a8-135e-4789-8234-90c8837d7f1c/ask?utm_source=github) [Discord](https://docling.ai/discord) [OpenSSF Best Practices](https://www.bestpractices.dev/projects/10101) [LF AI &amp; Data](https://lfaidata.foundation/projects/)

## What is Docling ?

Docling simplifies document processing by parsing diverse formats - including advanced PDF understanding - and providing seamless integrations with the generative AI ecosystem.

## Features

- 🗂️ Parsing of [multiple document formats](https://docling-project.github.io/docling/usage/supported_formats/) including PDF, DOCX, PPTX, XLSX, HTML, EPUB, WAV, MP3, WebVTT, email formats (EML, MSG), images (PNG, TIFF, JPEG, ...), LaTeX, DocLang, plain text, and more
- 📑 Advanced PDF understanding incl. page layout, reading order, table structure, code, formulas, image classification, and more
- 🧬 A unified, expressive [DoclingDocument](https://docling-project.github.io/docling/concepts/docling_document/) representation format
- ↪️ Various [export formats](https://docling-project.github.io/docling/usage/supported_formats/) and options, including Markdown, HTML, WebVTT, DocLang, [DocTags](https://arxiv.org/abs/2503.11576) and lossless JSON
- 📜 Support for several application-specific XML schemas including [DocLang](https://doclang.ai/) , [USPTO](https://www.uspto.gov/patents) patents, [JATS](https://jats.nlm.nih.gov/) articles, and [XBRL](https://www.xbrl.org/) financial reports.
- 🔒 Local execution capabilities for sensitive data and air-gapped environments
- 🤖 Plug-and-play [integrations](https://docling-project.github.io/docling/integrations/) incl. LangChain, LlamaIndex, Crew AI &amp; Haystack for agentic AI
- 🔍 Extensive OCR support for scanned PDFs and images
- 👓 Support for several Visual Language Models, such as ( [GraniteDocling](https://huggingface.co/ibm-granite/granite-docling-258M) )
- 🎙️ Audio support with Automatic Speech Recognition (ASR) models
- 🔌 Connect to any agent using the [MCP server](https://docling-project.github.io/docling/usage/mcp/)
- 🌐 Run Docling as a service with the [API server](https://docling-project.github.io/docling/usage/api_server/) (docling-serve)
- 💻 Simple and convenient CLI

### What's new

- 📄 Parsing of ODF (OpenDocument Format) files for text documents ( `.odt` ), spreadsheets ( `.ods` ), and presentations ( `.odp` )
- 💼 Parsing of XBRL (eXtensible Business Reporting Language) documents for financial reports
- 📧 Parsing of email files ( `.eml` , `.msg` )
- 📚 Parsing of EPUB (Electronic Publication) files for e-books
- 📝 Parsing of plain-text files ( `.txt` , `.text` ) and Markdown supersets ( `.qmd` , `.Rmd` )
- 📊 Chart understanding (Barchart, Piechart, LinePlot): convert them into tables or code and add detailed descriptions

### Coming soon

- 📝 Metadata extraction, including title, authors, references &amp; language
- 📝 Complex chemistry understanding (Molecular structures)

## Quickstart

### 1. Install

```
pip install docling
```

**Note:** Python 3.9 support was dropped in docling version 2.70.0. Please use Python 3.10 or higher.

Works on macOS, Linux and Windows environments for both x86\_64 and arm64 architectures.

More [detailed installation instructions](https://docling-project.github.io/docling/getting_started/installation/) are available in the docs.

## 2. Convert a document (CLI)

```
docling https://arxiv.org/pdf/2206.01062
```

This generates a .md file in the current directory containing structured document content.

You can also use 🥚 [GraniteDocling](https://huggingface.co/ibm-granite/granite-docling-258M) and other VLMs via Docling CLI:

```
docling --pipeline vlm --vlm-model granite_docling https://arxiv.org/pdf/2206.01062
```

## 3. Python usage (recommended)

```
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # a document via a local path or URL
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"
```

More advanced [usage](https://docling-project.github.io/docling/usage/) and [configuration](https://docling-project.github.io/docling/getting_started/installation/) options.

## Documentation

Check out Docling's [documentation](https://docling-project.github.io/docling/) for details on installation, usage, concepts, recipes, extensions, and more.

## Examples

Go hands-on with our [examples](https://docling-project.github.io/docling/examples/) , demonstrating how to address different application use cases with Docling.

## Integrations

To further accelerate your AI application development, check out Docling's native [integrations](https://docling-project.github.io/docling/integrations/) with popular frameworks and tools.

## Get help and support

Please feel free to connect with us using the [discussion section](https://github.com/docling-project/docling/discussions) .

## Technical report

For more details on Docling's inner workings, check out the [Docling Technical Report](https://arxiv.org/abs/2408.09869) .

## Contributing

Please read [Contributing to Docling](https://github.com/docling-project/docling/blob/main/CONTRIBUTING.md) for details.

## References

If you use Docling in your projects, please consider citing the following:

```
@techreport{Docling,
  author = {Deep Search Team},
  month = {8},
  title = {Docling Technical Report},
  url = {https://arxiv.org/abs/2408.09869},
  eprint = {2408.09869},
  doi = {10.48550/arXiv.2408.09869},
  version = {1.0.0},
  year = {2024}
}
```

## License

The Docling codebase is under MIT license. For individual model usage, please refer to the model licenses found in the original packages.

## LF AI &amp; Data

Docling is hosted as a project in the [LF AI &amp; Data Foundation](https://lfaidata.foundation/projects/) .

### IBM ❤️ Open Source AI

The project was started by the AI for knowledge team at IBM Research Zurich.