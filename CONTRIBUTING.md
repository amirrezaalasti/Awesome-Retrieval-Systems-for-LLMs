# 🤝 Contributing to Awesome Retrieval Systems for LLMs

Thank you for helping keep this list comprehensive, accurate, and up to date!

## 🚀 Recommended: Open an Issue Form

The easiest way to propose a new entry is to open a structured GitHub issue. A workflow then checks formatting and looks for duplicates in `Readme.md`.

1. Open **[New Issue](https://github.com/amirrezaalasti/Awesome-Retrieval-Systems-for-LLMs/issues/new/choose)**.
2. Choose one of:
   - **📄 Add a Paper** — research papers and surveys
   - **🛠️ Add a Resource** — frameworks, vector DBs, benchmarks, tools, etc.
3. Fill in every required field and submit.
4. Wait for the **Validate Contribution Issue** check. It will comment with:
   - syntax / field errors
   - possible duplicates (name, arXiv ID, GitHub repo, URL)
   - a suggested README snippet if checks pass

| Label | Meaning |
| --- | --- |
| `contribution: paper` / `contribution: resource` | Submission type from the issue form |
| `validation: passed` | Automatic checks succeeded |
| `validation: failed` | Fix the reported field/syntax problems |
| `validation: duplicate` | Entry appears to already exist in `Readme.md` |

After validation passes, maintainers (or you via PR) can add the suggested snippet under the correct year and category.

You can also run the same checks locally:

```bash
python scripts/validate_contribution.py \
  --body-file /path/to/issue_body.md \
  --title "[paper] Example" \
  --labels "contribution: paper"
```

## 📋 Before You Submit

1. Search existing entries to avoid duplicates.
2. Place new resources under the correct **year** and **category**.
3. Follow the entry format used throughout the README.

## ✏️ Entry Format

Each entry should include:

- **Name** (bold)
- 📄 **Paper link** (preferred for research)
- 💻 **GitHub repository** (if available)
- 🌐 **Project page** (optional)
- 📝 **One or two sentence description**
- 🏷️ **Relevant tags** in backticks

Example:

```markdown
- **Project Name**
  - 📄 Paper: https://arxiv.org/abs/xxxx.xxxxx
  - 💻 Code: https://github.com/organization/project
  - Short description of what the project does and why it matters.
  `RAG` `GraphRAG`
```

## ✅ Inclusion Criteria

Projects should be:

- 🔍 Retrieval-centric
- 🤖 Relevant to LLMs
- 📖 Publicly documented
- 🔧 Actively maintained (preferred)
- ⭐ Widely used or academically significant

We welcome:

- 📚 Research papers and surveys
- 🛠️ Open-source frameworks
- 📊 Benchmarks and datasets
- 📏 Evaluation toolkits
- 🌐 Graph retrieval and knowledge graph systems
- 🗄️ Vector databases
- 🏢 Enterprise retrieval tools
- 🤖 Agentic retrieval frameworks

## 🔧 Alternative: Pull Request

If you prefer to edit the README yourself:

1. Fork the repository.
2. Create a branch for your changes.
3. Add or update entries in `Readme.md`.
4. Open a pull request with a clear description of what you added and why.

## 📝 Pull Request Guidelines

- Keep PRs focused on a single topic or year when possible.
- Use conventional commit messages (e.g., `docs: add LightRAG to 2024 section`).
- Double-check all links before submitting.
- Prefer opening an issue form first so automatic validation can run.

## 🐛 Reporting Issues

Open a GitHub issue for:

- Broken or outdated links
- Missing widely-used projects
- Categorization corrections
- Typos or formatting problems

For new papers/resources, prefer the dedicated issue forms above.

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
