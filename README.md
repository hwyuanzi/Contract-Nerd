# ContractNerd

ContractNerd is a research prototype for analyzing contracts with large language models. It reviews uploaded PDF contracts against jurisdiction-specific legal references and returns clause-level findings about enforceability, risk, missing terms, linguistic ambiguity, and suggested improvements.

The project accompanies the paper:

> Sinkala, M.; Duan, Y.; Yuan, H.; Shasha, D. **ContractNerd: An AI Tool to Find Unenforceable, Ambiguous, and Prejudicial Clauses in Contracts.** *Electronics* 2025, 14(21), 4212. https://doi.org/10.3390/electronics14214212

Paper page: https://www.mdpi.com/2079-9292/14/21/4212

## Authors

- Musonda Sinkala, Center for Data Science, New York University
- Yuge Duan, Department of Computer Science, Courant Institute of Mathematical Sciences, New York University
- Haowen Yuan, Department of Computer Science, Courant Institute of Mathematical Sciences, New York University
- Dennis Shasha, Department of Computer Science, Courant Institute of Mathematical Sciences, New York University

## Paper Summary

The paper introduces ContractNerd as a layperson-oriented contract analysis tool. It focuses on contracts where one party may face unfair or legally vulnerable terms, especially rental and employment agreements. ContractNerd uses LLaMA-family models to compare contract clauses against regulations and known risky clause patterns, then classifies clauses into categories such as missing clauses, unenforceable clauses, legally sound clauses, and legal but risky clauses.

The published system is built around three main ideas:

1. Jurisdiction-aware analysis: clauses are checked against local regulations and legal references instead of being evaluated in the abstract.
2. Structured risk classification: clauses are labeled with risk tiers, enforceability context, explanations, and suggested improvements.
3. User-facing explanations: the UI is designed for contract readers and writers who need practical guidance before signing or drafting an agreement.

The paper reports experiments comparing ContractNerd with contract-review tools such as goHeather, Legly, and YesChat Contract Checker. ContractNerd was evaluated on rental clauses connected to litigation and was designed to provide clearer regulatory citations, risk labels, and improvement suggestions. ContractNerd is a research and decision-support tool, not a substitute for professional legal advice.

## What ContractNerd Does

- Accepts a PDF contract upload through a Flask web interface.
- Lets the user choose a contract type and jurisdiction.
- Extracts clauses from the uploaded contract.
- Compares clauses against stored legal/regulatory documents.
- Assigns clause-level classifications and risk tiers.
- Detects legal-linguistic traits such as lexical ambiguity, syntactic ambiguity, undue generality, and redundancy.
- Returns a structured JSON response that the UI renders as a readable report.

## Current Supported Data

The repository currently includes reference materials for:

- Rental contracts in New York and Chicago.
- Employment contracts in New York and Chicago.
- Rental sample contracts for New York.
- A New York rental gold-standard contract.
- New York rental risky clause examples and experimental clause sets.

The UI exposes these choices:

- Jurisdictions: `New York`, `Chicago`
- Contract types: `Rental`, `Employment`

The active Flask route builds legal-resource paths from those values:

```text
Data/Regulations/<Contract Type>/<Jurisdiction>/regulations.pdf
Data/Risky Clauses/<Contract Type>/<Jurisdiction>/risky_clauses.txt
```

At present, the core comparison pipeline reads the uploaded PDF and the regulation PDF. The risky clause path is passed through the app for future and experimental use, but the active comparison code does not load that file directly.

## Repository Structure

