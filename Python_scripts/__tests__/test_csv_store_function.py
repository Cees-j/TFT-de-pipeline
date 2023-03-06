import pytest
from unittest.mock import patch, Mock
import sys
sys.path.append('..')
import requests
from Get_challengers_euw2.Classes_2 import csv_store_function

from unittest.mock import patch, Mock
import pandas as pd
from google.cloud.storage.blob import Blob
from google.cloud.storage.client import Client
from google.cloud.exceptions import NotFound
from google.cloud.storage.blob import _get_encryption_headers
from google.cloud.storage.bucket import Bucket
from google.cloud import storage



def test_csv_store_function_with_successful_upload():
    # Mocking the Google Cloud Storage API to return a successful upload response
    with patch.object(Blob, 'upload_from_string') as mock_upload, \
         patch.object(storage.Client, '__init__', return_value=None), \
         patch.object(storage.Client, 'get_bucket') as mock_get_bucket:
        
        mock_get_bucket.return_value = Mock()
        mock_blob = mock_get_bucket.return_value.blob.return_value
        mock_blob.upload_from_string.return_value = None
        mock_blob.name = 'test.csv'
        
        data = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        file_name = 'test.csv'

        response = csv_store_function(data, file_name)

        assert response == '200, test.csv storage Complete'
        mock_upload.assert_called_once_with(data.to_csv(index=False))