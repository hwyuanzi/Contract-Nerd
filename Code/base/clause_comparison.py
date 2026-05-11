import pickle
import os
import openai
import json
from Code.base.utils.functions import read_pdf_pymupdf, extract_info  # If publishing the code using flask
# from utils.functions import read_pdf_pymupdf, extract_info  # If testing locally

def clause_comparison(contract_path, law_path, risky_clauses, model, role, api_base, api_key, temperature, top_p, max_tokens, retries = 5):
    # Define Llama client
    client = openai.OpenAI(
        api_key  = api_key,
        base_url = api_base,
    )

    def completeness_assesment(contract, laws):
        prompt = f"""
                     You are a contract language specialist tasked with reviewing the
                     following contract relative to the gold standard contract provided.
                     Highlight each clause in the gold standard contract that is not present
                     in the provided contract and detail the possible implications of this
                     clause not being present.
                     The output should be of the following format:
                     Clause:
                     Implication if missing:   
                  """

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": role, "content": prompt}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    # Function to compare contract against relevant laws
    def law_comparison(contract, laws):

        prompt = f"""
                  You are a contract language specialist reviewing contract clauses against regulations. 
                  Output Requirements:
                  - Analyze each clause individually
                  - Use EXACTLY this format for every clause without deviation:
                      
                  Clause: "[EXACT FULL CLAUSE TEXT FROM CONTRACT]"
                  Regulation(s) Implicated: [REGULATION CITATION OR "None" IF COMPLIANT]
                  Reasoning: [CONCISE EXPLANATION OF COMPLIANCE/NON-COMPLIANCE]
                    
                  Rules:
                  1. Always include the exact clause text in quotes after "Clause:"
                  2. Never create titles or summarize clauses - use them exactly as written
                  3. If uncertain about compliance, state this in the reasoning
                  4. Never combine clauses - analyze each separately
                  5. Include all clauses, even compliant ones
                  6. Preserve all numbers and names exactly as written
                    
                  Contract Clauses:
                  {contract}
                   
                  Regulations:
                  {laws}
                  """

        response = client.chat.completions.create(
            model       = model,
            messages    = [{"role": role, "content": prompt}],
            temperature = temperature,
            top_p       = top_p,
            max_tokens  = max_tokens,
        )

        return response.choices[0].message.content

    # Function to conduct few shot learning to classify "risky" clauses
    def few_shot_learning(comparison, risky_clauses_text):
        prompt = f"""
                  You are a contract language specialist.
                  Having compared a contract against a set of regulations, you've identified the following:
                  {comparison}

                  YOUR TASK:

                  1. Risk Tier Assignment:
                     - High Risk: Clearly violates law in common scenarios
                     - Medium Risk: Potentially problematic in some contexts
                     - Low Risk: Generally compliant but needs monitoring
                
                  2. Contextual Classification:
                     - For each clause, specify:
                       * "Enforceable in [specific contexts]"
                       * OR "Unenforceable under [specific conditions]"
                     - Note any exception cases
                     
                  3. Improvement Framework:
                    - For medium/high risk clauses, suggest:
                      Alternative phrasing options
                    - For low risk clauses:
                      No changes needed.

                  Output Format:
                  - Clause: The full text of the clause.
                  - Regulation(s) Implicated: The exact regulation(s) or criteria implicated (if unenforceable).
                  - Classification: Either `enforceable` or `unenforceable`.
                  - Risk Tier: [High Risk/Medium Risk/Low Risk]
                  - Explanation of Classification: A clear explanation of why the clause was classified as enforceable or unenforceable. If a clause is one-sided in nature, make mention of this.
                  - Improvement Guidance: [Actionable steps]
                  
                  Rules:
                  1. Always include the exact clause text in quotes after "Clause:"
                  2. Never create titles or summarize clauses - use them exactly as written
                  3. If uncertain about compliance, state this in the reasoning
                  4. Never combine clauses - analyze each separately
                  5. Include all clauses, even compliant ones
                  6. Preserve all numbers and names exactly as written
                  """

        response = client.chat.completions.create(
            model       = model,
            messages    = [{"role": role, "content": prompt}],
            temperature = temperature,
            top_p       = top_p,
            max_tokens  = max_tokens,
        )

        return response.choices[0].message.content

    def language_detection(comparison):
        prompt = f"""You are provided with a list of contract clauses:
                     {comparison}
                     For each clause, the following fields are included:
                     - Clause:
                     - Regulation(s) Implicated:
                     - Classification:
                     - Risk Tier:
                     - Explanation of Classification:
                     - Improvement Guidance:
                     
                     YOUR TASK:
                     
                     - For all clauses, reproduce all the provided fields in the output.
                     - If a clause is classified as unenforceable, analyze it to determine whether it exhibits any of the following linguistic flaws:
                     1. Lexical Ambiguity: Words or phrases with multiple interpretations due to insufficient context (e.g., 'reasonable time').
                     2. Syntactic Ambiguity: Grammatical structure is unclear or confusing (e.g., 'The contractor will repair the walls with cracks').
                     3. Undue Generality: The clause is overly broad or vague in scope (e.g., 'must meet all necessary standards').
                     4. Redundancy: The clause repeats the same information unnecessarily.
                     
                     - Only mention the traits that are actually present in a clause. If no traits are present, state: 'None listed.'
                     - For enforceable clauses, do not analyze linguistic traits; instead, simply include all provided fields as-is and state: 'Not applicable' under 'Linguistic Traits Identified.'
                     
                     The output should specifically be of the following format with no exceptions:
                     - Clause:
                     - Regulation(s) Implicated:
                     - Classification:
                     - Risk Tier:
                     - Linguistic Traits Identified:
                     - Explanation of Classification:
                     - Improvement Guidance:
                     
                     Rules:
                     1. Always include the exact clause text in quotes after "Clause:"
                     2. Never create titles or summarize clauses - use them exactly as written
                     3. If uncertain about compliance, state this in the reasoning
                     4. Never combine clauses - analyze each separately
                     5. Include all clauses, even compliant ones
                     6. Preserve all numbers and names exactly as written
                  """

        response = client.chat.completions.create(
            model       = model,
            messages    = [{"role": role, "content": prompt}],
            temperature = temperature,
            top_p       = top_p,
            max_tokens  = max_tokens,
        )

        return response.choices[0].message.content

    # Read the contract file
    contract_text = read_pdf_pymupdf(contract_path)

    ##############################################################
    ######### Include Code to split clauses into batches #########
    ##############################################################

    # Unpack the list into a string
    risky_clauses_text = ""
    # for item in loaded_data:
    #     risky_clauses_text += item + ('\n\n' if 'Combination:' in item else '\n')

    # Read the regulation file
    regulations_text = read_pdf_pymupdf(law_path)

    clauses = extract_info(contract_text = contract_text)

    comparison1 = law_comparison(clauses, regulations_text)
    comparison2 = few_shot_learning(comparison1, risky_clauses_text)
    comparison3 = language_detection(comparison2)

    return comparison3

if __name__ == "__main__":
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    if not api_key:
        raise RuntimeError("Set SAMBANOVA_API_KEY before running this script.")

    final_evaluation  = clause_comparison(
        contract_path="D:/Downloads/Academics/Capstone Project/Data/Contracts/Rental/New York/Contract 7.pdf",
        law_path      = "D:/Downloads/Academics/Capstone Project/Data/Regulations/Rental/New York/regulations.txt",
        risky_clauses = "D:/Downloads/Academics/Capstone Project/Data/Risky Clauses/Rental/New York/risky_clauses.pkl",
        model         = 'Meta-Llama-3.3-70B-Instruct',
        role          = "user",
        api_key       = api_key,
        api_base      = "https://api.sambanova.ai/v1",
        temperature   = 0.1,
        top_p         = 1.0,
        max_tokens    = 4096
    )
    print(final_evaluation)
