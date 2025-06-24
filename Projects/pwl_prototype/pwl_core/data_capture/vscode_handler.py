"""
A simple Python script invoked by the VS Code extension on a file save event.
This script's only job is to print the received file path to standard output.
"""

import sys

def main():
    """
    Checks for a command-line argument and prints it to stdout.
    """
    # The first argument (sys.argv[0]) is the script name itself.
    # We expect exactly one more argument: the file path.
    if len(sys.argv) == 2:
        saved_file_path = sys.argv[1]
        # Print the success message to stdout for the extension to capture.
        print(f"Successfully received save event for: {saved_file_path}")
        sys.exit(0)  # Exit with a success code
    else:
        # Print an error message to stderr for the extension to capture.
        error_msg = (
            f"Usage: python vscode_handler.py <file_path>. "
            f"Received {len(sys.argv) - 1} arguments."
        )
        print(error_msg, file=sys.stderr)
        sys.exit(1)  # Exit with a failure code

if __name__ == "__main__":
    main()