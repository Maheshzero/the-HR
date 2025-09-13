
input_file = r"C:\Users\mahes\OneDrive\Desktop\WindowsUpdate.log"
output_file = r"C:\Users\mahes\OneDrive\Desktop\FilteredUpdateLog.txt"

# Keywords to search for
keywords = ["Error", "Warning", "Fail", "0x8"]

with open(input_file, "r", encoding="utf-8", errors="ignore") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    
    for line in infile:
        if any(keyword in line for keyword in keywords):
            outfile.write(line)

print(f"Filtered log saved to: {output_file}")