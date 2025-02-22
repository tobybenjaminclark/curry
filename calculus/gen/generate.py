import os

def generate_agda_record(name, components):
    """
    Generates an Agda record definition for a compound object.
    
    :param name: The name of the record (e.g., "Cake")
    :param components: A list of component names (e.g., ["Milk", "BakingPowder", "Egg", "Flour"])
    :return: Agda code as a string
    """
    # Create fields for each component's entity and proof.
    entity_fields = [f"e{i}  :   Entity" for i in range(1, len(components) + 1)]
    proof_fields = [
        f"p{i}  :   is{component.replace(' ', '')} e{i}"
        for i, component in enumerate(components, 1)
    ]
    
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


def generate_agda_code(ingredients, substitutes, compound_objects):
    """
    Generates the complete Agda code for the given ingredients, substitutes, and compound objects.
    
    :param ingredients: List of ingredient names.
    :param substitutes: List of tuples (substitute, base).
    :param compound_objects: Dict mapping compound name to a list of components.
    :return: The Agda code as a string.
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
    for obj_name, components in compound_objects.items():
        agda_code += generate_agda_record(obj_name, components)
    
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
    
    Each line should be of the form:
      Compound : Component1 & Component2 & ...
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
                # Split components on "&" and remove extra spaces.
                components = [comp.strip().replace(" ", "") for comp in components_str.split("&") if comp.strip()]
                compounds[obj_name] = components
    return compounds


def main():
    # Define file names.
    primitives_file = "gen/primitives.txt"
    substitutes_file = "gen/substitutes.txt"
    compounds_file = "gen/compounds.txt"
    
    # Check that each file exists.
    for filename in [primitives_file, substitutes_file, compounds_file]:
        if not os.path.exists(filename):
            print(f"File '{filename}' not found!")
            return
    
    # Parse each file.
    primitives = parse_primitives_file(primitives_file)
    substitutes = parse_substitutes_file(substitutes_file)
    compound_objects = parse_compounds_file(compounds_file)
    
    # Generate Agda code.
    agda_code = generate_agda_code(primitives, substitutes, compound_objects)
    output_file = "cooking_primitives.agda"
    
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(agda_code)
    
    print(f"Agda code generated and saved to '{output_file}'")


if __name__ == "__main__":
    main()