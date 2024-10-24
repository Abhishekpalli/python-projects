from sentence_transformers import SentenceTransformer
import pandas as pd

# Load the cleaned data
courses_df = pd.read_csv('cleaned_courses.csv')  # Assuming the cleaned file is saved

# Load a pre-trained embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Generate embeddings for course titles
courses_df['Embeddings'] = list(model.encode(courses_df['Title'].tolist(), convert_to_tensor=True))

# Save the embeddings for later use
courses_df.to_csv('courses_with_embeddings.csv', index=False)