import os
import glob
import openai
from Code.base.utils.functions import read_pdf_pymupdf, extract_with_llm  # If publishing the code using flask
# from utils.functions import read_pdf_pymupdf, extract_info  # If testing locally

def synthesize_regulations(source_folder, model, role, api_key, api_base, temperature, top_p, max_tokens):
    # Initialize OpenAI client
    client = openai.OpenAI(api_key = api_key, base_url = api_base)

    # Get all PDF file paths
    pdf_paths = glob.glob(os.path.join(source_folder, "*.pdf"))
    print(f"Found {len(pdf_paths)} PDF(s) in source folder.")

    # Store extracted clause sets from each document
    document_clause_sets = []

    for pdf_path in pdf_paths:
        print(f"Processing: {pdf_path}")
        text = read_pdf_pymupdf(pdf_path)

        clauses = extract_with_llm(
            document    = text,
            prompt      = "Extract legal provisions and clauses exactly as stated in the document. Return them as a numbered list. Do not rephrase or summarize, include the exact text in the document.",
            client      = client,
            model       = model,
            role        = role,
            temperature = temperature,
            top_p       = top_p,
            max_tokens  = max_tokens
        )

        clause_list = [clause.strip() for clause in clauses.split('\n') if clause.strip()]
        document_clause_sets.append(set(clause_list))
        # print("*" *100)
        # print(document_clause_sets)
        # print("*" * 100)

    # # Calculate union, intersection and partial overlap
    # all_clauses    = set().union(*document_clause_sets)
    # common_clauses = set.intersection(*document_clause_sets)
    # partially_common_clauses = set()
    #
    # # Find clauses that appear in more than one doc but not all
    # for clause in all_clauses:
    #     count = sum(clause in doc_set for doc_set in document_clause_sets)
    #     if 1 < count < len(document_clause_sets):
    #         partially_common_clauses.add(clause)
    #
    # # Final clauses = common to all OR unique to one
    # final_clauses = []
    # for clause in all_clauses:
    #     if clause in common_clauses:
    #         final_clauses.append(f"[COMMON] {clause}")
    #     elif sum(clause in doc_set for doc_set in document_clause_sets) == 1:
    #         final_clauses.append(f"[UNIQUE] {clause}")



    return document_clause_sets#final_clauses


if __name__ == "__main__":
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        raise RuntimeError("Set SAMBANOVA_API_KEY before running this script.")

    def save_clauses_to_txt(clause_sets, output_path):
        combined_clauses = set()
        for clause_set in clause_sets:
            combined_clauses.update(clause_set)  # Avoid duplicates

        sorted_clauses = sorted(combined_clauses,
                                key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else 9999)

        with open(output_path, 'w', encoding='utf-8') as f:
            for clause in sorted_clauses:
                f.write(clause.strip() + '\n\n')

        print(f"Saved {len(sorted_clauses)} clauses to {output_path}")

    final_output = synthesize_regulations(
        source_folder = "D:/Downloads/Academics/Capstone Project/Data/Regulations/Rental/New York/Source",
        model         = 'Meta-Llama-3.3-70B-Instruct',
        role          = "user",
        api_key       = api_key,
        api_base      = "https://api.sambanova.ai/v1",
        temperature   = 0.1,
        top_p         = 0.1,
        max_tokens    = 8192
    )

    print("\n===== FILTERED CLAUSES =====\n")
    for clause in final_output:
        print(clause)
    # print(final_output)

    save_clauses_to_txt(
        clause_sets = final_output,
        output_path = "D:/Downloads/Academics/Capstone Project/Data/Regulations/Rental/New York/regulations.txt"
    )
