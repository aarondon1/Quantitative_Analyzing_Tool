# streamlit_app.py
import streamlit as st
import pandas as pd
import base64
import os

# Services
from services.data_service import fetch_alpha_vantage, fetch_yahoo_finance

# LLM
from llm.llm_parser import parse_financial_report, generate_llm_summary

# Models
from models.dcf_model import run_dcf
from models.consolidation_model import run_consolidation
from models.budget_model import run_budget
from models.forecasting_model import run_forecasting

# Risk
from risk.risk_manager import run_risk_analysis

# Reports
from reports.report_generator import generate_report

def app():
    st.title("Quant Analysis Tool (4 Models + Risk + LLM Report)")

    # 1) File Upload
    st.subheader("Upload Financial Research Report (PDF or DOCX)")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
    parsed_text = ""
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        if st.button("Parse File"):
            parsed_text = parse_financial_report(uploaded_file, file_type)
            st.success("File parsed successfully!")
            st.write(parsed_text[:500] + "...")  # show snippet

    # 2) Data Ingestion via APIs (Alpha Vantage / Yahoo)
    st.subheader("Fetch Market Data")
    symbol = st.text_input("Enter Symbol (e.g., AAPL)", value="AAPL")
    use_alpha = st.checkbox("Use Alpha Vantage (Daily)", value=False)
    use_yahoo = st.checkbox("Use Yahoo Finance (1y daily)", value=True)

    if st.button("Fetch Data"):
        data_df = pd.DataFrame()
        if use_alpha:
            data_df = fetch_alpha_vantage(symbol, interval="daily", outputsize="compact")
        if use_yahoo:
            data_df = fetch_yahoo_finance(symbol, period="1y", interval="1d")
        
        if not data_df.empty:
            st.success(f"Data fetched for {symbol}: {len(data_df)} rows")
            st.dataframe(data_df.head(10))
        else:
            st.warning("No data returned. Check symbol or API config.")
    
    # 3) Models Section
    st.subheader("Run Financial Models")

    # DCF
    with st.expander("DCF Model"):
        st.write("Enter projected cash flows for DCF:")
        cf_input = st.text_area("Comma-separated CFs", value="1000,1200,1500,2000")
        discount_rate = st.number_input("Discount Rate (decimal)", value=0.1)
        if st.button("Run DCF"):
            cfs = [float(x.strip()) for x in cf_input.split(",")]
            dcf_df, npv = run_dcf(cfs, discount_rate)
            st.write(dcf_df)
            st.write(f"Calculated NPV: {npv}")
            st.session_state["dcf_result"] = (dcf_df.to_string(index=False), npv)

    # Consolidation
    with st.expander("Consolidation Model"):
        st.write("Provide sample subsidiary data (Name, Revenue, Expenses).")
        sample_data = [
            {"Name": "SubA", "Revenue": 2000, "Expenses": 1500},
            {"Name": "SubB", "Revenue": 3000, "Expenses": 1800}
        ]
        if st.button("Run Consolidation"):
            cons_df, cons_summary = run_consolidation(sample_data)
            st.write(cons_df)
            st.write(cons_summary)
            st.session_state["consolidation_result"] = (cons_df.to_string(index=False), cons_summary)

    # Budget
    with st.expander("Budget Model"):
        st.write("Provide budget vs actual data.")
        sample_budget = [
            {"Category": "Marketing", "Budgeted": 1000, "Actual": 950},
            {"Category": "R&D", "Budgeted": 2000, "Actual": 2200}
        ]
        if st.button("Run Budget"):
            budget_df, budget_summary = run_budget(sample_budget)
            st.write(budget_df)
            st.write(budget_summary)
            st.session_state["budget_result"] = (budget_df.to_string(index=False), budget_summary)

    # Forecasting
    with st.expander("Forecasting Model"):
        st.write("Use previously fetched data for forecasting if available.")
        if st.button("Run Forecasting"):
            if 'data_df' in locals() and not data_df.empty and "Date" in data_df.columns and "Close" in data_df.columns:
                forecast_df, forecast_plot = run_forecasting(data_df[["Date", "Close"]])
                if not forecast_df.empty:
                    st.write(forecast_df)
                    st.image(f"data:image/png;base64,{forecast_plot}")
                    st.session_state["forecast_result"] = (forecast_df.to_string(index=False), "Forecast Plot included")
                else:
                    st.warning("Forecasting failed or data unavailable.")
            else:
                st.warning("No valid data to forecast. Fetch data first (Yahoo/Alpha).")

    # 4) Risk Analysis
    st.subheader("Risk Analysis")
    base_val = st.number_input("Base Value for Risk Simulation", value=100.0)
    vol = st.number_input("Volatility (std dev)", value=0.1)
    sims = st.number_input("Simulations", value=1000)
    if st.button("Run Risk Analysis"):
        risk_summary = run_risk_analysis(base_value=base_val, volatility=vol, simulations=sims)
        st.write(risk_summary)
        st.session_state["risk_summary"] = risk_summary

    # 5) Generate Final Report with LLM
    st.subheader("Generate Final Report")
    if st.button("Generate Report"):
        # Gather session data
        dcf_data = ""
        if "dcf_result" in st.session_state:
            dcf_df_str, dcf_npv = st.session_state["dcf_result"]
            dcf_data = f"{dcf_df_str}\nNPV: {dcf_npv}"

        consolidation_data = ""
        if "consolidation_result" in st.session_state:
            cons_df_str, cons_summary = st.session_state["consolidation_result"]
            consolidation_data = f"{cons_df_str}\n{cons_summary}"

        budget_data = ""
        if "budget_result" in st.session_state:
            budget_df_str, budget_summary = st.session_state["budget_result"]
            budget_data = f"{budget_df_str}\n{budget_summary}"

        forecast_data = ""
        if "forecast_result" in st.session_state:
            fc_df_str, fc_plot = st.session_state["forecast_result"]
            forecast_data = f"{fc_df_str}\n{fc_plot}"

        risk_data = st.session_state.get("risk_summary", "No risk analysis run.")

        # Build a dictionary for LLM
        model_outputs = {
            "DCF": dcf_data,
            "Consolidation": consolidation_data,
            "Budget": budget_data,
            "Forecast": forecast_data
        }
        # Convert to string for the LLM
        model_output_str = "\n".join([f"{k}: {v}" for k, v in model_outputs.items()])

        # Generate LLM-based summary
        llm_text = generate_llm_summary(parsed_text, model_output_str, risk_data)
        st.write("LLM Summary:")
        st.write(llm_text)

        # Finally generate PDF
        pdf_path = generate_report(
            llm_summary=llm_text,
            dcf_data=dcf_data,
            consolidation_data=consolidation_data,
            budget_data=budget_data,
            forecast_data=forecast_data,
            risk_analysis=risk_data
        )
        st.success(f"Report generated: {pdf_path}")
        
        # Provide download link
        with open(pdf_path, "rb") as f:
            pdf_contents = f.read()
            b64 = base64.b64encode(pdf_contents).decode()
            download_link = f'<a href="data:application/octet-stream;base64,{b64}" download="final_report.pdf">Download Final Report</a>'
            st.markdown(download_link, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Quant Analysis Tool", layout="wide")
    # Clear session state on each run for simplicity
    if st.sidebar.button("Reset Session"):
        st.session_state.clear()
    app()

if __name__ == "__main__":
    main()
