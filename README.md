# Linear Fox | GenoFusion

[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.11%20%7C%203.10-blue)](https://badge.fury.io/py/genet) 
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

GenoFusion | Enhance your fundamental molecular biology techniques to yield better outcomes.

## Overview
Welcome to Linear Fox GenoFusion, a Python library and app designed to facilitate DNA/RNA sequence analysis & prediction. This platform integrates a suite of bioinformatics tools that cater to researchers and scientists, helping you achieve better results in your molecular biology projects.

## Installation

### Prerequisites
- Python 3.10-3.12 (3.13 not yet supported)
- pip (latest version recommended)
 

### Set up environment
```bash
git clone https://github.com/Linear-Fox-Labs/GenoFusion.git
cd GenoFusion

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows

# Update pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .

# Optional: Install TensorFlow (Platform specific)
# For macOS with Apple Silicon:
pip install tensorflow-macos>=2.15.0
# For other platforms:
pip install tensorflow>=2.15.0
```

## Features
- DNA/RNA sequence analysis
- Sequence visualization
- Built-in bioinformatics tools
- Integration with common biological databases

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support
Contact: support@linearfox.com

## License
Apache License 2.0