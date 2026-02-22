import sys
from pathlib import Path


def remove_double_quotes(text: str) -> str:
    """Remove all double quotes from text."""
    return text.replace('"', '')


def remove_double_quotes_from_file(input_file: str, output_file: str = None) -> str:
    """Remove double quotes from a file and save to output file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = remove_double_quotes(content)
        
        if output_file is None:
            output_file = input_file.replace('.txt', '_cleaned.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        return f"Successfully cleaned file. Output saved to: {output_file}"
    except FileNotFoundError:
        return f"Error: File '{input_file}' not found"
    except Exception as e:
        return f"Error: {e}"
