from langchain_aws import BedrockLLM as Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3

AWS_REGION = "us-west-2"

bedrock = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)
model = Bedrock(model_id="amazon.titan-text-express-v1", client=bedrock)
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

question = "What themes does Gone with the Wind explore?"
# Data ingestion
loader = PyPDFLoader("assets/document.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(separators=[". \n"], chunk_size=200)
splitted_docs = splitter.split_documents(docs)

# Create vector store
vector_store = FAISS.from_documents(splitted_docs, bedrock_embeddings)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
results = retriever.invoke(question)
results_string = []
for result in results:
    results_string.append(result.page_content)

# Build template
template = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer the users questions based on the following context: {context}"),
        ("user", "{question}"),
    ]
)

chain = template.pipe(model)
response = chain.invoke({"question": question, "context": results_string})
print(response)
