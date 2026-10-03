# ComfyUI PixAI Tagger

A ComfyUI custom node for image tagging using [PixAI Tagger v1.0](https://huggingface.co/pixai-labs/pixai-tagger-v1.0).

This node supports batch image tagging and provides both a simple tagger interface and an advanced interface with separate category outputs.

## Features

* Uses PixAI Tagger v1.0
* Batch image tagging
* Simple tagger node with a workflow similar to commonly used WD14 Tagger interfaces
* Advanced tagger node with separate outputs for each PixAI tag category
* Configurable category thresholds
* Underscore replacement
* Tag exclusion
* Optional trailing comma
* Optional model unloading after execution
* Model is downloaded automatically from Hugging Face on first use

## Nodes

### PixAI Tagger

A simple tagger designed for workflows that need a single combined tag list.

**Inputs**

| Input                 | Description                             |
| --------------------- | --------------------------------------- |
| `image`               | Input image(s)                          |
| `model`               | Hugging Face model ID                   |
| `threshold`           | Threshold for general and style tags    |
| `character_threshold` | Threshold for character tags            |
| `replace_underscore`  | Replace `_` with spaces                 |
| `trailing_comma`      | Add a trailing comma to the output      |
| `unload_model`        | Unload the model after execution        |
| `exclude_tags`        | Comma-separated list of tags to exclude |

**Output**

* `all_tags` — Combined general, character, and style tags

Default thresholds:

* General: `0.17`
* Character: `0.27`
* Style: `0.17`

> The Simple node uses a shared threshold for general and style tags for a simpler workflow. The PixAI-recommended style threshold of `0.15` is available in the Advanced node.

---

### PixAI Tagger (Advanced)

Provides separate outputs for all PixAI Tagger categories.

**Inputs**

| Input                 | Default |
| --------------------- | ------: |
| `character_threshold` |  `0.27` |
| `general_threshold`   |  `0.17` |
| `style_threshold`     |  `0.15` |
| `copyright_threshold` |  `0.24` |
| `meta_threshold`      |  `0.17` |
| `rating_threshold`    |  `0.41` |
| `replace_underscore`  | `False` |
| `unload_model`        | `False` |
| `exclude_tags`        |    `""` |

**Outputs**

* `character_tags`
* `general_tags`
* `style_tags`
* `copyright_tags`
* `meta_tags`
* `rating_tags`

The default category thresholds above follow the thresholds recommended by PixAI Tagger v1.0.

## Installation

### ComfyUI Manager

Once this project is available through ComfyUI Manager or the Comfy Registry, it can be installed directly from the Manager.

### Manual Installation

Clone this repository into your ComfyUI `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/warwk/ComfyUI-PixAI-Tagger.git
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Or, if your environment is configured for Python packages through `pyproject.toml`:

```bash
pip install .
```

Restart ComfyUI after installation.

> Do not install or replace PyTorch manually unless required by your ComfyUI environment. This node does not specify `torch` or `torchvision` as dependencies because ComfyUI normally manages its own PyTorch environment.

## Model

The default model is:

`pixai-labs/pixai-tagger-v1.0`

The model is downloaded automatically from Hugging Face when the node is used for the first time.

The model is **not included or redistributed with this repository**.

Model page:

[PixAI Tagger v1.0](https://huggingface.co/pixai-labs/pixai-tagger-v1.0)

## Example Workflow

A typical workflow can be:

```text
Load Image
    ↓
PixAI Tagger
    ↓
all_tags
    ↓
Prompt / Text Processing
```

For workflows that need category-specific tags:

```text
Load Image
    ↓
PixAI Tagger (Advanced)
    ├── character_tags
    ├── general_tags
    ├── style_tags
    ├── copyright_tags
    ├── meta_tags
    └── rating_tags
```

Both nodes support batched `IMAGE` input.

## Tag Processing

Tags are sorted by confidence score in descending order.

The following processing is applied:

1. Tags below the selected threshold are removed.
2. Tags specified in `exclude_tags` are removed.
3. Underscores can optionally be replaced with spaces.
4. Parentheses are escaped for prompt-oriented workflows.
5. Tags are joined with `, `.
6. The Simple node can optionally append a trailing comma.

For example:

```text
1girl, solo, long hair, looking at viewer
```

## Excluding Tags

Multiple tags can be excluded by separating them with commas.

Example:

```text
text, watermark, signature
```

Tag matching for exclusion is case-insensitive.

## WD14 Tagger Compatibility

The Simple `PixAI Tagger` node is designed to provide a workflow and interface similar to commonly used WD14 Tagger nodes.

This project is an independent implementation using the Transformers pipeline API and does **not** include or redistribute the source code of `ComfyUI-WD14-Tagger`.

The PixAI Tagger model and its associated implementation are provided by PixAI Labs and are subject to their respective license terms.

## Requirements

The main Python dependencies are:

* Transformers
* timm
* Hugging Face Hub
* NumPy
* Pillow

See `requirements.txt` for the Python package dependencies.

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for the complete license text.

### Third-Party Software and Models

This project uses **PixAI Tagger v1.0**, which is licensed under the **Apache License 2.0**.

PixAI Tagger v1.0:

* Repository: https://huggingface.co/pixai-labs/pixai-tagger-v1.0
* License: Apache-2.0

The PixAI Tagger model is downloaded from Hugging Face at runtime and is not bundled with this project.

This project is not affiliated with, endorsed by, or sponsored by PixAI Labs.

## Credits

* **PixAI Labs** — PixAI Tagger v1.0
* **Hugging Face** — Model hosting and Transformers ecosystem
* **ComfyUI** — ComfyUI and custom node ecosystem

## Disclaimer

This project is an independent community project.

PixAI Tagger, PixAI, and related trademarks belong to their respective owners.

## Issues and Contributions

Bug reports, feature requests, and pull requests are welcome.

When reporting an issue, please include:

* ComfyUI version
* Python version
* Operating system
* GPU and VRAM
* Relevant error message or traceback
* Node settings used when the problem occurred
