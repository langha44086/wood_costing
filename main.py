import streamlit as st
import pandas as pd
import os
from costing.cost_calculator import CostCalculator
from costing.variance_analyzer import VarianceAnalyzer
from reports.report_generator import ReportGenerator

DATA_DIR = "data"

# Đọc dữ liệu từ CSV (không dùng cache)
def load_dataframes():
    bom = pd.read_csv(f"{DATA_DIR}/bom.csv")
    materials_prices_df = pd.read_csv(f"{DATA_DIR}/materials_prices.csv")
    labor_costs_df = pd.read_csv(f"{DATA_DIR}/labor_costs.csv")
    actual_costs_df = pd.read_csv(f"{DATA_DIR}/actual_costs.csv")
    return bom, materials_prices_df, labor_costs_df, actual_costs_df

# Ghi thêm dòng dữ liệu vào file CSV
def append_to_csv(file_path, row_dict):
    df = pd.read_csv(file_path)
    df = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
    df.to_csv(file_path, index=False)

st.set_page_config(page_title="Wood Costing System", layout="wide")
st.title("📈 Hệ thống tính giá thành sản phẩm gỗ và nội thất")

# Load dữ liệu mới mỗi lần chạy
bom_df, materials_df, labor_df, actual_df = load_dataframes()

# Tạo dict để tính toán
material_prices = materials_df.set_index("material")["price"].to_dict()
labor_costs = labor_df.set_index("product_id")["labor_cost"].to_dict()
actual_costs = actual_df.set_index("product_id")["actual_cost"].to_dict()
products = bom_df["product_id"].unique()

selected_product = st.selectbox("Chọn mã sản phẩm:", products)

# Tính giá thành
calculator = CostCalculator(bom_df, material_prices, labor_costs)
standard_cost = calculator.calculate_cost(selected_product)
actual_cost = actual_costs.get(selected_product, 0)

# Phân tích chênh lệch
analyzer = VarianceAnalyzer()
variance = analyzer.analyze(actual_cost, standard_cost)

st.subheader("📃 Kết quả tính giá thành")
st.metric("Chi phí chuẩn", f"{standard_cost:,.0f} VND")
st.metric("Chi phí thực tế", f"{actual_cost:,.0f} VND")
st.metric("Chênh lệch", f"{variance['difference']:,.0f} VND ({variance['percent']:.2f}%)")

if st.button("💾 Xuất báo cáo Excel"):
    report = [{
        "product_id": selected_product,
        "standard_cost": standard_cost,
        "actual_cost": actual_cost,
        "difference": variance['difference'],
        "percent_diff": variance['percent']
    }]
    ReportGenerator().generate_report(report)
    st.success("Đã xuất báo cáo report.xlsx")

st.markdown("---")
st.header("📋 Quản lý dữ liệu chi phí")

with st.expander("📊 Xem dữ liệu hiện tại"):
    tab1, tab2, tab3, tab4 = st.tabs(["BOM", "Nguyên vật liệu", "Nhân công", "Chi phí thực tế"])
    with tab1:
        st.dataframe(bom_df, use_container_width=True)
    with tab2:
        st.dataframe(materials_df, use_container_width=True)
    with tab3:
        st.dataframe(labor_df, use_container_width=True)
    with tab4:
        st.dataframe(actual_df, use_container_width=True)

st.markdown("---")
st.header("🆕 Thêm dữ liệu mới")

# === Thêm BOM ===
with st.expander("➕ Thêm định mức nguyên vật liệu"):
    with st.form("add_bom"):
        bom_pid = st.text_input("Mã sản phẩm")
        bom_material = st.text_input("Tên nguyên vật liệu")
        bom_qty = st.number_input("Số lượng", min_value=0.0, step=0.1)
        if st.form_submit_button("Thêm vào BOM"):
            append_to_csv(f"{DATA_DIR}/bom.csv", {
                "product_id": bom_pid, "material": bom_material, "quantity": bom_qty
            })
            st.success("✅ Đã thêm định mức mới! Vui lòng tải lại trang để xem cập nhật.")

# === Thêm giá nguyên vật liệu ===
with st.expander("➕ Thêm giá nguyên vật liệu"):
    with st.form("add_material_price"):
        mat_name = st.text_input("Tên nguyên vật liệu")
        mat_price = st.number_input("Giá (VND)", min_value=0)
        if st.form_submit_button("Thêm giá"):
            append_to_csv(f"{DATA_DIR}/materials_prices.csv", {
                "material": mat_name, "price": mat_price
            })
            st.success("✅ Đã thêm giá nguyên vật liệu! Vui lòng tải lại trang để xem cập nhật.")

# === Thêm chi phí nhân công ===
with st.expander("➕ Thêm chi phí nhân công"):
    with st.form("add_labor_cost"):
        labor_pid = st.text_input("Mã sản phẩm")
        labor_cost = st.number_input("Chi phí nhân công (VND)", min_value=0)
        if st.form_submit_button("Thêm chi phí nhân công"):
            append_to_csv(f"{DATA_DIR}/labor_costs.csv", {
                "product_id": labor_pid, "labor_cost": labor_cost
            })
            st.success("✅ Đã thêm chi phí nhân công! Vui lòng tải lại trang để xem cập nhật.")

# === Thêm chi phí thực tế ===
with st.expander("➕ Thêm chi phí thực tế"):
    with st.form("add_actual_cost"):
        act_pid = st.text_input("Mã sản phẩm")
        act_cost = st.number_input("Chi phí thực tế (VND)", min_value=0)
        if st.form_submit_button("Thêm chi phí thực tế"):
            append_to_csv(f"{DATA_DIR}/actual_costs.csv", {
                "product_id": act_pid, "actual_cost": act_cost
            })
            st.success("✅ Đã thêm chi phí thực tế! Vui lòng tải lại trang để xem cập nhật.")
