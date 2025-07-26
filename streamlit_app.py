import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import difflib

# Configure page
st.set_page_config(
    page_title="RegulatoryMind",
    page_icon="🧠",
    layout="wide"
)

# Theme configuration
def apply_theme(theme_mode):
    """Apply light or dark theme styles"""
    if theme_mode == "Light":
        return """
        <style>
            .stApp {
                background-color: #ffffff;
                color: #000000;
            }
            .main-header {
                color: #1f4e79;
                text-align: center;
                margin-bottom: 2rem;
            }
            .regulation-card {
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #1f4e79;
                margin-bottom: 1rem;
                color: #000000;
            }
            .changed-regulation {
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                color: #000000;
            }
            .compliance-section {
                background-color: #e8f4fd;
                padding: 1.5rem;
                border-radius: 8px;
                margin: 1rem 0;
                color: #000000;
            }
            .diff-added {
                background-color: #d4edda;
                color: #155724;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .diff-removed {
                background-color: #f8d7da;
                color: #721c24;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .stSidebar {
                background-color: #f0f2f6;
            }
            .stTextArea textarea {
                background-color: #ffffff;
                color: #000000;
            }
            .stSelectbox > div > div {
                background-color: #ffffff;
                color: #000000;
            }
            /* Force light theme for main content */
            .stMarkdown, .stText, .stSubheader, .stHeader {
                color: #000000 !important;
            }
        </style>
        """
    else:  # Dark theme
        return """
        <style>
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .main-header {
                color: #4da6ff;
                text-align: center;
                margin-bottom: 2rem;
            }
            .regulation-card {
                background-color: #1e2124;
                padding: 1rem;
                border-radius: 8px;
                border-left: 4px solid #4da6ff;
                margin-bottom: 1rem;
                color: #fafafa;
            }
            .changed-regulation {
                background-color: #2d2a1e;
                border-left: 4px solid #ffc107;
                color: #fafafa;
            }
            .compliance-section {
                background-color: #1a1f2e;
                padding: 1.5rem;
                border-radius: 8px;
                margin: 1rem 0;
                color: #fafafa;
            }
            .diff-added {
                background-color: #1a3d2e;
                color: #5bc27d;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .diff-removed {
                background-color: #3d1a1a;
                color: #ff6b6b;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .stSidebar {
                background-color: #262730;
            }
            .stTextArea textarea {
                background-color: #1e2124;
                color: #fafafa;
            }
            .stSelectbox > div > div {
                background-color: #1e2124;
                color: #fafafa;
            }
            /* Force dark theme for main content */
            .stMarkdown, .stText, .stSubheader, .stHeader {
                color: #fafafa !important;
            }
        </style>
        """

# Initialize theme in session state
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = "Light"  # Default to light mode

# Theme toggle in sidebar
st.sidebar.header("Settings")
theme_mode = st.sidebar.selectbox(
    "Theme Mode",
    ["Light", "Dark"],
    index=0 if st.session_state.theme_mode == "Light" else 1,
    key="theme_selector"
)

# Update session state
st.session_state.theme_mode = theme_mode

# Apply the selected theme
st.markdown(apply_theme(theme_mode), unsafe_allow_html=True)

# Configure Gemini API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Sample regulations data
REGULATIONS_2024 = {
    "engine_checks": [
        {
            "id": "EC-101",
            "title": "Daily Engine Visual Inspection",
            "description": "Visual inspection of engine exterior for damage, leaks, or foreign objects",
            "frequency": "Daily",
            "requirements": [
                "Check for oil leaks around engine casing",
                "Inspect fan blades for damage or foreign object debris",
                "Verify all engine cowling panels are secure",
                "Check for fuel leaks at connections"
            ],
            "documentation": "Log findings in Aircraft Technical Log"
        },
        {
            "id": "EC-205",
            "title": "Engine Oil Level Check",
            "description": "Verification of engine oil quantity and quality",
            "frequency": "Pre-flight",
            "requirements": [
                "Check oil level using dipstick or sight gauge",
                "Oil level must be between minimum and maximum marks",
                "Record oil quantity in technical log",
                "Report any unusual oil consumption"
            ],
            "documentation": "Record in pre-flight inspection checklist"
        },
        {
            "id": "EC-310",
            "title": "Engine Run-up Test",
            "description": "Ground engine operational test to verify performance parameters",
            "frequency": "After maintenance",
            "requirements": [
                "Engine must reach operating temperature within 5 minutes",
                "All engine parameters must be within normal limits",
                "No unusual vibrations or noises",
                "Throttle response must be smooth and immediate"
            ],
            "documentation": "Complete engine run-up form with all parameters recorded"
        }
    ]
}

