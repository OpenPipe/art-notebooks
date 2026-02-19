Notebooks to demonstrate ART (Agent Reinforcement Trainer) in practice!

## 📒 Notebooks

| Agent Task          | Example Notebook                                                                                                                       | Description                                         | Comparative Performance                                                                                                                                                                                                                             |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ART•E [Serverless]**   | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/art-e.ipynb)                       | Qwen 3 14B learns to search emails using RULER     | <img src="https://github.com/openpipe/art-notebooks/raw/main/assets/benchmarks/email_agent/accuracy-training-progress.svg" height="72"> [benchmarks](https://github.com/openpipe/art/blob/main/dev/art-e/art_e/evaluate/display_benchmarks.ipynb)   |
| **2048**            | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/2048/2048.ipynb)                   | Qwen 3 14B learns to play 2048                     | <img src="https://github.com/openpipe/art-notebooks/raw/main/assets/benchmarks/2048/accuracy-training-progress.svg" height="72"> [benchmarks](https://github.com/openpipe/art/blob/main/examples/2048/display_benchmarks.ipynb)                     |
| **ART•E LangGraph** | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/langgraph/art-e-langgraph.ipynb)   | Qwen 2.5 7B learns to search emails using LangGraph | [Link coming soon]                                                                                                                                                                                                                                  |
| **MCP•RL**          | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/mcp-rl/mcp-rl.ipynb)               | Qwen 2.5 3B masters the NWS MCP server              | [Link coming soon]                                                                                                                                                                                                                                  |
| **Temporal Clue**   | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/temporal_clue/temporal-clue.ipynb) | Qwen 2.5 7B learns to solve Temporal Clue           | [Link coming soon]                                                                                                                                                                                                                                  |
| **Tic Tac Toe**     | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/tic_tac_toe/tic-tac-toe.ipynb)     | Qwen 2.5 3B learns to play Tic Tac Toe              | <img src="https://github.com/openpipe/art-notebooks/raw/main/assets/benchmarks/tic-tac-toe-local/accuracy-training-progress.svg" height="72"> [benchmarks](https://github.com/openpipe/art/blob/main/examples/tic_tac_toe/display-benchmarks.ipynb) |
| **Codenames**       | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/codenames/Codenames_RL.ipynb)      | Qwen 2.5 3B learns to play Codenames                | <img src="https://github.com/openpipe/art-notebooks/raw/main/assets/benchmarks/codenames/win_rate_over_time.png" height="72"> [benchmarks](https://github.com/OpenPipe/ART/blob/main/examples/codenames/Codenames_RL.ipynb)                         |
| **AutoRL [RULER]**  | [🏋️ Train agent](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/auto_rl.ipynb)                     | Train Qwen 2.5 7B to master any task                | [Link coming soon]                                                                                                                                                                                                                                  |
| **SFT from File**   | [🏋️ Train model](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/sft/train_from_file.ipynb)         | Fine-tune Qwen 3 30B on text-to-SQL from a dataset  | [Link coming soon]                                                                                                                                                                                                                                  |
| **Distillation**    | [🏋️ Train model](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/sft/distillation.ipynb)            | Distill text-to-SQL from Qwen 3 235B to Qwen 3 30B  | [Link coming soon]                                                                                                                                                                                                                                  |
| **SFT + RL**        | [🏋️ Train model](https://colab.research.google.com/github/openpipe/art-notebooks/blob/main/examples/sft/sft-rl.ipynb)                  | Train a document summarizer with SFT warmup then RL  | [Link coming soon]                                                                                                                                                                                                                                  |

## 🧩 Supported Models

ART should work with most vLLM/HuggingFace-transformers compatible causal language models, or at least the ones supported by [Unsloth](https://docs.unsloth.ai/get-started/all-our-models). Gemma 3 does not appear to be supported for the time being. If any other model isn't working for you, please let us know on [Discord](https://discord.gg/zbBHRUpwf4) or open an issue on [GitHub](https://github.com/openpipe/art-notebooks/issues)!

## 🤝 Contributing

ART is in active development, and contributions are most welcome! Please see the [CONTRIBUTING.md](https://github.com/openpipe/art-notebooks/blob/main/CONTRIBUTING.md) file for more information.

## ⚖️ License

This repository's source code is available under the [Apache-2.0 License](LICENSE).

## 🙏 Credits

ART stands on the shoulders of giants. While we owe many of the ideas and early experiments that led to ART's development to the open source RL community at large, we're especially grateful to the authors of the following projects:

- [Unsloth](https://github.com/unslothai/unsloth)
- [vLLM](https://github.com/vllm-project/vllm)
- [trl](https://github.com/huggingface/trl)
- [torchtune](https://github.com/pytorch/torchtune)
- [SkyPilot](https://github.com/skypilot-org/skypilot)

Finally, thank you to our partners who've helped us test ART in the wild! We're excited to see what you all build with it.

[pypi-url]: https://pypi.org/project/openpipe-art/
[contribute-url]: https://github.com/openpipe/art-notebooks/blob/main/CONTRIBUTING.md
[contribute-image]: https://img.shields.io/badge/PRs-welcome-blue.svg
