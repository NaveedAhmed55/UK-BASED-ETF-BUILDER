def get_category_division(risk_level):
    #[equity, commodity, bonds, real estate]
    div_dict = {"very_low": [0.3, 0.15, 0.4, 0.15],
                "low":[0.35, 0.1, 0.45, 0.1],
                "medium":[0.35, 0.15, 0.35, 0.15],
                "high":[0.5, 0.15, 0.2, 0.15],
                "very_high":[0.55, 0.15, 0.15, 0.15]
                }
    return div_dict[risk_level]