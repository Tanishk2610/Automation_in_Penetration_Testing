import streamlit as st
from agents.agent import CyberSecurityAgent

def main():
    st.title("Agentic Cybersecurity Workflow")
    st.write("Enter a high-level instruction, for example:")
    st.code('"Scan the kaggle.com using Nmap and visualize it using Zenmap"')
    
    instruction = st.text_input("Security Task Instruction")
    scope = st.text_input("Target Scope (e.g., kaggle.com or 192.168.1.0/24)")
    
    if st.button("Run Scan"):
        if instruction and scope:
            st.info("Executing tasks – please wait...")
            agent = CyberSecurityAgent(scope)
            report = agent.run(instruction)
            st.subheader("Final Report")
            st.text_area("Audit Report", report, height=300)
        else:
            st.error("Please enter both an instruction and a target scope.")

if __name__ == "__main__":
    main()