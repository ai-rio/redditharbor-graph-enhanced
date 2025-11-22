# RedditHarbor Graph Enhanced 🚀

**RedditHarbor with Deep-Graph-MCP integration - AI-powered code analysis, dependency mapping, and intelligent refactoring for Reddit data collection pipelines.**

<div align="center">

![RedditHarbor Logo](https://img.shields.io/badge/RedditHarbor-Graph%20Enhanced-FF6B35?style=for-the-badge&logo=reddit)
![Deep-Graph-MCP](https://img.shields.io/badge/Deep-Graph-MCP-AI%20Powered-004E89?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-004E89?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Research%20Ready-F7B801?style=for-the-badge)

</div>

---

## 🎯 Overview

RedditHarbor Graph Enhanced is an experimental fork of RedditHarbor that integrates **Deep-Graph-MCP** for intelligent code analysis, dependency mapping, and automated refactoring. This version transforms the Reddit data collection pipeline into a self-analyzing, self-optimizing system that can understand its own architecture and suggest improvements.

### 🧠 Deep-Graph-MCP Integration

This enhanced version includes:
- **🔍 Semantic Code Analysis** - AI-powered understanding of code relationships and functionality
- **🗺️ Dependency Mapping** - Automated visualization of module interdependencies
- **⚡ Intelligent Refactoring** - AI-suggested code improvements with impact analysis
- **📊 Architecture Insights** - Real-time analysis of pipeline performance and structure
- **🤖 Knowledge Graph** - Living documentation that evolves with codebase changes

### 🚀 Original RedditHarbor Features

- **Comprehensive Reddit Data Collection** with DLT activity validation
- **Multi-factor Activity Scoring** for quality-focused collection
- **AI-agent Ready Architecture** for automated workflows
- **Production-ready Pipeline** with comprehensive error handling
- **Advanced Research Templates** for monetizable app research

---

## 🏗️ Architecture Enhancement

### Original Architecture
```
core/
├── collection.py          # Reddit API data collection
├── deduplication/         # Advanced deduplication logic
├ enrichment/             # Market validation & analysis
├ pipeline/               # Data flow orchestration
├ agents/                 # AI agent systems
└── storage/               # Hybrid storage solutions
```

### Enhanced Architecture with Deep-Graph-MCP
```
core/
├── collection.py          # Enhanced with graph analysis
├── graph_integration/     # NEW: Deep-Graph-MCP tools
│   ├── analyzer.py       # AI-powered code analysis
│   ├── dependencies.py   # Dependency mapping
│   └── refactoring.py    # Intelligent refactoring
├── deduplication/         # Graph-optimized deduplication
├ enrichment/             # Enhanced with semantic search
├ pipeline/               # Graph-aware orchestration
├ agents/                 # Graph-coordinated agents
└── storage/               # Dependency-optimized storage
```

---

## 🚀 Quick Start

### Prerequisites

1. **Deep-Graph-MCP Setup**
   ```bash
   # Create your DeepGraph project
   Visit: https://deepgraph.co/projects/redditharbor-graph-enhanced
   ```

2. **Python Environment**
   ```bash
   # Clone this repository
   git clone https://github.com/ai-rio/redditharbor-graph-enhanced.git
   cd redditharbor-graph-enhanced

   # Install dependencies
   uv sync
   ```

3. **Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   # Edit .env with your Reddit API credentials
   ```

### Graph-Enhanced Development

1. **Analyze Code Dependencies**
   ```python
   from core.graph_integration.analyzer import RedditHarborGraphAnalyzer

   analyzer = RedditHarborGraphAnalyzer()
   dependencies = analyzer.analyze_module_dependencies("core/collection")
   print(dependencies)
   ```

2. **Get Refactoring Suggestions**
   ```python
   suggestions = analyzer.find_refactoring_opportunities()
   for suggestion in suggestions:
       print(f"Module: {suggestion['file']}")
       print(f"Issue: {suggestion['complexity']}")
       print(f"Solution: {suggestion['suggestions']}")
   ```

3. **Trace Data Flow**
   ```python
   data_flow = analyzer.trace_data_flow("submission_data")
   print(f"Pipeline stages: {data_flow['stages']}")
   print(f"Bottlenecks: {data_flow['bottlenecks']}")
   ```

---

## 🔧 Configuration

### Deep-Graph-MCP Configuration

```python
# config/graph_settings.py
GRAPH_CONFIG = {
    "deepgraph_project": "redditharbor-graph-enhanced",
    "auto_analysis": True,
    "refactoring_threshold": 0.8,
    "dependency_depth": 5,
    "semantic_search_enabled": True
}
```

### Environment Variables

```bash
# Deep-Graph-MCP
DEEP_GRAPH_PROJECT_ID=your_project_id
DEEP_GRAPH_API_KEY=your_api_key

# Original RedditHarbor settings
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

## 📊 Research Capabilities

### Graph-Enhanced Analysis

1. **Architecture Impact Analysis**
   - Predict impact of changes before implementation
   - Identify critical path dependencies
   - Visualize data flow bottlenecks

2. **Automated Refactoring**
   - AI-suggested code improvements
   - Automated dependency updates
   - Risk assessment for changes

3. **Performance Optimization**
   - Identify slow pipeline stages
   - Suggest architectural improvements
   - Optimize data flow patterns

### Original Research Features

- **Monetizable App Research** with market validation
- **Activity-Based Collection** with quality scoring
- **Multi-Dimensional Scoring** for opportunity assessment
- **Comprehensive Analytics** with automated reporting

---

## 🛠️ Development

### Graph-Enhanced Workflow

1. **Code Analysis**
   ```bash
   # Analyze entire codebase
   python -m core.graph_integration.analyzer --analyze-all

   # Find refactoring opportunities
   python -m core.graph_integration.analyzer --find-opportunities
   ```

2. **Dependency Mapping**
   ```bash
   # Generate dependency graph
   python -m core.graph_integration.dependencies --generate-graph

   # Check impact of changes
   python -m core.graph_integration.dependencies --impact-analysis
   ```

3. **Intelligent Testing**
   ```bash
   # Run graph-aware tests
   python -m tests.graph_integration --validate-dependencies
   ```

### Code Quality

```bash
# Run all quality checks
./lint.sh

# Run graph-enhanced analysis
python -m core.graph_integration.quality_check
```

---

## 📚 Documentation

- **[Architecture Guide](docs/architecture/)** - System design and graph integration
- **[API Reference](docs/api/)** - Complete API documentation
- **[Graph Analysis Guide](docs/graph-integration/)** - Deep-Graph-MCP usage
- **[Development Guide](docs/development/)** - Contributing guidelines
- **[Original Features](docs/original-features/)** - RedditHarbor functionality

---

## 🔒 Security

- **PII Anonymization** for Reddit user data
- **Secure API Key Management** with environment variables
- **Graph Data Privacy** - local analysis, secure cloud storage
- **Access Control** for Deep-Graph-MCP features

---

## 🤝 Contributing

This is a research-focused experimental version. Contributions welcome for:

- **Graph Analysis Algorithms** - Improve dependency detection
- **Refactoring Logic** - Enhance AI suggestions
- **Performance Optimization** - Better graph analysis speed
- **Documentation** - Improve guides and examples

---

## 📈 Status

**Current Version**: v0.4-graph-enhanced
**Status**: Research & Development
**Deep-Graph-MCP**: ✅ Integrated
**Original Features**: ✅ Maintained

### Roadmap

- [ ] **Graph-Based Testing** - Automatic test generation from code analysis
- [ ] **Real-time Refactoring** - Live code improvement suggestions
- [ ] **Visual Graph Interface** - Interactive dependency visualization
- [ ] **Performance Prediction** - AI-based performance impact analysis

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **RedditHarbor** - Original platform architecture
- **Deep-Graph-MCP** - AI-powered code analysis tools
- **Open Source Community** - Tools and libraries that make this possible

<div align="center">

**⭐ Star this repo to support the research!**

Made with ❤️ for AI-enhanced development

</div>