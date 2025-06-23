import os
import pandas as pd

class TemplateProfile:
    def __init__(self, name, field_ids, field_names):
        self.name = name  # Template name or program area
        self.field_ids = field_ids  # List from row 0
        self.field_names = field_names  # List from row 1

def load_template(file_path):
    try:
        df = pd.read_csv(file_path, header=None)
        field_ids = list(df.iloc[0])  # First row: Apricot field IDs
        field_names = list(df.iloc[1])  # Second row: Friendly names

        template_name = os.path.splitext(os.path.basename(file_path))[0]
        return TemplateProfile(template_name, field_ids, field_names)
    except Exception as e:
        print(f"Error loading template: {file_path}\n{str(e)}")
        return None

def load_all_templates(folder_path):
    templates = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            full_path = os.path.join(folder_path, filename)
            profile = load_template(full_path)
            if profile:
                templates[profile.name] = profile
    return templates