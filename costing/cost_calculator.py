
class CostCalculator:
    def __init__(self, bom_df, materials_prices, labor_costs):
        self.bom = bom_df
        self.materials = materials_prices
        self.labor = labor_costs

    def calculate_cost(self, product_id):
        product_bom = self.bom[self.bom['product_id'] == product_id]
        material_cost = sum(
            row['quantity'] * self.materials.get(row['material'], 0)
            for _, row in product_bom.iterrows()
        )
        labor_cost = self.labor.get(product_id, 0)
        return material_cost + labor_cost
