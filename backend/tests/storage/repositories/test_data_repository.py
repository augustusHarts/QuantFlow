import pytest
import json
from pathlib import Path

from shared.enums.datalayer import DataLayer
from shared.enums.datasource import DataSource
from shared.models.pipeline_model import SaveRequest
from storage.repositories.data_repository import DataRepository


# --------------------------------------------------
# Save
# --------------------------------------------------

class TestSaveToRawLayer:
    """Test saving data to the RAW layer"""

    def test_save_creates_directory_structure(self, repository, save_request_raw):
        """Test that save creates the correct directory structure"""
        repository.save(save_request_raw)

        expected_dir = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
        )

        assert expected_dir.exists()
        assert expected_dir.is_dir()

    def test_save_creates_json_file(self, repository, save_request_raw):
        """Test that save creates a JSON file"""
        repository.save(save_request_raw)

        file_path = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
            / f"{save_request_raw.key}.json"
        )

        assert file_path.exists()
        assert file_path.is_file()

    def test_save_writes_correct_payload(self, repository, save_request_raw):
        """Test that save writes the correct payload to file"""
        repository.save(save_request_raw)

        file_path = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
            / f"{save_request_raw.key}.json"
        )

        with open(file_path, "r") as f:
            saved_data = json.load(f)

        assert saved_data == save_request_raw.payload

    def test_save_with_complex_payload(self, repository, complex_payload):
        """Test saving complex nested data"""
        request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="BTC-USD",
            payload=complex_payload
        )

        repository.save(request)

        file_path = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
            / "BTC-USD.json"
        )

        with open(file_path, "r") as f:
            saved_data = json.load(f)

        assert saved_data == complex_payload


class TestSaveToProcessedLayer:
    """Test saving data to the PROCESSED layer"""

    def test_save_to_processed_layer(self, repository, save_request_processed):
        """Test saving to PROCESSED layer"""
        repository.save(save_request_processed)

        file_path = (
            repository.root_dir
            / DataLayer.PROCESSED.value
            / DataSource.YAHOO.value
            / f"{save_request_processed.key}.json"
        )

        assert file_path.exists()

    def test_save_overwrites_existing_file(self, repository, save_request_raw):
        """Test that save overwrites existing files"""
        repository.save(save_request_raw)

        updated_request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="AAPL",
            payload={"symbol": "AAPL", "price": 200.00}
        )

        repository.save(updated_request)

        file_path = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
            / "AAPL.json"
        )

        with open(file_path, "r") as f:
            saved_data = json.load(f)

        assert saved_data["price"] == 200.00


class TestSaveEdgeCases:
    """Test edge cases for save method"""

    def test_save_multiple_files_same_provider(self, repository):
        """Test saving multiple files to same provider"""
        for symbol in ["AAPL", "MSFT", "GOOGL"]:
            request = SaveRequest(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO,
                key=symbol,
                payload={"symbol": symbol, "price": 100}
            )
            repository.save(request)

        provider_dir = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
        )

        files = list(provider_dir.glob("*.json"))

        assert len(files) == 3

    def test_save_with_special_characters_in_key(self, repository):
        """Test saving with special characters in key"""
        request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="BTC-USD",
            payload={"symbol": "BTC-USD", "price": 50000}
        )

        repository.save(request)

        file_path = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
            / "BTC-USD.json"
        )

        assert file_path.exists()

    def test_save_empty_payload(self, repository):
        """Test saving empty payload"""
        request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="EMPTY",
            payload={}
        )

        repository.save(request)

        file_path = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
            / "EMPTY.json"
        )

        with open(file_path, "r") as f:
            saved_data = json.load(f)

        assert saved_data == {}


# --------------------------------------------------
# Load
# --------------------------------------------------

class TestLoadFromRawLayer:
    """Test loading data from the RAW layer"""

    def test_load_returns_correct_data(self, repository, save_request_raw):
        """Test that load returns the correct data"""
        repository.save(save_request_raw)

        loaded_data = repository.load(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="AAPL"
        )

        assert loaded_data == save_request_raw.payload

    def test_load_complex_payload(self, repository, complex_payload):
        """Test loading complex nested data"""
        request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="BTC-USD",
            payload=complex_payload
        )

        repository.save(request)

        loaded_data = repository.load(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="BTC-USD"
        )

        assert loaded_data == complex_payload


