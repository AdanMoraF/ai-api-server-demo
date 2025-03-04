from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_chroma import Chroma
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)
from langchain.schema.output_parser import StrOutputParser
import os

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL = "llama3-chatqa"
PROMPT_TEMPLATE = """
    Eres un asistente de soporte técnico especializado en Windows. Responde de manera clara y concisa en español a la siguiente pregunta:

    {question}

    Basándote en el siguiente contexto: {context}
"""

class DataBaseChroma:
    def __init__(self):
        self.links = [
            "https://www.argentina.gob.ar/normativa/nacional/ley-20744-25552/actualizacion",
            "https://www.argentina.gob.ar/normativa/nacional/ley-24013-412/actualizacion",
            "https://www.argentina.gob.ar/normativa/nacional/ley-24557-27971/actualizacion",
            "https://www.argentina.gob.ar/normativa/nacional/ley-11544-63368/actualizacion"
        ]
        self.titles = [
            "REGIMEN DE CONTRATO DE TRABAJO LEY N° 20.744",
            "EMPLEO Ley Nº 24.013",
            "RIESGOS DEL TRABAJO LEY N° 24.557",
            "JORNADA DE TRABAJO Ley 11.544"
        ]
        self.dataset = self.create_or_load_database()

    def split_documents(self, documents: list[Document]):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)

    def download_documents(self):
        loader = AsyncHtmlLoader(self.links)
        docs = loader.load()
        return docs

    def get_dataset(self):
        docs = self.download_documents()
        print("Texto legal descargado.")
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["article"])

        documents = []
        for i in range(len(docs_transformed)):
            metadata = {"title": self.titles[i], "source": self.links[i]}
            d = Document(metadata=metadata, page_content=docs_transformed[i].page_content)
            documents.append(d)

        chunks = self.split_documents(documents)
        print("Documentos creados.")
        return chunks

    def create_or_load_database(self):
        collection_name = "laborAI_db"
        db_directory = f"./api/resources/{collection_name}"

        embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        if not os.path.exists(db_directory):
            print("Inicio de proceso de creación de base de datos.")
            os.makedirs(db_directory)
            chunks = self.get_dataset()
            database = Chroma.from_documents(chunks, embedding=embedding, collection_name=collection_name, persist_directory=db_directory)
            print("Base de datos CREADA y cargada exitosamente.")
        else:
            database = Chroma(collection_name=collection_name, embedding_function=embedding, persist_directory=db_directory)
            print("Base de datos cargada exitosamente.")

        return database


class OllamaLangsmithModelService:
    def __init__(self):
        llm = OllamaLLM(model=MODEL)
        self.database = DataBaseChroma()
        self.retriever = self.database.dataset.as_retriever(search_type="mmr", search_kwargs={'k': 5, 'fetch_k': 50})
        retrieval = RunnableParallel({"context": self.retriever, "question": RunnablePassthrough()})
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        self.chain = retrieval | prompt | llm | StrOutputParser()
        
    def ask_question(self, question: str):
        result = self.chain.invoke(question)
        contexts = [docs.page_content for docs in self.retriever.get_relevant_documents(question)]
        return {"answer": result, "context": contexts}

