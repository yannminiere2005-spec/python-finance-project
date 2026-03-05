from financial_statement import FinancialStatement

statement = FinancialStatement("data/company.csv")
print(FinancialStatement.__dict__.keys())

print(statement.data)
print(statement.years)
print(statement.items)
print(statement.get("Revenue", 2023))
