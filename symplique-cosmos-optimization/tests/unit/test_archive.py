import unittest
from unittest.mock import MagicMock, patch
from src.ArchiveFunction import __init__ as archive_function

class TestArchiveFunction(unittest.TestCase):
    
    @patch('src.ArchiveFunction.__init__.CosmosClient')
    @patch('src.ArchiveFunction.__init__.BlobServiceClient')
    def test_archive_process(self, mock_blob, mock_cosmos):
        # Setup mocks
        mock_container = MagicMock()
        mock_container.query_items.return_value = [
            {'id': '1', 'partitionKey': 'cust1', 'createdDate': '2023-01-01', 'isArchived': False, 'data': {}}
        ]
        
        mock_cosmos.return_value.get_database_client.return_value.get_container_client.return_value = mock_container
        
        # Test
        archive_function.main(MagicMock())
        
        # Assertions
        mock_container.upsert_item.assert_called_once()