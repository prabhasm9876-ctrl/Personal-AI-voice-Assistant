import subprocess

def ask_offline_llm(prompt):
   
 result= subprocess.Popen(
    ["ollama", "run", "mistral"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=0
 )

 for line in result.stdout:
    text = line.decode("utf-8", errors="ignore")
    print(text, end="")
    return text