```text
Contract-Nerd/
|-- Code/
|   |-- app.py
|   |-- base/
|   |   |-- __init__.py
|   |   |-- clause_comparison.py
|   |   |-- clause_generation.py
|   |   |-- main.py
|   |   |-- regulation_synthesizing.py
|   |   `-- utils/
|   |       |-- __init__.py
|   |       `-- functions.py
|   |-- static/
|   |   |-- contractnerds_logo.jpg
|   |   |-- dennis-shasha.jpg
|   |   |-- haowen-yuan.jpg
|   |   `-- musonda-sinkala.jpg
|   `-- ui/
|       `-- templates/
|           |-- about.html
|           `-- index.html
|-- Data/
|   |-- Contracts/
|   |-- Gold Standards/
|   |-- Regulations/
|   |-- Risky Clauses/
|   |-- Sample clauses/
|   `-- Tests/
|-- Documentation/
|   |-- Capstone comparable models.docx
|   |-- Sample clause.docx
|   `-- Spring 2025/
|-- .env.example
|-- .gitignore
|-- LICENSE
|-- README.md
`-- requirements.txt
```

Historical archives, local IDE metadata, and runtime upload artifacts are intentionally excluded from the active repository and covered by `.gitignore`.

## File and Folder Guide

### Root Files

| Path | Purpose |
| --- | --- |
| `README.md` | Main project documentation, paper summary, setup instructions, and structure guide. |
| `requirements.txt` | Python dependency lock list for Flask, OpenAI-compatible client calls, PDF parsing, and utility libraries. |
| `.gitignore` | Keeps virtual environments, local secrets, generated uploads, caches, archives, IDE files, and temporary files out of git. |
| `.env.example` | Template for local runtime configuration. Copy it to `.env` and add your own API key. |
| `LICENSE` | MIT License for the original ContractNerd code and repository documentation. |

### `Code/`

Source code for the web app and LLM contract-analysis pipeline.

| Path | Purpose |
| --- | --- |
| `Code/app.py` | Flask application entry point. Defines `/`, `/about`, and `/analyze`; handles PDF upload; selects legal resources; calls the clause-comparison pipeline; formats JSON for the UI. |
| `Code/base/__init__.py` | Marks `Code/base` as a Python package area for shared analysis code. |
| `Code/base/clause_comparison.py` | Core analysis pipeline. Reads the contract and regulations, extracts clauses, prompts the LLM for legal comparison, assigns risk/enforceability labels, and performs linguistic trait detection. |
| `Code/base/clause_generation.py` | Experimental helper for generating transformed risky clauses from source clauses using LLM prompts. Useful for building or expanding risky-clause examples. |
| `Code/base/main.py` | Local script-style entry point used during development for direct pipeline testing with hardcoded local paths that should be adjusted before use. |
| `Code/base/regulation_synthesizing.py` | Experimental helper for extracting/synthesizing legal provisions from regulation PDFs in a source folder. |
| `Code/base/utils/__init__.py` | Marks the utility module directory as importable. |
| `Code/base/utils/functions.py` | Shared helpers for reading PDFs with PyMuPDF, extracting text, calling the LLM for extraction tasks, and splitting contract text into numbered clauses. |

### `Code/ui/templates/`

HTML templates rendered by Flask.

| Path | Purpose |
| --- | --- |
| `Code/ui/templates/index.html` | Main web UI. Presents jurisdiction/type selectors, PDF upload, submit button, loading state, and results rendering for clause findings. |
| `Code/ui/templates/about.html` | About page with a short explanation of ContractNerd, a legal-advice disclaimer, and team information. |

### `Code/static/`

Static assets served by Flask.

| Path | Purpose |
| --- | --- |
| `Code/static/contractnerds_logo.jpg` | ContractNerd logo used in the UI and as a fallback team image. |
| `Code/static/musonda-sinkala.jpg` | Team portrait used on the About page. |
| `Code/static/haowen-yuan.jpg` | Team portrait used on the About page. |
| `Code/static/dennis-shasha.jpg` | Team portrait used on the About page. |

### `Data/`

Project data, reference documents, sample contracts, and evaluation/supporting materials.

| Path | Purpose |
| --- | --- |
| `Data/Contracts/` | Sample contracts used for testing the analyzer. |
| `Data/Contracts/Rental/New York/Contract 2.pdf` to `Contract 7.pdf` | New York rental contract PDFs used as sample inputs. |
| `Data/Contracts/Rental/New York/Contract 6.docx`, `Contract 7.docx` | Editable source versions for two sample rental contracts. |
| `Data/Gold Standards/` | Reference contracts treated as fuller or more complete examples. |
| `Data/Gold Standards/Rental/New York/Contract 1.pdf` | New York rental gold-standard contract used for completeness and comparison experiments. |
| `Data/Regulations/` | Jurisdiction and contract-type legal references used by the app. |
| `Data/Regulations/Rental/New York/regulations.pdf` | Active New York rental regulation PDF consumed by the web app. |
| `Data/Regulations/Rental/New York/regulations.txt` | Text version or extracted/synthesized New York rental regulations for experiments. |
| `Data/Regulations/Rental/New York/Source/` | Source PDFs used to build New York rental regulation references. |
| `Data/Regulations/Rental/New York/Source/NYC_tenants_rights.pdf` | NYC tenant rights source document. |
| `Data/Regulations/Rental/New York/Source/Residential tenants’ rights guide.pdf` | Residential tenant rights source guide. |
| `Data/Regulations/Rental/New York/Source/The Complete Guide on Landlord Tenant Laws - New York.pdf` | Additional New York landlord-tenant law source document. |
| `Data/Regulations/Rental/Chicago/regulations.pdf` | Chicago rental regulation PDF used when the UI selects Rental/Chicago. |
| `Data/Regulations/Rental/Chicago/regulations.txt` | Text version or extracted/synthesized Chicago rental regulations. |
| `Data/Regulations/Employment/New York/regulations.pdf` | New York employment regulation reference PDF. |
| `Data/Regulations/Employment/Chicago/regulations.pdf` | Chicago employment regulation reference PDF. |
| `Data/Risky Clauses/` | Risky-clause examples and generated variants. |
| `Data/Risky Clauses/Rental/New York/risky_clauses.txt` | Main New York rental risky-clause example file expected by the Flask resource path. |
| `Data/Risky Clauses/Rental/New York/risky_clauses2.txt`, `risky_clauses3.txt`, `risky_clauses4.txt`, `risky_clauses4b.txt` | Iterative risky-clause experiment outputs. |
| `Data/Risky Clauses/Rental/New York/risky_clauses4b.pdf` | PDF source/version corresponding to one risky-clause experiment set. |
| `Data/Sample clauses/` | Clause-level experiment files and intermediate results. |
| `Data/Sample clauses/04-07-2025/` | Clause set and results from the April 7, 2025 experiment. |
| `Data/Sample clauses/04-07-2025/All clauses.txt` | Combined clause list for the experiment. |
| `Data/Sample clauses/04-07-2025/Non-risky clauses.txt` | Non-risky clause examples. |
| `Data/Sample clauses/04-07-2025/Risky clauses 2-20-2025.txt` | Risky clauses imported from the February 20, 2025 set. |
| `Data/Sample clauses/04-07-2025/Risky clauses 3-17-2025.txt` | Risky clauses imported from the March 17, 2025 set. |
| `Data/Sample clauses/04-07-2025/Results.txt` | Results from the April 7, 2025 clause experiment. |
| `Data/Sample clauses/04-21-2025/Results.txt` | Results from the April 21, 2025 clause experiment. |
| `Data/Sample clauses/Rulings/` | Ruling-related risky-clause notes. |
| `Data/Sample clauses/Rulings/Risky clauses 2-20-2025.txt` | Risky-clause ruling notes from February 20, 2025. |
| `Data/Sample clauses/Rulings/Risky clauses 3-17-2025.txt` | Risky-clause ruling notes from March 17, 2025. |
| `Data/Sample clauses/Rulings/Risky clauses 4-7-2025.txt` | Risky-clause ruling notes from April 7, 2025. |
| `Data/Tests/` | Sample text test inputs and outputs used during development. |
| `Data/Tests/Sample testing.txt` to `Sample testing 5.txt` | Iterative sample testing files. |

### `Documentation/`

Human-readable project notes and capstone materials that remain useful for understanding the project history.

| Path | Purpose |
| --- | --- |
| `Documentation/Capstone comparable models.docx` | Notes comparing ContractNerd with related or baseline models/tools. |
| `Documentation/Sample clause.docx` | Sample clause document used for writing or testing examples. |
| `Documentation/Spring 2025/` | Spring 2025 progress notes, screenshots, and project working documents. |
| `Documentation/Spring 2025/03-10-2025.txt`, `03-17-2025.txt`, `03-24-2025.txt`, `03-31-2025.txt`, `03-31-2025 - Dennis' code.txt`, `04-07-2025.txt` | Dated development notes. |
| `Documentation/Spring 2025/To-do list.txt` | Development task list from the Spring 2025 period. |
| `Documentation/Spring 2025/Comparison.docx` | Comparison notes/documentation for model or tool outputs. |
| `Documentation/Spring 2025/0. Analyzing.png`, `1. Results.png`, `Document Upload.png`, `Landing Page.PNG` | UI screenshots and result screenshots from development. |

