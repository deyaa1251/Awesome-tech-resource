[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "llmobs-cli"
version = "0.1.0"
description = "CLI tool for managing LLMObs platform"
authors = [{name = "LLMObs Team"}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "click>=8.1.0",
    "docker>=6.1.0",
    "requests>=2.31.0",
    "rich>=13.7.0",
    "pyyaml>=6.0.0",
]

[project.scripts]
llmobs = "cli.main:cli"

[tool.setuptools]
packages = ["cli", "cli.commands", "cli.utils"]
