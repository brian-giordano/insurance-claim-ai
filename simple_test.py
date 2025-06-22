import os

# Print current directory
print(f"Current directory: {os.getcwd()}")

# Check if file exists
sample_path = "data/sample_claims/water_damage_claim.txt"
print(f"File exists: {os.path.exists(sample_path)}")

# Try to read the file
try:
    with open(sample_path, 'r') as f:
        content = f.read()
        print(f"File content length: {len(content)}")
        print(f"First 100 characters: {content[:100]}")
except Exception as e:
    print(f"Error reading file: {e}")