import os
from pathlib import Path
from typing import Dict, List
import uuid
from videosdk.agents import JobContext, RoomOptions, WorkerJob, Options
from pipeline import start_agent
from utils.helpers.chunking_method import chunk_by_word_count
from utils.helpers.chroma_db import ChromaVectorStore
from utils.helpers.document_loader import add_documents

def make_context() -> JobContext:
    room_options = RoomOptions(
        auth_token=os.getenv("VIDSDK_JWT_TOKEN"),
        name="Sandbox Agent",
        playground=True
    )
    return JobContext(room_options=room_options)

def _handle_ingest_directory_flow():
    dir_str = input("Enter the path to the directory to ingest (e.g., 'docs'): ").strip()
    if not dir_str:
        print("No path provided. Canceling ingestion.")
        return
    
    dir_path = Path(dir_str).expanduser().resolve()
    if not dir_path.is_dir():
        print(f"Error: The path '{dir_path}' is not a valid directory.")
        return

    print(f"Processing all files in directory: {dir_path}")
    
    ingested_count = 0
    failed_count = 0
    
    for file_path in dir_path.iterdir():
        if file_path.is_file():
            try:
                print(f"Ingesting file: {file_path}")
                result = add_documents(file_path, chunk_size=2000)
                print(f"Ingest successful for {file_path}: {result}")
                ingested_count += 1
            except Exception as e:
                print(f"Ingest failed for {file_path}: {e}")
                failed_count += 1

    print(f"\nIngestion summary: {ingested_count} files successfully ingested, {failed_count} files failed.")

def _handle_agent_flow():
    job = WorkerJob(entrypoint=start_agent, jobctx=make_context(), options=Options(

    ))
    job.start()

if __name__ == "__main__":
    # To ingest documents, uncomment the line below and comment out _handle_agent_flow()
    # _handle_ingest_directory_flow()
    
    # To run the agent, comment out the line above and uncomment _handle_agent_flow()
    _handle_agent_flow()
            