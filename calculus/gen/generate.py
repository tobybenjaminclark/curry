import os

def abbreviate(prop):
    # Take the first two letters of the property name, lower-cased.
    return prop[:2].lower()

def process_to_predicate(process):
    """
    Given a process (e.g. "chop", "bake"), return the corresponding predicate name.
    Here we use custom mappings for known processes.
    """
    if process.lower() == "chop":
        return "isChopped"
    elif process.lower() == "bake":
        return "isBaked"
    else:
        # Fallback: if the process ends with "e", add a "d"; otherwise add "ed"
        if process.endswith("e"):
            return "is" + process.capitalize() + "d"
        else:
            return "is" + process.capitalize() + "ed"

def generate_agda_record(name, groups):
    """
    Generates an Agda record definition for a compound object.
    Here, 'groups' is a list of groups, where each group is a list of properties.
    For each group, an entity field is generated and then for each property in that group,
    a corresponding proof field is generated.
    """
    num_groups = len(groups)
    # Create one entity field per group.
    entity_fields = [f"e{i}  :   Entity" for i in range(1, num_groups + 1)]
    
    # For each group, create proof fields for each property.
    proof_fields = []
    for i, group in enumerate(groups, start=1):
        for prop in group:
            proof_name = f"{abbreviate(prop)}{i}"
            proof_fields.append(f"{proof_name}  :   is{prop} e{i}")
    
    entity_section = "\n    ".join(entity_fields)
    proof_section = "\n    ".join(proof_fields)
    
    agda_code = f"""
record {name} : Set where
  constructor mk{name}
  field
    {entity_section}

    {proof_section}
"""
    return agda_code

def generate_agda_code(ingredients, substitutes, compound_objects, processes):
    """
    Generates the complete Agda code for the given ingredients, substitutes, compound objects,
    and processes.
    """
    agda_code = (
        "module cooking_primitives where\n\n"
        "open import entity\n\n"
        "postulate\n\n"
    )
    
    # Postulate type classes for each ingredient.
    for ingredient in ingredients:
        entity_name = ingredient.replace(" ", "")
        agda_code += f"  is{entity_name} : Entity → Set\n"
    agda_code += "\n"
    
    # Add coercive subtyping functions for substitutes.
    for sub, base in substitutes:
        agda_code += f"  {sub}To{base} : ∀ (e : Entity) → is{sub} e → is{base} e\n"
    agda_code += "\n"
    
    # Add process definitions.
    for process in processes:
        predicate = process_to_predicate(process)
        proc_function = process.capitalize()
        agda_code += f"  {predicate} : Entity → Set\n"
        agda_code += f"  {proc_function} : ∀ (e : Entity) → {predicate} e\n"
    agda_code += "\n"
    
    # Define records for each ingredient.
    for ingredient in ingredients:
        entity_name = ingredient.replace(" ", "")
        agda_code += (
            f"record {entity_name} : Set where\n"
            f"  constructor mk{entity_name}\n"
            f"  field\n"
            f"    e₁            : Entity\n"
            f"    proof{entity_name}      : is{entity_name} e₁\n\n"
        )
    
    # Generate compound object records.
    for obj_name, groups in compound_objects.items():
        agda_code += generate_agda_record(obj_name, groups)
    
    return agda_code

def parse_primitives_file(filepath):
    """
    Parses the primitives file.
    
    Each non-empty line is assumed to be an ingredient.
    """
    primitives = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                primitives.append(line)
    return primitives

def parse_substitutes_file(filepath):
    """
    Parses the substitutes file.
    
    Each line should be of the form:
      Substitute → Base
    (The arrow can be either "→" or "->".)
    """
    substitutes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "→" in line:
                parts = line.split("→")
            elif "->" in line:
                parts = line.split("->")
            else:
                continue  # Skip lines that do not match the expected format.
            if len(parts) == 2:
                sub = parts[0].strip().replace(" ", "")
                base = parts[1].strip().replace(" ", "")
                substitutes.append((sub, base))
    return substitutes

def parse_compounds_file(filepath):
    """
    Parses the compounds file.
    
    For compounds you can now write lines in either of two formats:
    
      1. If you use ";" then each group represents one entity whose properties are comma-separated.
         For example:
           Salad : Vegetable, Chopped ; Vegetable, Chopped
         yields two groups: [["Vegetable", "Chopped"], ["Vegetable", "Chopped"]]
         
      2. Otherwise, if you use "&", each component is taken as a separate group.
         For example:
           Cake : Milk & BakingPowder & Egg & Flour
         becomes: [["Milk"], ["BakingPowder"], ["Egg"], ["Flour"]]
    """
    compounds = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                obj_name, components_str = line.split(":", 1)
                obj_name = obj_name.strip()
                groups = []
                if ";" in components_str:
                    group_strs = components_str.split(";")
                    for group in group_strs:
                        properties = [prop.strip().replace(" ", "") for prop in group.split(",") if prop.strip()]
                        if properties:
                            groups.append(properties)
                elif "&" in components_str:
                    properties = [prop.strip().replace(" ", "") for prop in components_str.split("&") if prop.strip()]
                    groups = [[prop] for prop in properties]
                else:
                    prop = components_str.strip().replace(" ", "")
                    groups = [[prop]]
                compounds[obj_name] = groups
    return compounds

def parse_processes_file(filepath):
    """
    Parses the processes file.
    
    Each non-empty line in the file is assumed to be a process name.
    """
    processes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                processes.append(line)
    return processes

def main():
    # Define file names.
    primitives_file = "gen/primitives.txt"
    substitutes_file = "gen/substitutes.txt"
    compounds_file = "gen/compounds.txt"
    processes_file = "gen/processes.txt"
    
    # Check that each file exists.
    for filename in [primitives_file, substitutes_file, compounds_file, processes_file]:
        if not os.path.exists(filename):
            print(f"File '{filename}' not found!")
            return
    
    # Parse each file.
    primitives = parse_primitives_file(primitives_file)
    substitutes = parse_substitutes_file(substitutes_file)
    compound_objects = parse_compounds_file(compounds_file)
    processes = parse_processes_file(processes_file)
    
    # Generate Agda code.
    agda_code = generate_agda_code(primitives, substitutes, compound_objects, processes)
    output_file = "cooking_primitives.agda"
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(agda_code)
    
    print(f"Agda code generated and saved to '{output_file}'")

if __name__ == "__main__":
    main()