REGULATIONS_2025 = {
    "engine_checks": [
        {
            "id": "EC-101",
            "title": "Daily Engine Visual Inspection",
            "description": "Visual inspection of engine exterior for damage, leaks, or foreign objects",
            "frequency": "Daily",
            "requirements": [
                "Check for oil leaks around engine casing",
                "Inspect fan blades for damage or foreign object debris",
                "Verify all engine cowling panels are secure",
                "Check for fuel leaks at connections"
            ],
            "documentation": "Log findings in Aircraft Technical Log"
        },
        {
            "id": "EC-205",
            "title": "Engine Oil Level Check",
            "description": "Verification of engine oil quantity and quality",
            "frequency": "Pre-flight",
            "requirements": [
                "Check oil level using dipstick or sight gauge",
                "Oil level must be between minimum and maximum marks",
                "Record oil quantity in technical log",
                "Report any unusual oil consumption",
                "Check oil color and consistency for contamination"
            ],
            "documentation": "Record in pre-flight inspection checklist with digital timestamp"
        },
        {
            "id": "EC-310",
            "title": "Engine Run-up Test",
            "description": "Ground engine operational test to verify performance parameters",
            "frequency": "After maintenance",
            "requirements": [
                "Engine must reach operating temperature within 4 minutes",
                "All engine parameters must be within normal limits",
                "No unusual vibrations or noises",
                "Throttle response must be smooth and immediate",
                "Record ambient temperature and pressure conditions"
            ],
            "documentation": "Complete engine run-up form with all parameters recorded and digitally signed"
        }
    ]
}

def get_regulation_changes():
    """Compare 2024 and 2025 regulations to identify changes"""
    changes = []
    
    for i, (reg_2024, reg_2025) in enumerate(zip(REGULATIONS_2024["engine_checks"], REGULATIONS_2025["engine_checks"])):
        if reg_2024 != reg_2025:
            changes.append({
                "regulation_id": reg_2024["id"],
                "title": reg_2024["title"],
                "changes": {
                    "requirements": {
                        "old": reg_2024["requirements"],
                        "new": reg_2025["requirements"]
                    },
                    "documentation": {
                        "old": reg_2024["documentation"],
                        "new": reg_2025["documentation"]
                    }
                }
            })
    
    return changes

def create_compliance_prompt(regulations, document_content):
    """Create prompt for compliance analysis"""
    return f"""
    You are RegulatoryMind, an AI compliance expert for aviation engine maintenance.
    
    Analyze the uploaded document against these engine check regulations:
    
    {json.dumps(regulations, indent=2)}
    
    Document content to analyze:
    {document_content}
    
    Provide a detailed compliance analysis including:
    1. **Compliance Status**: Overall compliance score (0-100%)
    2. **Compliant Items**: What the document does well
    3. **Non-Compliant Items**: What's missing or incorrect
    4. **Recommendations**: Specific actions to improve compliance
    5. **Risk Assessment**: Potential risks of non-compliance
    
    Format your response in clear markdown with sections and bullet points.
    """

def create_impact_analysis_prompt(changes, document_content):
    """Create prompt for regulatory change impact analysis"""
    return f"""
    You are RegulatoryMind, analyzing the impact of regulatory changes.
    
    Regulatory changes from 2024 to 2025:
    {json.dumps(changes, indent=2)}
    
    Current document content:
    {document_content}
    
    Analyze the impact of these changes on the uploaded document:
    
    1. **Change Summary**: What has changed in the regulations
    2. **Document Impact**: How these changes affect the current document
    3. **Required Updates**: Specific changes needed in the document
    4. **Implementation Timeline**: Suggested timeline for updates
    5. **Training Requirements**: Any additional training needed
    6. **Cost Implications**: Potential costs of implementing changes
    
    Format your response in clear markdown with actionable recommendations.
    """

# Main app
st.markdown("<h1 class='main-header'>🧠 RegulatoryMind</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.1em;'>AI-Powered Engineering Compliance Intelligence</p>", unsafe_allow_html=True)

# Sidebar for regulation selection
st.sidebar.header("Regulation Version")
selected_year = st.sidebar.selectbox("Select Regulation Year", ["2024", "2025"])

regulations = REGULATIONS_2024 if selected_year == "2024" else REGULATIONS_2025

# Display regulations
st.header(f"🔧 Engine Check Regulations ({selected_year})")

