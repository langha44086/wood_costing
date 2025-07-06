
class VarianceAnalyzer:
    def analyze(self, actual_cost, standard_cost):
        diff = actual_cost - standard_cost
        percent = (diff / standard_cost) * 100 if standard_cost else 0
        return {"difference": diff, "percent": percent}
