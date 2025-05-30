import pytest
from omegaconf import OmegaConf
import hydra

def test_from_env_existing_variable(monkeypatch):
    with hydra.initialize(config_path=None, version_base='1.2') as config:
        monkeypatch.setenv("MY_TEST_VAR", "test_value")
        cfg = OmegaConf.create({"val": "${from_env:MY_TEST_VAR}"})
        assert cfg.val == "test_value"

def test_from_env_with_default(monkeypatch):
    with hydra.initialize(config_path=None, version_base='1.2') as config:
        monkeypatch.delenv("MY_MISSING_VAR", raising=False)
        cfg = OmegaConf.create({"val": "${from_env:MY_MISSING_VAR,default_value}"})
        assert cfg.val == "default_value"

def test_from_env_missing_without_default(monkeypatch):
    with hydra.initialize(config_path=None, version_base='1.2') as config:
        monkeypatch.delenv("MY_MISSING_VAR", raising=False)
        cfg = OmegaConf.create({"val": "${from_env:MY_MISSING_VAR}"})
        with pytest.raises(ValueError, match="Environment variable 'MY_MISSING_VAR' not found and no default provided."):
            _ = cfg.val