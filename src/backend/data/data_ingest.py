"""Module to ingest parquet data into the database."""
import os
import glob
from typing import List, Any, Tuple, Dict
from datetime import datetime
from urllib.parse import urlparse
import pandas as pd
from prisma import Prisma
from prisma.models import Document

from backend.paths import DATA_DIR, ROOT_DIR, MLB_DATA_DIR



def ingest_parquet_data(file_name: str) -> Tuple[Dict[str, Any], List[Document]]:
    """Ingest parquet data into the database.

    Args:
        file_name (str): The name of the parquet file to ingest.

    Returns:
        Tuple[Dict[str, Any], List[Document]]: A tuple containing the metadata and the list of documents ingested.
    """
    # Prisma instance
    db = Prisma()
    db.connect()

    # Read the parquet file
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_parquet(file_path)

    # Get the metadata
    metadata = {
        'file_name': file_name,
        'file_path': file_path,
        'num_rows': df.shape[0],
        'num_columns': df.shape[1],
        'columns': df.columns.tolist(),
        'created_at': datetime.now(),
    }

    # Ingest the data
    documents = []
    for i, row in df.iterrows():
        document = db.document.create(
            {
                'data': row.to_dict(),
                'metadata': metadata,
            }
        )
        documents.append(document)

    db.disconnect()

    return metadata, documents  # type: ignore                                                                  



def get_parquet_files() -> List[str]:
    """Get the list of parquet files in the data directory."""
    pattern = f"{MLB_DATA_DIR}/**/*.parquet"
    return list(glob.iglob(pattern, recursive=True))


