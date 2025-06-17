import os
import json
import google.generativeai as genai

# --- Configuration & Initialization ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # Using a fast and capable model
    generation_config={"response_mime_type": "application/json"},
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
)

# --- Main Function ---
def main():
    commit_url = os.environ.get("COMMIT_URL")
    commit_message = os.environ.get("COMMIT_MESSAGE")
    if not commit_url or not commit_message:
        print("ERROR: COMMIT_URL or COMMIT_MESSAGE env vars not provided.")
        exit(1)

    prompt = f"""
    You are an expert AI code reviewer and technical writer for the Chiron Guild. Your task is to analyze a Git commit and provide a structured summary.
    Analyze the code changes found at the following URL. The original commit message was:

    --- COMMIT MESSAGE ---
    {commit_message}
    --- END COMMIT MESSAGE ---

    Based on your analysis of the code changes (the 'diff') and the commit message, provide a JSON object with the following three keys:
    1. "objective": A concise, one-sentence statement describing the primary goal or purpose of this commit. Infer the 'why' behind the changes.
    2. "summary_of_changes": A brief, plain-language summary of what was technically done. Mention the files changed and the nature of the changes (e.g., 'added a function', 'refactored a class', 'fixed a bug').
    3. "constructive_critique": A brief, objective critique of the code changes. If the code is excellent, state that. If there are potential improvements (e.g., 'a variable could be named more clearly', 'this function could benefit from more comments', 'consider adding a unit test for this edge case'), mention them constructively. If the commit is too simple for a critique (e.g., a typo fix), state that.

    Return ONLY the raw JSON object, with no other text or markdown formatting.
    """

    try:
        print(f"Sending request to Gemini with URL: {commit_url}")
        # Use the URL Context Tool by including the URL directly in the prompt
        response = model.generate_content([prompt, commit_url])
        
        # Write the JSON response to a file for the workflow to use
        with open('enrichment_output.json', 'w') as f:
            f.write(response.text)
        print("Successfully generated enrichment data.")

    except Exception as e:
        print(f"ERROR: An error occurred while calling Gemini API: {e}")
        exit(1)

if __name__ == "__main__":
    main()