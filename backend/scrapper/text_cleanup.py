import re
import sys
from pathlib import Path


def remove_double_quotes(text: str) -> str:
    """Remove all double quotes from text."""
    return text.replace('"', '')


def remove_double_quotes_from_file(input_file: str, output_file: str = None) -> str:
    """Remove double quotes and line breaks from a file and save to output file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove double quotes
        cleaned_content = content.replace('"', '')

        # Remove all line breaks (Windows + Unix safe)
        cleaned_content = cleaned_content.replace('\r', ' ').replace('\n', ' ')

        # Collapse multiple spaces into single space
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()

        if output_file is None:
            if input_file.endswith('.txt'):
                output_file = input_file.replace('.txt', '_cleaned.txt')
            else:
                output_file = input_file + '_cleaned'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        return f"Successfully cleaned file. Output saved to: {output_file}"

    except FileNotFoundError:
        return f"Error: File '{input_file}' not found"
    except Exception as e:
        return f"Error: {e}"
