import json

def extract_resource_types(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)

    resource_types = set()

    for entry in data.get("entry", []):
        resource = entry.get("resource", {})
        resource_type = resource.get("resourceType")
        if resource_type:
            resource_types.add(resource_type)

    return resource_types

if __name__ == "__main__":
    file_path = "sample_file.json"  # Adjust if needed
    types_found = extract_resource_types(file_path)
    
    print("✅ Resource types found in sample_file.json:")
    for t in sorted(types_found):
        print(f" - {t}")
