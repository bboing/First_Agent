import os
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# embedding_model = AzureOpenAIEmbeddings(
#     deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
#     model="text-embedding-ada-002",
#     openai_api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
#     openai_api_type="azure",
#     validate_base_url=False,
#     chunk_size=1000
# )

print(os.getenv("AZURE_OPENAI_API_KEY"))
print(os.getenv("AZURE_DI_KEY"))
print(os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"))
print(os.getenv("AZURE_OPENAI_ENDPOINT"))
print(os.getenv("AZURE_OPENAI_API_VERSION"))
print(os.getenv("AZURE_OPENAI_API_TYPE"))
print(f".env exists: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))}")
# print(f'embedding_model: {embedding_model}')

