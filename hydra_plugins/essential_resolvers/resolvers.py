import importlib
import logging
import os

import dotenv
from omegaconf import OmegaConf


def register_resolver(
    name: str,
    **kwargs
):
    def decorator(resolver_func):
        OmegaConf.register_new_resolver(name, resolver_func, **kwargs)
        return resolver_func

    return decorator


@register_resolver("from_env")
def from_env_resolver(env_var: str, default: str = None) -> str:
    """
    Custom OmegaConf resolver to get environment variables from a .env file or the system environment.
    """
    logging.info(f"Opening .env file to get variable '{env_var}'")
    dotenv.load_dotenv()
    value = os.getenv(env_var)
    if value is None:
        if default is not None:
            logging.warning(f"Environment variable '{env_var}' not found, using default value: '{default}'")
            return default
        else:
            raise ValueError(f"Environment variable '{env_var}' not found and no default provided.")
    return value


@register_resolver("torch_device")
def get_device_resolver(device: str):
    """
    Custom OmegaConf resolver to validate the torch device.
    """
    try:
        import torch
    except ImportError:
        raise ImportError("The 'torch' module is required for the 'torch_device' resolver. Please install PyTorch.")
    if device == "cuda":
        if not torch.cuda.is_available():
            logging.warning("CUDA is not available. Defaulting to CPU.")
            return "cpu"
        return "cuda"
    elif device == "cpu":
        return "cpu"
    else:
        raise ValueError(f"Invalid device '{device}'. Must be 'cuda' or 'cpu'.")


@register_resolver("get_attr")
def get_attr_resolver(package_name, attr_name):
    """
    Custom OmegaConf resolver to get an attribute from a package (e.g. bfloat16 from torch).
    """
    package = importlib.import_module(package_name)
    if not hasattr(package, attr_name):
        raise ValueError(f"Package '{package_name}' does not have attribute '{attr_name}'.")
    attr = getattr(package, attr_name)
    return attr