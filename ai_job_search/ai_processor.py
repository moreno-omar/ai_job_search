from ollama import generate
import pandas as pd


# read from csv file
df = pd.read_csv("jobs_flat.csv")

# select text from description column
texts = df["description"].tolist()

# select first row only
text = texts[0]


# since want summary, 1-shot is fine.
response = generate(
	model="phi3:mini",
	prompt=f"List 5 points that the employer is looking for in this job description: {text}"
	)

print(response.response)