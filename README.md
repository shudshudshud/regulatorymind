# RegulatoryMind

**AI-Powered Engineering Compliance Intelligence**

RegulatoryMind is an intelligent compliance management system that helps aviation maintenance teams understand regulations, analyze documents for compliance, and track the impact of regulatory changes on existing procedures.

## Features

### Regulation Management
- Multi-year regulation support (2024/2025) with easy switching
- Visual change indicators highlighting updated requirements
- Structured regulation display with expandable requirement details
- Regulation comparison showing differences between versions

### AI-Powered Document Analysis
- Compliance scoring with detailed breakdown (0-100%)
- Gap analysis identifying non-compliant items
- Risk assessment highlighting potential safety/regulatory risks
- Actionable recommendations for improving compliance

### Regulatory Change Impact Analysis
- Change detection automatically identifying regulation updates
- Impact assessment analyzing how changes affect existing documents
- Implementation guidance with suggested timelines and training needs
- Cost implications highlighting financial impact of changes

### Aviation-Specific Focus
- Engine maintenance procedures (daily inspections, oil checks, run-up tests)
- Multi-authority compliance (CAAS, FAA, EASA)
- Industry best practices built into analysis algorithms

## Technology Stack

- Frontend: Streamlit with custom CSS styling
- AI Engine: Google Gemini 1.5 Flash for compliance analysis
- Data Processing: Python with JSON-based regulation storage
- Document Support: Text, Markdown (PDF coming soon)

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/regulatorymind.git
   cd regulatorymind
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API key
   Create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

4. Run the application
   ```bash
   streamlit run streamlit_app.py
   ```

5. Open your browser
   Navigate to `http://localhost:8501`

## Usage

### 1. Select Regulation Version
Use the sidebar to switch between 2024 and 2025 regulations. Changed regulations will be highlighted.

### 2. Review Regulations
Browse the engine check regulations for your selected year. Click on expandable sections to see detailed requirements.

### 3. Upload Document
Upload your maintenance procedure document (`.txt` or `.md` format) for analysis.

### 4. Run Analysis
Choose from two analysis types:
- Analyze Compliance: Compare your document against current regulations
- Analyze Regulatory Changes Impact: Understand how regulation changes affect your document

### 5. Review Results
Get detailed AI-powered insights including:
- Compliance scores and gap analysis
- Specific recommendations for improvement
- Risk assessment and mitigation strategies
- Change impact analysis and implementation guidance

## Sample Regulations

The system includes engine check regulations covering:

### EC-101: Daily Engine Visual Inspection
- Oil leak detection
- Fan blade inspection
- Cowling panel security
- Fuel leak checks

### EC-205: Engine Oil Level Check
- Oil quantity verification
- Quality assessment
- Consumption monitoring
- 2025 Update: Contamination checking and digital timestamps

### EC-310: Engine Run-up Test
- Performance parameter verification
- Temperature and timing requirements
- Throttle response testing
- 2025 Update: Reduced timing requirements and environmental recording

## Regulatory Changes (2024 → 2025)

Key changes include:
- Enhanced oil quality checks with contamination detection
- Digital documentation requirements with timestamps and signatures
- Tightened timing requirements for engine warm-up procedures
- Environmental condition recording for run-up tests

## Architecture

```
User Interface (Streamlit)
├── Regulation display
├── Document upload
└── Analysis results
        │
AI Analysis Engine
├── Gemini integration
├── Compliance scoring
└── Change impact
        │
Data Layer
├── JSON regulations
├── Document parsing
└── Change detection
```

## Future Roadmap

### Phase 1: Enhanced Document Support
- PDF document processing
- Multi-document batch analysis
- Document comparison features

### Phase 2: Advanced AI Features
- Predictive compliance monitoring
- Automated regulation tracking
- Smart recommendations engine

### Phase 3: Enterprise Integration
- API development for external systems
- Multi-authority regulation support
- Real-time regulation updates

### Phase 4: Industry Expansion
- Other engineering domains (mechanical, electrical)
- International regulation standards
- Compliance workflow automation

## Contributing

We welcome contributions! Please see our Contributing Guidelines for details.

### Development Setup
```bash
# Clone and install in development mode
git clone https://github.com/your-username/regulatorymind.git
cd regulatorymind
pip install -e .

# Run tests
python -m pytest tests/

# Run with live reload
streamlit run streamlit_app.py --server.runOnSave true
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

- Documentation: Project Wiki
- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@regulatorymind.ai

## Use Cases

### Aviation Maintenance Organizations
- Ensure compliance with multi-authority regulations
- Streamline document review processes
- Reduce regulatory violation risks

### Engineering Consulting Firms
- Accelerate compliance assessments
- Provide data-driven recommendations
- Track regulatory changes across projects

### Regulatory Affairs Teams
- Monitor regulation changes and impacts
- Automate compliance documentation
- Generate audit-ready compliance reports

## Benefits

- Accuracy: AI-powered analysis reduces human error
- Speed: Instant compliance assessment vs. manual review
- Cost Savings: Reduce compliance consulting costs
- Adaptability: Automatic tracking of regulatory changes
- Insights: Data-driven compliance decision making

## Why RegulatoryMind?

Traditional compliance management is manual, error-prone, and reactive. RegulatoryMind transforms this with:

1. Proactive Intelligence: Know about changes before they impact you
2. AI-Powered Analysis: Leverage machine learning for accurate assessments
3. Industry Focus: Built specifically for aviation engineering compliance
4. Continuous Learning: System improves with every analysis

---

Made with care for the aviation engineering community

*RegulatoryMind - Because compliance shouldn't be complicated*