class TestLoadFromProcessedLayer:
    """Test loading data from the PROCESSED layer"""

    def test_load_from_processed_layer(self, repository, save_request_processed):
        """Test loading from PROCESSED layer"""
        repository.save(save_request_processed)

        loaded_data = repository.load(
            layer=DataLayer.PROCESSED,
            provider=DataSource.YAHOO,
            key="MSFT"
        )

        assert loaded_data == save_request_processed.payload


class TestLoadEdgeCases:
    """Test edge cases for load method"""

    def test_load_nonexistent_file_raises_error(self, repository):
        """Test that loading nonexistent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            repository.load(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO,
                key="NONEXISTENT"
            )

    def test_load_from_nonexistent_layer_raises_error(self, repository):
        """Test that loading from nonexistent layer raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            repository.load(
                layer=DataLayer.CURATED,
                provider=DataSource.YAHOO,
                key="ANY"
            )


# --------------------------------------------------
# Exists
# --------------------------------------------------

class TestExists:
    """Test checking if files exist"""

    def test_exists_returns_true_for_existing_file(self, repository, save_request_raw):
        """Test that exists returns True for existing file"""
        repository.save(save_request_raw)

        exists = repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        )

        assert exists is True

    def test_exists_returns_false_for_nonexistent_file(self, repository):
        """Test that exists returns False for nonexistent file"""
        exists = repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="NONEXISTENT"
        )

        assert exists is False

    def test_exists_for_different_layers(self, repository):
        """Test exists across different layers"""
        request_raw = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="AAPL",
            payload={"symbol": "AAPL"}
        )

        repository.save(request_raw)

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is True

        assert repository.exists(
            layer=DataLayer.PROCESSED,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is False


# --------------------------------------------------
# Delete
# --------------------------------------------------

class TestDelete:
    """Test deleting files"""

    def test_delete_removes_file(self, repository, save_request_raw):
        """Test that delete removes the file"""
        repository.save(save_request_raw)

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is True

        repository.delete(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        )

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is False

    def test_delete_nonexistent_file_does_not_raise_error(self, repository):
        """Test that deleting nonexistent file doesn't raise error"""
        repository.delete(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="NONEXISTENT"
        )

    def test_delete_does_not_affect_other_files(self, repository):
        """Test that delete doesn't affect other files"""
        for symbol in ["AAPL", "MSFT"]:
            request = SaveRequest(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO,
                key=symbol,
                payload={"symbol": symbol}
            )
            repository.save(request)

        repository.delete(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        )

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is False

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="MSFT"
        ) is True


# --------------------------------------------------
# List Providers
# --------------------------------------------------

class TestListProviders:
    """Test listing providers in a layer"""

    def test_list_providers_empty_layer(self, repository):
        """Test listing providers from empty layer returns empty list"""
        providers = repository.list_providers(DataLayer.RAW)

        assert providers == []

    def test_list_providers_single_provider(self, repository, save_request_raw):
        """Test listing providers with single provider"""
        repository.save(save_request_raw)

        providers = repository.list_providers(DataLayer.RAW)

        assert len(providers) == 1
        assert DataSource.YAHOO in providers

    def test_list_providers_ignores_non_directories(self, repository, save_request_raw):
        """Test that list_providers ignores non-directory items"""
        repository.save(save_request_raw)

        # Create a file directly in the layer directory
        layer_dir = repository.root_dir / DataLayer.RAW.value
        (layer_dir / "somefile.txt").touch()

        providers = repository.list_providers(DataLayer.RAW)

        assert len(providers) == 1
        assert DataSource.YAHOO in providers

    def test_list_providers_handles_invalid_provider_names(self, repository, save_request_raw):
        """Test that list_providers handles invalid provider names gracefully"""
        repository.save(save_request_raw)

        # Create a directory with invalid provider name
        layer_dir = repository.root_dir / DataLayer.RAW.value
        (layer_dir / "invalid_provider").mkdir(parents=True, exist_ok=True)

        providers = repository.list_providers(DataLayer.RAW)

        # Should only return valid DataSource enums
        assert len(providers) == 1
        assert DataSource.YAHOO in providers


class TestListProvidersMultipleProviders:
    """Test listing multiple providers"""

    def test_list_providers_multiple_providers(self, repository):
        """Test listing multiple providers"""
        # Create multiple providers manually
        layer_dir = repository.root_dir / DataLayer.RAW.value

        for provider in [DataSource.YAHOO]:
            provider_dir = layer_dir / provider.value
            provider_dir.mkdir(parents=True, exist_ok=True)
            (provider_dir / "test.json").touch()

        providers = repository.list_providers(DataLayer.RAW)

        assert len(providers) >= 1
        assert DataSource.YAHOO in providers


