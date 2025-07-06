
import pandas as pd

class ReportGenerator:
    def generate_report(self, cost_summary, path="report.xlsx"):
        df = pd.DataFrame(cost_summary)
        df.to_excel(path, index=False)
