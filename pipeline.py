import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from tqdm import tqdm  # Import tqdm for the progress bar

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_qa_pairs(sentence, num_pairs=3):
    qa_pairs = []
    for _ in range(num_pairs):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"Generate a question and answer based on this sentence: '{sentence}'"
                }
            ],
            model="llama3-8b-8192",  # Replace with the desired model name
        )
        qa_pairs.append(chat_completion.choices[0].message.content)
    return qa_pairs

# Read the text data from the CSV file
input_file = "wikipedia_text_data.csv"  # Replace with your CSV filename
data = pd.read_csv(input_file)

# Ensure the CSV contains a column named 'Text' for the sentences
if 'Text' not in data.columns:
    raise ValueError("CSV file must contain a 'Text' column.")

# Generate Q&A pairs with progress tracking
dataset = []
for index, row in tqdm(data.iterrows(), total=len(data), desc="Generating Q&A pairs"):
    sentence = row['Text']
    if pd.isna(sentence) or sentence.strip() == "":  # Check if sentence is NaN or empty
        continue
    
    try:
        qa_pairs = generate_qa_pairs(sentence)  # Generate three Q&A pairs for each valid sentence
        dataset.append({
            "qa_pair_1": qa_pairs[0],
            "qa_pair_2": qa_pairs[1],
            "qa_pair_3": qa_pairs[2]
        })
    except Exception as e:
        print(f"Error generating Q&A pairs for sentence at index {index}: {e}")

# Save only the generated Q&A pairs to a new CSV file
output_file = "generated_qa_pairs.csv"
df = pd.DataFrame(dataset)
df.to_csv(output_file, index=False)
print(f"Q&A pairs saved to '{output_file}'.") 


