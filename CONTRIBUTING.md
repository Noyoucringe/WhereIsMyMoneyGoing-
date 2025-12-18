# Contributing to Expense Tracker

Thank you for your interest in contributing to the Expense Tracker project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/WhereIsMyMoneyGoing-.git
   cd WhereIsMyMoneyGoing-
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests to ensure everything works:
   ```bash
   PYTHONPATH=. python tests/test_expense_tracker.py
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests:
   ```bash
   PYTHONPATH=. python tests/test_expense_tracker.py
   ```

4. Run the demo to ensure everything works:
   ```bash
   python demo.py
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a Pull Request

## Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Add type hints where appropriate

## Testing

- Write tests for new features
- Ensure all existing tests pass
- Aim for good test coverage
- Test edge cases

Example test structure:
```python
def test_feature_name(self):
    """Test description"""
    # Arrange
    input_data = ...
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    self.assertEqual(result, expected_value)
```

## Adding New Features

### Adding a New Category

To add a new expense category:

1. Edit `expense_tracker/categorizer.py`
2. Add your category to `_initialize_categories()`:
   ```python
   'YourCategory': ExpenseCategory(
       name='YourCategory',
       keywords=['keyword1', 'keyword2', 'keyword3']
   ),
   ```
3. Add tests in `tests/test_expense_tracker.py`

### Adding a New Anomaly Detection Method

To add a new anomaly detection method:

1. Edit `expense_tracker/anomaly_detector.py`
2. Add your method:
   ```python
   def detect_new_method(self, transactions: List[Transaction]) -> List[Transaction]:
       """Your detection logic"""
       anomalies = []
       # Your implementation
       return anomalies
   ```
3. Update `detect_all_anomalies()` to include your method
4. Add tests

### Adding a New Visualization

To add a new visualization:

1. Edit `expense_tracker/visualizer.py`
2. Add your plotting function:
   ```python
   def plot_new_chart(self, transactions: List[Transaction], output_path: str = None):
       """Create new chart"""
       df = self.create_dataframe(transactions)
       # Your visualization code
   ```
3. Add to the dashboard if appropriate

## Documentation

- Update README.md if you add major features
- Add usage examples to USAGE_EXAMPLES.md
- Update docstrings for modified functions
- Add comments for complex logic

## Commit Messages

Use clear, descriptive commit messages:

- Good: "Add support for multi-currency transactions"
- Good: "Fix anomaly detection for edge case with single transaction"
- Bad: "Update code"
- Bad: "Fix bug"

Format:
```
Short summary (50 chars or less)

Detailed explanation if needed. Explain what and why,
not how (the code shows how).

- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"
```

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Update documentation
3. Add tests for new features
4. Ensure all tests pass
5. Update CHANGELOG.md if applicable
6. Request review from maintainers

## Bug Reports

When reporting bugs, include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces
- Minimal code example

## Feature Requests

When requesting features:

- Describe the use case
- Explain why it would be useful
- Provide examples if possible
- Consider implementation approach

## Areas for Contribution

Here are some areas where contributions are especially welcome:

### High Priority
- [ ] Web interface (Flask/Django)
- [ ] REST API
- [ ] Database integration (SQLite, PostgreSQL)
- [ ] Improved OCR accuracy
- [ ] Budget tracking and alerts

### Medium Priority
- [ ] Export to Excel/CSV with formatting
- [ ] Recurring transaction detection
- [ ] Custom rules engine
- [ ] Mobile app integration
- [ ] Bank API integration

### Low Priority
- [ ] Multi-currency support
- [ ] Tax reporting features
- [ ] Receipt image attachment
- [ ] Cloud backup
- [ ] Notification system

## Questions?

If you have questions:
- Open an issue
- Check existing issues
- Review the documentation

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

Thank you for contributing! 🎉
