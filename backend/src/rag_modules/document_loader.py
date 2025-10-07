from langchain_community.document_loaders import TextLoader
import os


class DocumentLoader:
    """
    DocumentLoader is a class for loading text and log files from a specified directory.
    Attributes:
        directory (str): The path to the folder containing the files to load.
    Methods:
        load_logs():
            Scans the directory for files ending with '.txt' or '.log',
            loads their contents using TextLoader, and returns a list of documents.
    """

    def __init__(self, directory):
        self.directory = directory

    def load_logs(self):
        logs = []
        for filename in os.listdir(self.directory):
            if filename.endswith(".txt") or filename.endswith(".log"):
                path = os.path.join(self.directory, filename)
                loader = TextLoader(path)
                docs = loader.load()
                logs.extend(docs)
        return logs