## Installation

Use Python 3.10 or later. Python 3.12 also works with the listed dependencies.

```bash
git clone https://github.com/hwyuanzi/Contract-Nerd.git
cd Contract-Nerd

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set your SambaNova-compatible API key:

```bash
SAMBANOVA_API_KEY=your_sambanova_api_key_here
SAMBANOVA_API_BASE=https://api.sambanova.ai/v1
SAMBANOVA_MODEL=Meta-Llama-3.3-70B-Instruct
```

On Windows, activate the environment with:

```powershell
venv\Scripts\activate
```

## Running the Web App

From the repository root:

```bash
python Code/app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Basic workflow:

1. Select a jurisdiction.
2. Select a contract type.
3. Upload a PDF contract.
4. Click the analyze button.
5. Review the clause-level report in the results panel.

Uploaded PDFs are saved temporarily to `uploads/`, which is created automatically and ignored by git.

## API Usage

The Flask app exposes one analysis endpoint:

```text
POST /analyze
```

Form fields:

| Field | Required | Description |
| --- | --- | --- |
| `jurisdiction` | Yes | Must match a folder under `Data/Regulations/<Contract Type>/`, such as `New York` or `Chicago`. |
| `contractType` | Yes | Must match a folder under `Data/Regulations/`, such as `Rental` or `Employment`. |
| `contract` | Yes | PDF contract file to analyze. |

