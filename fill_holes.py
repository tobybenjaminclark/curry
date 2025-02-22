import json
import subprocess

def start_agda():
    """Starts Agda in interaction mode with explicit UTF-8 encoding."""
    return subprocess.Popen(
        ["agda", "--interaction-json"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",  # Explicitly specify UTF-8 encoding
        errors="replace"  # Replaces invalid UTF-8 sequences instead of crashing
    )



def run_load_command(command: str, agda_process):
    """Sends a command to Agda's interaction mode and reads the response until an 'info' JSON is found."""
    agda_process.stdin.write(command + "\n")
    agda_process.stdin.flush()
    
    output = []
    full_message = []

    while True:
        line = agda_process.stdout.readline().strip()
        if not line:
            break
        
        output.append(line)
        full_message.append(line)
        
        try:
            data = json.loads(line)
            if "info" in data:
                return "\n".join(full_message)[5:]
        except json.JSONDecodeError:
            pass
    
    return "\n".join(output)  # Return all output if no "info" is found

def run_fill_command(command: str, agda_process):
    agda_process.stdin.write(command + "\n")
    agda_process.stdin.flush()
    
    output = []
    full_message = []

    while True:
        line = agda_process.stdout.readline().strip()
        if line[:5] == "JSON>":
            line = line[5:]
        
        output.append(line)
        full_message.append(line)
        
        try:
            data = json.loads(line)
            if "giveResult" in data:
                return data.get("giveResult").get("str")
        except json.JSONDecodeError:
            print(f"COULD NOT DECODE: {data}")

def parse_response(response):
    """Parses JSON responses from Agda."""
    response_json = "".join(response)
    try:
        return [json.loads(line) for line in response_json.splitlines()]
    except json.JSONDecodeError:
        print("Failed to parse Agda response.")
        return []

def find_hole_id(responses):
    """Finds the first hole ID in the Agda response."""
    for resp in responses:
        if resp.get("info") and isinstance(resp["info"], dict):
            if resp["info"].get("visibleGoals"):
                goals = resp["info"]["visibleGoals"]
                return [goal.get("constraintObj").get("id") for goal in goals]
    return None

def fill_hole(file_name, hole_id, agda_process):
    """Fills the given hole using Cmd_autoOne."""
    auto_fill_command = f'IOTCM "{file_name}" None Direct (Cmd_autoOne Simplified {hole_id} noRange " -m " )'
    return run_fill_command(auto_fill_command, agda_process)

def main():
    file_name = "calculus/test_one.agda"
    agda_process = start_agda()
    
    load_command = f'IOTCM "{file_name}" None Direct (Cmd_load "{file_name}" [])'
    response = run_load_command(load_command, agda_process)
    responses = parse_response(response)
    
    hole_ids = find_hole_id(responses)
    if hole_ids is None:
        print("No holes found.")
        return
    
    for hole_id in hole_ids:
        fill_response = fill_hole(file_name, hole_id, agda_process)
        print("\nFilled Hole Response:")
        print(fill_response)
    
    agda_process.stdin.close()
    agda_process.stdout.close()
    agda_process.stderr.close()
    agda_process.wait()

if __name__ == "__main__":
    main()
