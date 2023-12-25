from django.shortcuts import render
from django.http import HttpResponse
from . import portfolio_builder as pb
from portfolioApp.modules.get_category_division import get_category_division
risk_dict = {
    'very_low': 0.05,
    'low': 0.1,
    'medium': 0.2,
    'high': 0.4,
    'very_high': 0.5
}
# Create your views here.

def home(request):
    return render(request, 'index.html')
def input(request):
    return render(request, 'input.html')

def output(request):
    
    if request.method == 'POST':
        years = float(request.POST.get('years'))
        amount = float(request.POST.get('amount'))
        risk_level = request.POST.get('risk_level')
        print(years, amount, risk_level)
        result = pb.getOptPortfolio(amount, years, risk_dict[risk_level], get_category_division(risk_level))
        # result = {'list': [('S', '2', '3', '5', '6', '5', 'la')], 'one_week_return': '-5.369246080776757%', 'one_month_return': '-22.978104186577998%', 'one_year_return': '-9.828501909369935%', 'five_year_return': '100.707018572929%', 'divident_amount': 528.680544595186, 'total_spent': 972.0236542669584, 'divident_yeild': '0.5438967892133088%', 'expense_ratio_annual_amount': 303.00190262582055, 'expense_ratio_annual_per': '0.5438967892133088%'}
        print(result)
    return render(request, 'output.html', {'portfolio': result, 'years': years, 'amount': str(amount)+"£", 'risk_level': risk_level})