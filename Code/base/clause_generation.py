import pickle
import os
import time
import openai
from Code.base.utils.functions import read_pdf_pymupdf, extract_with_llm  # If publishing the code using flask
# from utils.functions import read_pdf_pymupdf, extract_info  # If testing locally

def clause_generation(contract_path, output_file, model, role, api_base, api_key, temperature, top_p, max_tokens, retries = 5):
    # Define Llama client
    client = openai.OpenAI(
        api_key  = api_key,
        base_url = api_base,
    )

    # Function to transform clauses using Llama
    def llama_transformation(clause, retries):
        prompt = f"""
            You are a contract language specialist tasked with identifying and creating transformations of contract clauses to illustrate linguistic and legal ambiguities. Using the clause provided, apply each of the following transformations:
                1. Lexical Ambiguity: Adjust the clause so that it contains terms or phrases with multiple possible interpretations due to insufficient context.
                2. Syntactic Ambiguity: Restructure the clause so the grammatical relationship between words or phrases is unclear or open to multiple interpretations.
                3. Undue Generality: Remove specific details or context to make the clause overly broad or vague, so it becomes unclear what it applies to.
                4. Redundancy: Add unnecessary or repetitive terms that restate the same information, leading to redundancy in the clause.
                5. A combination of all of the above.

            CLAUSE:
            {clause}

            The output should strictly be of the following format, with no exceptions. Do not include explanations:
            'Original Clause: abc
            Lexical Ambiguity: def
            Syntactic Ambiguity: ghi
            Undue Generality: jkl
            Redundancy: mno
            Combination: pqr'
        """

        delay = 5
        for i in range(retries):
            try:
                response = client.chat.completions.create(
                    model       = model,
                    messages    = [{"role": role, "content": prompt}],
                    temperature = temperature,
                    top_p       = top_p,
                    max_tokens  = max_tokens,
                )
                return response.choices[0].message.content
            except Exception as e:
                if "rate limit" in str(e).lower():
                    print(f"Rate limit hit. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2
                else:
                    print(f"Error: {e}")
                    break
        print(f"Failed to get a response for post after {retries} retries.")
        return None

    # Read the contract file
    contract_text = read_pdf_pymupdf(contract_path)

    # Extract clauses from the contract
    clauses = extract_with_llm(
        document = contract_text,
        prompt = "Identify the contract clauses in this contract, detailing all figures and necessary specifics. Do not use any \\n characters within individual clauses - only use it to separate clauses, all parts of an individual clause must be written without any \\n characters. Include the clause name and detail in the same line (e.g., rent:...). Don't number the clauses:",
        client = client,
        model  = model,
        role   = role,
        temperature = temperature,
        top_p  = top_p,
        max_tokens = max_tokens,
    )

    # Split clauses and clean up the list
    clauses_list = [item for item in clauses.split("\n") if item]

    # Transform clauses
    transformed_clauses = []
    for clause in clauses_list:
        result = llama_transformation(clause, retries)
        if result:
            transformed_clauses.append(result)

    # Save to file
    with open(output_file, 'wb') as file:
        pickle.dump(transformed_clauses, file)
    print(f"Output saved to {output_file}")

    return transformed_clauses

if __name__ == "__main__":
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        raise RuntimeError("Set SAMBANOVA_API_KEY before running this script.")

    transformed_clauses = clause_generation(
        contract_path = "D:/Downloads/Academics/Capstone Project/Data/Gold Standards/Rental/New York/Contract 1.pdf",
        output_file   = "D:/Downloads/Academics/Capstone Project/Data/Risky Clauses/RentalNew York/risky_clauses.pkl",
        model         = 'Meta-Llama-3.1-405B-Instruct',
        role          = "user",
        api_key       = api_key,
        api_base      = "https://api.sambanova.ai/v1",
        temperature   = 0.1,
        top_p         = 1.0,
        max_tokens    = 4096
    )
