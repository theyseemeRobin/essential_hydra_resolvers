# Essential Hydra Resolvers
Some resolvers for OmegaConf I find myself reusing, provided as a Hydra plugin.

## Installation

```
pip install git+https://github.com/theyseemerobin/essential_hydra_resolvers.git
```

## Usage
Like any other Omegaconf resolver, you can use these in your config files. After installing the package, you can 
automatically use them when having imported hydra.

For example
```yaml
pi: ${get_attr:math,pi}
```

## Tests
Clone the repo, and install the `dev` dependencies. Then you can run the tests with pytest:
```bash
pip install -e .[dev]
pytest
```

