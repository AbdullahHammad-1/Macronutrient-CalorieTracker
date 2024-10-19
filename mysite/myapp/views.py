from django.shortcuts import render, redirect
from .models import Food, Consume
# Create your views here.


def index(request):
    if request.method == 'POST':
        food_consumed = request.POST['food_consumed']  #(food_consumed) is the name/id in the selectbox
        consumed = Food.objects.get(id=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consumed)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()

    consumed_food = Consume.objects.filter(user=request.user)

    # Calculate total proteins, carbs, fats, and calories
    total_proteins = sum([item.food_consumed.proteins for item in consumed_food])
    total_carbs = sum([item.food_consumed.carbs for item in consumed_food])
    total_fats = sum([item.food_consumed.fats for item in consumed_food])
    total_cals = sum([item.food_consumed.cals for item in consumed_food])

    # Calculate the progress bar width percentage
    cal_percentage = (total_cals / 2000) * 100 if total_cals <= 2000 else 100

    context = {
        'foods': foods,
        'consumed_food': consumed_food,
        'total_proteins': total_proteins,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
        'total_cals': total_cals,
        'cal_percentage': cal_percentage,
        'exceeded': total_cals > 2000,
    }

    return render(request, 'index.html', context)


def delete(request, id):
    consumed = Consume.objects.get(id=id)
    if request.method == "POST":
        consumed.delete()
        return redirect('/')
    return render(request, 'delete.html')