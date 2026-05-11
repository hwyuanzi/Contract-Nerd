# from clause_generation import clause_generation
import os

from clause_comparison import clause_comparison

def main():
    # Define parameters
    contract_path = "D:/Downloads/Academics/Capstone Project/Data/Risky Clauses/Rental/New York/risky_clauses4b.txt"
    # contract_path = "D:/Downloads/Academics/Capstone Project/Data/Contracts/Rental/New York/Contract 7.pdf"
    output_file   = "D:/Downloads/Academics/Capstone Project/Data/Risky Clauses/Rental/New York/risky_clauses.txt"
    law_path      = "D:/Downloads/Academics/Capstone Project/Data/Regulations/Residential tenants’ rights guide.pdf"#,"D:/Downloads/Academics/Capstone Project/Data/Regulations/The Complete Guide on Landlord Tenant Laws - New York.pdf"
    api_base      = "https://api.sambanova.ai/v1"
    api_key       = os.environ.get("SAMBANOVA_API_KEY")
    model         = 'Meta-Llama-3.3-70B-Instruct'
    role          = "user"
    temperature   = 0.1
    top_p         = 0.1
    max_tokens    = 8192

    # # Generate transformed clauses
    # transformed_clauses = clause_generation(1
    #     contract_path, output_file, model, role, api_key, api_base, temperature, top_p, max_tokens
    # )

    legal_doc_path = f"D:/Downloads/Academics/Capstone Project/Data/Regulations/Rental/New York/regulations.pdf"

    if not api_key:
        raise RuntimeError("Set SAMBANOVA_API_KEY before running this script.")

    # Compare clauses
    final_evaluation = clause_comparison(
        contract_path = contract_path,
        law_path      = legal_doc_path,
        risky_clauses = output_file,
        model         = model,
        role          = role,
        api_key       = api_key,
        api_base      = api_base,
        temperature   = temperature,
        top_p         = top_p,
        max_tokens    = max_tokens
    )


    print(final_evaluation)

if __name__ == "__main__":
    main()
