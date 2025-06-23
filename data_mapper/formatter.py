import os
import pandas as pd

def load_field_value_mapping(mapping_path):
    try:
        mapping_df = pd.read_csv(mapping_path)
        return mapping_df.groupby("Field Name").apply(
            lambda x: dict(zip(x["Incoming Value"], x["Apricot Value"]))
        ).to_dict()
    except:
        return {}

def format_data(input_path, template_profile, program_name, mapping_folder, output_folder):
    # Load raw file
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    # Build output DataFrame in correct column order
    output_df = pd.DataFrame(columns=template_profile.field_ids)

    # Try to match headers from input to template
    for i, field in enumerate(template_profile.field_ids):
        for col in df.columns:
            if field.strip().lower() == col.strip().lower():
                output_df[field] = df[col]
                break

    # Load value mapping (if any)
    mapping_file = os.path.join(mapping_folder, f"{program_name}_field_values.csv")
    mappings = load_field_value_mapping(mapping_file)

    for field, replacements in mappings.items():
        if field in output_df.columns:
            output_df[field] = output_df[field].replace(replacements)

    # Save output
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_name = f"{filename}_formatted.csv"
    output_path = os.path.join(output_folder, output_name)
    output_df.to_csv(output_path, index=False)

    return output_path