Example with `curl`:

```bash
curl -X POST http://127.0.0.1:5000/analyze \
  -F "jurisdiction=New York" \
  -F "contractType=Rental" \
  -F "contract=@Data/Contracts/Rental/New York/Contract 2.pdf"
```

Response shape:

```json
{
  "metadata": {
    "jurisdiction": "New York",
    "contract_type": "Rental",
    "timestamp": "2026-01-01T12:00:00",
    "clause_count": 10,
    "unenforceable_count": 2
  },
  "clauses": [
    {
      "number": "1",
      "text": "Clause text",
      "classification": "Unenforceable under specific conditions",
      "risk_tier": "High Risk",
      "details": {
        "regulations": "Regulation citation",
        "linguistic_traits": "Undue Generality",
        "explanation": "Reasoning",
        "improvement_guidance": "Suggested revision"
      }
    }
  ],
  "raw": "Full model output",
  "legal_resources": {
    "regulations": "Data/Regulations/Rental/New York/regulations.pdf",
    "risky_clauses": "Data/Risky Clauses/Rental/New York/risky_clauses.txt"
  }
}
```

## Analysis Pipeline

The current app flow is:

1. `Code/app.py` receives the PDF and user selections.
2. The uploaded PDF is saved into `uploads/`.
3. The app resolves a regulation PDF under `Data/Regulations/`.
4. `Code/base/clause_comparison.py` reads the contract and regulation PDFs with PyMuPDF.
5. `extract_info()` in `Code/base/utils/functions.py` splits the contract into main numbered clauses.
6. The LLM compares clauses against the regulation text.
7. The LLM assigns risk tiers, enforceability labels, explanations, and improvement guidance.
8. The LLM checks for linguistic traits in problematic clauses.
9. Flask parses the model output into JSON.
10. `Code/ui/templates/index.html` renders the results.

## Extending the Project

### Add a New Jurisdiction

Create a folder using the same name that the UI will submit:

```text
Data/Regulations/Rental/<Jurisdiction>/regulations.pdf
```

Optionally add:

```text
Data/Regulations/Rental/<Jurisdiction>/regulations.txt
Data/Risky Clauses/Rental/<Jurisdiction>/risky_clauses.txt
```

Then add a matching `<option>` to `Code/ui/templates/index.html`.

### Add a New Contract Type

Create:

```text
Data/Regulations/<Contract Type>/<Jurisdiction>/regulations.pdf
Data/Risky Clauses/<Contract Type>/<Jurisdiction>/risky_clauses.txt
```

Then add a matching `<option>` to `Code/ui/templates/index.html`.

### Update the Model Provider

The app uses the OpenAI-compatible Python client. To switch providers, set these environment variables:

```bash
SAMBANOVA_API_BASE=<provider_base_url>
SAMBANOVA_MODEL=<model_name>
SAMBANOVA_API_KEY=<provider_api_key>
```

If the provider is not OpenAI-compatible, update the client creation and chat completion calls in `Code/base/clause_comparison.py`.

## Development Notes

- Run commands from the repository root so package imports and data paths resolve correctly.
- The main supported entry point is `python Code/app.py`.
- `Code/base/clause_generation.py` and `Code/base/regulation_synthesizing.py` are research utilities, not required for the web app.
- `Code/base/main.py` contains development paths from an earlier local environment. Treat it as a scratch runner and update paths before use.
- The project currently supports PDF uploads only.
- The analysis depends on LLM output format. If you modify prompts, update the parsing logic in `Code/app.py` accordingly.

## License

The original ContractNerd source code and repository documentation are released under the MIT License. See `LICENSE` for details.

The legal reference PDFs, sample contracts, and other third-party or source-derived materials under `Data/` and `Documentation/` may be subject to their original source terms and are included for research and reproducibility context. Verify those source terms before redistributing or using those materials commercially.

The published article is open access under the Creative Commons Attribution (CC BY 4.0) license as stated by MDPI.

## Legal and Research Disclaimer

ContractNerd is an academic research prototype. It can help surface possible contract risks, but it is not legal advice and should not be treated as an authoritative legal decision-maker. Users should consult qualified legal professionals before signing, drafting, or relying on contractual terms.
