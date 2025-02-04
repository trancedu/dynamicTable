# Financial Products Management System

A Qt-based application for managing financial instruments with real-time attribute editing and dependency tracking. Supports options, swaps, and other derivative products.

## Features

- 📊 Dual-view interface:
  - Product list view (name + price)
  - Detailed attribute editor (name, value, type, default)
- ✏️ In-place editing of financial product attributes
- 🔄 Automatic dependency resolution (e.g., updating price/quantity affects total)
- 🚦 Validation and type conversion system
- ⏱️ Timestamped status messages with success/failure feedback
- 📈 Supports multiple product types:
  - Options (with strike price, expiration, volatility)
  - Swaps (with fixed rate, notional value)

## Installation

### Dependencies
- Qt6 Core & Widgets
- C++20 compatible compiler
- CMake 3.16+

**Ubuntu:**
```bash
sudo apt install qt6-base-dev qt6-tools-dev-tools cmake build-essential
```

## Usage

1. **Main Window**
   - Displays list of financial products
   - Double-click to open detail view

2. **Detail Window**
   - Editable fields (Value column only)
   - Non-editable "Total" field (auto-calculated)
   - Type validation with error feedback
   - Dependency-aware updates

## Project Structure

### Core C++ Components
```
cpp/
├── CMakeLists.txt
├── FinancialProductModel.cpp  # Attribute table model
├── FinancialProductModel.h
├── ProductListModel.cpp        # Product list model
├── ProductListModel.h
├── FinancialProduct.cpp        # Base product class
├── FinancialProduct.h
├── Option.cpp                  # Option derivatives
├── Option.h
├── Swap.cpp                    # Swap contracts
├── Swap.h
└── main.cpp                    # Application entry point
```

### Key Implementation Details
- **Dynamic Attribute System:** Uses Qt meta-object system (Q_PROPERTY) for property management
- **Type Safety:** QMetaType conversions with fallback to defaults
- **Efficient Updates:** Model resetting with beginResetModel/endResetModel
- **Case-Insensitive Checks:** For "Total" field identification

## Building from Source

```bash
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=/path/to/qt6/lib/cmake ..
make
./FinancialProducts
```

## Python Implementation (Alternative)

See `py/` directory for PyQt6 version with:
- Similar functionality in Python 3.10+
- Dataclass-based product definitions
- Signal-based validation system

# Install dependencies
pip install -r requirements.txt

# Run the application
python py/main.py

## License
MIT License - See [LICENSE](LICENSE) for details