for reg in regulations["engine_checks"]:
    # Check if this regulation changed between years
    is_changed = False
    if selected_year == "2025":
        reg_2024 = next((r for r in REGULATIONS_2024["engine_checks"] if r["id"] == reg["id"]), None)
        if reg_2024 and reg_2024 != reg:
            is_changed = True
    
    card_class = "regulation-card changed-regulation" if is_changed else "regulation-card"
    
    st.markdown(f"""
    <div class="{card_class}">
        <h4>{reg['id']}: {reg['title']} {'🔄' if is_changed else ''}</h4>
        <p><strong>Description:</strong> {reg['description']}</p>
        <p><strong>Frequency:</strong> {reg['frequency']}</p>
        <p><strong>Documentation:</strong> {reg['documentation']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander(f"View Requirements - {reg['id']}"):
        for req in reg['requirements']:
            st.write(f"• {req}")

# Document upload section
st.header("📄 Document Analysis")
uploaded_file = st.file_uploader("Upload your engine check document", type=['txt', 'md', 'pdf'])

if uploaded_file is not None:
    # Read file content
    if uploaded_file.type == "text/plain" or uploaded_file.type == "text/markdown":
        document_content = str(uploaded_file.read(), "utf-8")
    else:
        st.warning("PDF support coming soon. Please upload a text file for now.")
        document_content = None
    
    if document_content:
        st.success("Document uploaded successfully!")
        
        # Display document preview
        with st.expander("Document Preview"):
            st.text_area("Content", document_content, height=200, disabled=True)
        
        # Analysis buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Analyze Compliance", type="primary"):
                if "GEMINI_API_KEY" in st.secrets:
                    with st.spinner("Analyzing compliance..."):
                        try:
                            model = genai.GenerativeModel('models/gemini-1.5-flash')
                            prompt = create_compliance_prompt(regulations, document_content)
                            response = model.generate_content(prompt)
                            
                            st.markdown(f"""
                            <div class="compliance-section">
                                <h3>🎯 Compliance Analysis ({selected_year} Regulations)</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(response.text)
                            
                        except Exception as e:
                            st.error(f"Analysis failed: {str(e)}")
                else:
                    st.error("Gemini API key not configured")
        
        with col2:
            if st.button("📊 Analyze Regulatory Changes Impact"):
                if "GEMINI_API_KEY" in st.secrets:
                    changes = get_regulation_changes()
                    if changes:
                        with st.spinner("Analyzing regulatory impact..."):
                            try:
                                model = genai.GenerativeModel('models/gemini-1.5-flash')
                                prompt = create_impact_analysis_prompt(changes, document_content)
                                response = model.generate_content(prompt)
                                
                                st.markdown(f"""
                                <div class="compliance-section">
                                    <h3>📈 Regulatory Change Impact Analysis</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                st.markdown(response.text)
                                
                            except Exception as e:
                                st.error(f"Analysis failed: {str(e)}")
                    else:
                        st.info("No regulatory changes detected between 2024 and 2025")
                else:
                    st.error("Gemini API key not configured")

# Regulatory changes section
st.header("🔄 Regulatory Changes (2024 → 2025)")

changes = get_regulation_changes()
if changes:
    for change in changes:
        st.subheader(f"{change['regulation_id']}: {change['title']}")
        
        # Requirements changes
        if change['changes']['requirements']['old'] != change['changes']['requirements']['new']:
            st.write("**Requirements Changes:**")
            
            old_reqs = change['changes']['requirements']['old']
            new_reqs = change['changes']['requirements']['new']
            
            # Simple diff display
            for i, (old_req, new_req) in enumerate(zip(old_reqs, new_reqs)):
                if old_req != new_req:
                    st.markdown(f"**Requirement {i+1}:**")
                    st.markdown(f"❌ **2024:** {old_req}")
                    st.markdown(f"✅ **2025:** {new_req}")
            
            # Check for added requirements
            if len(new_reqs) > len(old_reqs):
                st.markdown("**New Requirements:**")
                for new_req in new_reqs[len(old_reqs):]:
                    st.markdown(f"🆕 {new_req}")
        
        # Documentation changes
        if change['changes']['documentation']['old'] != change['changes']['documentation']['new']:
            st.write("**Documentation Changes:**")
            st.markdown(f"❌ **2024:** {change['changes']['documentation']['old']}")
            st.markdown(f"✅ **2025:** {change['changes']['documentation']['new']}")
        
        st.markdown("---")
else:
    st.info("No changes detected between 2024 and 2025 regulations")

# Footer
st.markdown("---")
footer_class = "footer-light" if theme_mode == "Light" else "footer-dark"
st.markdown(f"""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>🧠 <strong>RegulatoryMind</strong> - AI-Powered Engineering Compliance Intelligence</p>
    <p>Ensuring regulatory compliance through intelligent automation</p>
</div>
""", unsafe_allow_html=True)