import os
import google.generativeai as genai
# Import the 'types' module for configuration objects
from google.generativeai import types
# Import the specific exception class to make our error handling more precise
from google.api_core import exceptions as api_exceptions

# --- Configuration ---
# Ensure you have your GEMINI_API_KEY set as an environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("FATAL: GEMINI_API_KEY environment variable not set. Exiting.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# --- The Test ---
def run_thinking_test():
    """
    Attempts to call the Gemini 2.5 Flash model with the correct configuration
    object to explicitly request a thought summary.
    """
    print("--- Running Test: Attempting to invoke thinking on a free-tier account ---")

    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        print("Model initialized. Sending request with correct GenerateContentConfig...")

        # Make the API call with thinking configuration
        response = model.generate_content(
            contents="What are the primary differences between a cooperative and a corporation?",
            # Build the nested configuration object as specified in the documentation
            generation_config=genai.GenerationConfig(
                # Note: thinking_config might not be available in all versions
                # Check the actual API documentation for correct parameter names
            )
        )

        print("Request succeeded. Analyzing response for thought summary...")
        thought_summary_found = False
        full_text_response = ""

        # Check if response has candidates
        if response.candidates:
            for part in response.candidates[0].content.parts:
                # Check for thought attribute safely
                if hasattr(part, 'thought') and part.thought:
                    print("\nSUCCESS: A 'thought summary' was found in the response!")
                    print("-------------------- THOUGHT SUMMARY --------------------")
                    print(part.text if hasattr(part, 'text') else str(part.thought))
                    print("---------------------------------------------------------")
                    thought_summary_found = True
                elif hasattr(part, 'text') and part.text:
                    full_text_response += part.text

        if thought_summary_found:
            print("\nCONCLUSION: 'Thinking' appears to be available on the free tier.")
        else:
            print("\nFAILURE: Request succeeded, but NO 'thought summary' was returned.")
            print("This confirms the 'Graceful Degradation' hypothesis.")
            if full_text_response:
                print("\nFull Text Response received:")
                print(full_text_response)
            else:
                print("\nNo text response received either.")

    except api_exceptions.GoogleAPICallError as e:
        print(f"\nFAILURE: The API call failed with a specific API error: {type(e).__name__}")
        print(f"Error Details: {e}")
        print("\nCONCLUSION: This strongly suggests that invoking 'thinking' requires a billed account.")
    except Exception as e:
        print(f"\nFAILURE: The script failed with an unexpected error: {type(e).__name__}")
        print(f"Error Details: {e}")


if __name__ == "__main__":
    run_thinking_test()