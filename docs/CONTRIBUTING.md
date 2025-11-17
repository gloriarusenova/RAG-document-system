# Contributing Guide

Thank you for your interest in contributing to the Simple RAG Pipeline project!

---

## 🎯 Project Goals

This project aims to:
- Provide a **beginner-friendly** introduction to RAG systems
- Demonstrate **best practices** in RAG architecture
- Serve as a **learning resource** for understanding retrieval and generation
- Offer a **modular codebase** that's easy to extend

---

## 🤝 How to Contribute

### Ways to Contribute

1. **Bug Reports** - Report issues you encounter
2. **Feature Requests** - Suggest new features or improvements
3. **Documentation** - Improve or expand documentation
4. **Code** - Submit bug fixes or new features
5. **Examples** - Add new sample documents or test cases

---

## 🐛 Reporting Issues

When reporting bugs, please include:

- **Description** - Clear description of the issue
- **Steps to Reproduce** - How to recreate the problem
- **Expected Behavior** - What should happen
- **Actual Behavior** - What actually happens
- **Environment** - Python version, OS, etc.
- **Error Messages** - Full error output if applicable

**Example:**
```markdown
### Bug: Indexing fails with large PDFs

**Environment:**
- Python 3.13
- macOS 14.5
- 500MB PDF file

**Steps:**
1. Run `python main.py add -p large_file.pdf`
2. Wait for processing

**Expected:** Document indexed successfully
**Actual:** MemoryError after 5 minutes

**Error:**
```
MemoryError: Unable to allocate 2.5 GiB
```
```

---

## 💡 Suggesting Features

When suggesting features:

1. **Check existing issues** - Someone might have already suggested it
2. **Explain the use case** - Why is this feature needed?
3. **Describe the solution** - How should it work?
4. **Consider alternatives** - Are there other ways to achieve this?

---

## 📝 Code Contributions

### Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/simple-rag-pipeline.git
   cd simple-rag-pipeline
   ```
3. **Set up development environment**
   ```bash
   bash scripts/setup_env.sh
   ```
4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Guidelines

#### Code Style

- **PEP 8** - Follow Python style guidelines
- **Type Hints** - Use type hints for function parameters and return values
- **Docstrings** - Document functions, classes, and modules
- **Clear Names** - Use descriptive variable and function names

**Example:**
```python
def retrieve_chunks(
    query: str, 
    top_k: int = 5
) -> List[DocumentChunk]:
    """
    Retrieve the most relevant document chunks for a query.
    
    Args:
        query: User's search query
        top_k: Number of chunks to return
        
    Returns:
        List of DocumentChunk objects sorted by relevance
    """
    # Implementation
    pass
```

#### Testing

- Write tests for new features
- Ensure existing tests pass
- Test edge cases

**Run tests:**
```bash
# TODO: Add test command when tests are implemented
python -m pytest tests/
```

#### Documentation

- Update relevant documentation files
- Add docstrings to new functions/classes
- Include usage examples for new features

### Code Review Process

1. **Submit a Pull Request**
   - Clear title and description
   - Reference related issues
   - Include test results

2. **Address Feedback**
   - Respond to review comments
   - Make requested changes
   - Update your PR

3. **Merge**
   - Once approved, your PR will be merged
   - Your contribution will be acknowledged

---

## 🏗️ Architecture Guidelines

### Extending Components

The system uses interface-based design. To add new functionality:

#### Adding a New Document Type

1. **Implement `BaseIndexer`**
   ```python
   from src.interface.base_indexer import BaseIndexer
   
   class WordDocIndexer(BaseIndexer):
       def index(self, file_path: str) -> List[DocumentChunk]:
           # Your implementation
           pass
   ```

2. **Register in Pipeline**
   ```python
   # In rag_pipeline.py
   if file_path.endswith('.docx'):
       indexer = WordDocIndexer()
   ```

#### Adding a New Vector Database

1. **Implement `BaseDatastore`**
   ```python
   from src.interface.base_datastore import BaseDatastore
   
   class PineconeDatastore(BaseDatastore):
       def search(self, query_vector, top_k):
           # Your implementation
           pass
   ```

2. **Update Configuration**
   ```python
   # In create_pipeline()
   datastore = PineconeDatastore()
   ```

### Design Principles

1. **Single Responsibility** - Each component has one clear purpose
2. **Open/Closed** - Open for extension, closed for modification
3. **Interface Segregation** - Small, focused interfaces
4. **Dependency Injection** - Components receive dependencies, don't create them

---

## 📚 Documentation Contributions

Documentation is as important as code! Help us by:

- **Fixing typos** - Even small fixes matter
- **Clarifying concepts** - Make complex topics easier to understand
- **Adding examples** - Show how to use features
- **Improving structure** - Organize information better

### Documentation Standards

- Use clear, simple language
- Include code examples
- Add diagrams where helpful
- Link to related documentation

---

## 🧪 Adding Test Cases

### Test Question Format

Add evaluation questions to `sample_data/eval/sample_questions.json`:

```json
{
  "question": "What is the main product of AuraTech?",
  "expected_answer": "AuraTech's main product is the Empathy Core...",
  "relevant_doc_ids": [
    "auratechdynamics_history.pdf:1",
    "auratechdynamics_services_2025.pdf:0"
  ]
}
```

### Sample Documents

When adding sample documents:
- Use royalty-free or original content
- Keep files reasonably sized (< 10MB)
- Include a variety of content types

---

## 🚀 Release Process

(For maintainers)

1. **Update Version** - Bump version numbers
2. **Update CHANGELOG** - Document changes
3. **Run Tests** - Ensure everything works
4. **Tag Release** - Create Git tag
5. **Update Documentation** - Reflect new features

---

## ✅ Checklist for Pull Requests

Before submitting a PR:

- [ ] Code follows style guidelines
- [ ] Added/updated type hints
- [ ] Added/updated docstrings
- [ ] Tests pass (when implemented)
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main

---

## 📧 Communication

- **GitHub Issues** - For bugs and features
- **Pull Requests** - For code contributions
- **Discussions** - For questions and ideas

---

## 🙏 Recognition

All contributors will be:
- Listed in release notes
- Acknowledged in documentation
- Appreciated for their contributions!

---

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We want this to be a welcoming community for everyone learning about RAG systems.

---

**Thank you for contributing to Simple RAG Pipeline!** 🚀





