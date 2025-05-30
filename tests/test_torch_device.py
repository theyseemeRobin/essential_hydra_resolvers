import sys
import types

import omegaconf
import pytest
from omegaconf import OmegaConf
from hydra_plugins.essential_resolvers.resolvers import *


def test_torch_device_not_installed():
    sys.modules.pop("torch", None)
    cfg = OmegaConf.create({"attr": "${torch_device:cuda}"})
    with pytest.raises(
            omegaconf.errors.InterpolationResolutionError,
            match="ImportError raised while resolving interpolation: The 'torch' module is required "
    ):
        _ = cfg.attr


def test_torch_device_cuda_unavailable(monkeypatch):
    # Mock torch and torch.cuda.is_available to return False
    mock_torch = types.SimpleNamespace()
    mock_torch.cuda = types.SimpleNamespace(is_available=lambda: False)
    sys.modules["torch"] = mock_torch

    cfg = OmegaConf.create({"device": "${torch_device:cuda}"})
    assert cfg.device == "cpu"

    # Clean up
    del sys.modules["torch"]


def test_torch_device_cuda_available(monkeypatch):
    # Mock torch and torch.cuda.is_available to return False
    mock_torch = types.SimpleNamespace()
    mock_torch.cuda = types.SimpleNamespace(is_available=lambda: True)
    sys.modules["torch"] = mock_torch

    cfg = OmegaConf.create({"device": "${torch_device:cuda}"})
    assert cfg.device == "cuda"

    # Clean up
    del sys.modules["torch"]


def test_torch_device_invalid_input():
    mock_torch = types.SimpleNamespace()
    mock_torch.cuda = types.SimpleNamespace(is_available=lambda: False)
    sys.modules["torch"] = mock_torch
    cfg = OmegaConf.create({"device": "${torch_device:something}"})
    with pytest.raises(ValueError, match="Invalid device 'something'"):
        _ = cfg.device