import pytest
from omegaconf import OmegaConf
import omegaconf
from hydra_plugins.essential_resolvers.resolvers import *

def test_get_attr_existing_attribute():
    cfg = OmegaConf.create({"attr": "${get_attr:math,pi}"})
    assert abs(cfg.attr - 3.14159) < 1e-5

def test_get_attr_nonexistent_attribute():
    cfg = OmegaConf.create({"attr": "${get_attr:math,nonexistent_attr}"})
    with pytest.raises(ValueError, match="Package 'math' does not have attribute 'nonexistent_attr'."):
        _ = cfg.attr

def test_get_attr_nonexistent_module():
    cfg = OmegaConf.create({"attr": "${get_attr:nonexistent_module,attr}"})
    with pytest.raises(omegaconf.errors.InterpolationResolutionError, match="ModuleNotFoundError raised while resolving interpolation:"):
        _ = cfg.attr