# --------------------------------------------------
# List Keys
# --------------------------------------------------

class TestListKeys:
    """Test listing keys for providers"""

    def test_list_keys_empty_providers(self, repository):
        """Test listing keys with empty providers list"""
        keys = repository.list_keys(DataLayer.RAW, [])

        assert keys == {}

    def test_list_keys_single_provider_single_key(self, repository, save_request_raw):
        """Test listing keys for single provider with single key"""
        repository.save(save_request_raw)

        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        assert DataSource.YAHOO in keys
        assert "AAPL" in keys[DataSource.YAHOO]
        assert len(keys[DataSource.YAHOO]) == 1

    def test_list_keys_single_provider_multiple_keys(self, repository):
        """Test listing keys for single provider with multiple keys"""
        symbols = ["AAPL", "MSFT", "GOOGL"]

        for symbol in symbols:
            request = SaveRequest(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO,
                key=symbol,
                payload={"symbol": symbol}
            )
            repository.save(request)

        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        assert len(keys[DataSource.YAHOO]) == 3
        assert set(keys[DataSource.YAHOO]) == set(symbols)

    def test_list_keys_ignores_non_json_files(self, repository, save_request_raw):
        """Test that list_keys ignores non-JSON files"""
        repository.save(save_request_raw)

        provider_dir = (
            repository.root_dir
            / DataLayer.RAW.value
            / DataSource.YAHOO.value
        )

        # Create non-JSON files
        (provider_dir / "README.txt").touch()
        (provider_dir / "data.csv").touch()

        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        assert len(keys[DataSource.YAHOO]) == 1
        assert "AAPL" in keys[DataSource.YAHOO]

    def test_list_keys_nonexistent_provider_directory(self, repository):
        """Test listing keys for nonexistent provider directory"""
        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        assert keys == {}

    def test_list_keys_extracts_file_stem_correctly(self, repository):
        """Test that list_keys correctly extracts filename without extension"""
        request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="BTC-USD",
            payload={"symbol": "BTC-USD"}
        )

        repository.save(request)

        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        assert "BTC-USD" in keys[DataSource.YAHOO]


# --------------------------------------------------
# Integration Tests
# --------------------------------------------------

class TestRepositoryIntegration:
    """Integration tests for repository operations"""

    def test_save_load_cycle(self, repository, complex_payload):
        """Test complete save and load cycle"""
        request = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="TEST",
            payload=complex_payload
        )

        repository.save(request)
        loaded = repository.load(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="TEST"
        )

        assert loaded == complex_payload

    def test_save_delete_cycle(self, repository, save_request_raw):
        """Test save and delete cycle"""
        repository.save(save_request_raw)

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is True

        repository.delete(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        )

        assert repository.exists(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO.value,
            key="AAPL"
        ) is False

    def test_workflow_save_list_load_delete(self, repository):
        """Test complete workflow: save, list, load, delete"""
        symbols = ["AAPL", "MSFT"]

        for symbol in symbols:
            request = SaveRequest(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO,
                key=symbol,
                payload={"symbol": symbol, "price": 100}
            )
            repository.save(request)

        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        assert set(keys[DataSource.YAHOO]) == set(symbols)

        for symbol in symbols:
            loaded = repository.load(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO,
                key=symbol
            )

            assert loaded["symbol"] == symbol

            repository.delete(
                layer=DataLayer.RAW,
                provider=DataSource.YAHOO.value,
                key=symbol
            )

        keys = repository.list_keys(
            DataLayer.RAW,
            [DataSource.YAHOO]
        )

        # After deleting all files, the provider directory still exists but has no keys
        assert keys[DataSource.YAHOO] == []

    def test_multiple_layers_isolation(self, repository):
        """Test that different layers are isolated from each other"""
        request_raw = SaveRequest(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="AAPL",
            payload={"symbol": "AAPL", "source": "raw"}
        )

        request_processed = SaveRequest(
            layer=DataLayer.PROCESSED,
            provider=DataSource.YAHOO,
            key="AAPL",
            payload={"symbol": "AAPL", "source": "processed"}
        )

        repository.save(request_raw)
        repository.save(request_processed)

        raw_data = repository.load(
            layer=DataLayer.RAW,
            provider=DataSource.YAHOO,
            key="AAPL"
        )

        processed_data = repository.load(
            layer=DataLayer.PROCESSED,
            provider=DataSource.YAHOO,
            key="AAPL"
        )

        assert raw_data["source"] == "raw"
        assert processed_data["source"] == "processed"
