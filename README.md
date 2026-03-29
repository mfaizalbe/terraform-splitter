# terraform-splitter
A simple Python tool to automatically split a `main.tf` into multiple Terraform files, preserving comments and organizing blocks by type for easier management.

---

## Features

- Automatically detects `main.tf` in the current folder  
- Splits Terraform blocks into separate files:
  - `provider.tf`
  - `variables.tf`
  - `outputs.tf`
  - `data.tf`
  - `locals.tf`
  - `modules.tf`  
- Splits resource blocks by type (e.g., `s3.tf`, `cloudfront.tf`)  
- Preserves all comments  
- Keeps multi-line blocks intact  

---

## Installation & Usage

1. Make sure you have **Python 3** installed  

2. Copy the Python script (`terraform_splitter.py`) to the folder where your `main.tf` is located.

3. Go to that folder in the terminal:

```bash
cd /path/to/your/terraform/project
```

4. Run the splitter:

```bash
python3 terraform_splitter.py
```

# Possible Future Enhancements

- Allow running the script from any directory without moving the Python file (by passing the project folder as an argument)
- Automatically detect modules and split them into separate files
- Add support for custom naming rules for resource files
- Optionally, integrate with pre-commit hooks for automatic splitting
- Add a dry-run mode to preview changes before creating files