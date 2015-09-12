from django.http.response import HttpResponse
from rms.rms_models.models import Users,FoodItem,Restaurant,FoodContent,BasicFoodItem,UserRatings,Quality,BasicFoodQuality,Allergic,Deficiency,Transaction
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
# Create your views here.

#Some Important Parameters
WEIGHT_HEALTH = 0.3
WEIGHT_PRICE = 0.3
WEIGHT_TIME = 0.3
WEIGHT_RATING = 0.7
TOTAL_SUGGESTIONS = 5
USER_DEFICIENCY = 1

class SuggestionTable(object):
    def __init__(self,food_name,price,scaled_health,scaled_price,scaled_time,ratings,user_deficiency,calculated_value):
        self.food_name = food_name
        self.price = price
        self.scaled_time = scaled_time
        self.scaled_health = scaled_health
        self.scaled_price = scaled_price
        self.ratings = ratings
        self.user_deficiency = user_deficiency
        self.calculated_value = calculated_value
    def __str__(self):
        return 'food_name: '+str(self.food_name)+'price: '+str(self.price)+' scaled_time: '+str(self.scaled_time)+' scaled_health: '+str(self.scaled_health)+' scaled_price: '+str(self.scaled_price)+' ratings: '+str(self.ratings)+' deficiency: '+str(self.user_deficiency)
    def get_ratings(self):
        return self.ratings

@csrf_exempt
def verify_cred(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        temp_user = Users.objects.filter(_username=username,_password=password)
        if len(temp_user) == 0:
            response_data['result'] = 'failed'
            response_data['message'] = 'No_USER'
        else:
            response_data['username'] = temp_user[0].get_username()
            response_data['name'] = temp_user[0].name
            response_data['message'] = 'USER_PRESENT'
            request.session['username'] = username
    else:
        response_data['message'] = 'Wrong request sent!!!'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def add_restaurant(request):
    response_data = {}
    if request.method == 'GET':
        response_data['message'] = 'Wrong request sent!!!'
    else:
        id = request.POST['restaurant_id']
        name = request.POST['restaurant_name']
        locations = request.POST['restaurant_location']
        restaurant_count = Restaurant.objects.filter(Q(_rest_id=id) | (Q( _rest_name=name) & Q(_rest_location=locations))).count()
        if restaurant_count==0:
            response_data['restaurant_id'] = id
            response_data['restaurant_name'] = name
            response_data['restaurant_rate'] = 0
            Restaurant.objects.create(_rest_id=id,_rest_name=name,_rest_location=locations)
            response_data['message'] = 'Restaurant added Succesfully!!!'
        else:
            response_data['message'] = 'Restaurant already present!!'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def add_user(request):
    response_data={}
    response_data['message']=''
    if request.method=='GET':
        response_data['message']='Wrong request sent!!!'
    else:
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        calorie_intake = request.POST['calorie_intake']
        budget = request.POST['budget']
        user_count = Users.objects.filter(_username=username).count()
        if user_count==0:
            Users.objects.create(_username=username,_password=password,name=name,_per_meal_cost=budget,_calorie_intake_per_meal=calorie_intake)
            response_data['message'] = 'User added Successfully!!!'
        else:
            response_data['message'] = 'User already present!!'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

"""
@csrf_exempt
def get_calories(request):
    food_item_id = request.POST['food_item_id']
    food_item_list = FoodItem.objects.filter(_item_id=food_item_id)
    food_item = food_item_list[0]
    food_item.set_calorie_value()
    food_item.save()
    response_data = {}
    response_data['food_id'] = str(food_item)
    response_data['calories']= food_item.get_calories()
    return HttpResponse(json.dumps(response_data),content_type="application/json")
"""

@csrf_exempt
def load_menu(request):
    restaurant_id = request.POST['restaurant_id']
    restaurant_list = Restaurant.objects.filter(_rest_id=restaurant_id)
    rest_count = len(restaurant_list)
    response_data = {}
    if rest_count != 0:
        restaurant_name = str(restaurant_list[0])+' ; '+ restaurant_list[0].get_location()
        food_list = FoodItem.objects.filter(_restaurant=restaurant_list[0])
        menu = []
        count = 0
        for food in food_list:
            menu.append(food.get_name())
            count+=1
        response_data['count'] = count
        response_data['name'] = restaurant_name
        response_data['menu'] = str(menu)
    else:
        response_data['message'] = 'Restaurant does not exist!'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def create_suggestion_table(request):
    rest_id = request.POST['restaurant_id']
    user_id = request.POST['user_id']
    algo = request.POST['algo']
    restaurant_list = Restaurant.objects.filter(_rest_id=rest_id)
    food_list = FoodItem.objects.filter(_restaurant=restaurant_list[0])
    user_list = Users.objects.filter(_username=user_id)
    suggestion_table = []
    count = 0
    if algo == 'health_and_nutrition':
        allergic_list = Allergic.objects.filter(_user_id=user_list[0])
        allergic_basic_food_list = []
        allergic_basic_food_list_temp = []
        for allergy in allergic_list:
            allergic_basic_food_list_temp = BasicFoodQuality.objects.filter(_qual_id=allergy.get_allergy())
            allergic_basic_food_list.extend(allergic_basic_food_list_temp)
        allergic_basic_food_list = list(set(allergic_basic_food_list))

        deficiency_list = Deficiency.objects.filter(_user_id=user_list[0])
        deficiency_basic_food_list = []
        deficiency_basic_food_list_temp = []
        for deficiency in deficiency_list:
            deficiency_basic_food_list_temp = BasicFoodQuality.objects.filter(_qual_id=deficiency.getdeficiency())
            deficiency_basic_food_list.extend(deficiency_basic_food_list_temp)
        deficiency_basic_food_list = list(set(deficiency_basic_food_list))

    for food in food_list:
        user_deficiency = 0
        if algo == 'health_and_nutrition':
            food_item_basic_food_content_list = []
            food_item_allergic_basic_food_list = []
            food_item_deficiency_basic_food_list = []
            food_item_basic_food_content_list = FoodContent.objects.filter(_food_id=food)
            food_item_allergic_basic_food_list = list(set(allergic_basic_food_list) & set(food_item_basic_food_content_list))
            allergy_count = len(food_item_allergic_basic_food_list)
            if allergy_count == 0:
                food_item_deficiency_basic_food_list = list(set(deficiency_basic_food_list) & set(food_item_basic_food_content_list))
                deficiency_count = len(food_item_deficiency_basic_food_list)
                if deficiency_count != 0:
                    user_deficiency = deficiency_count*USER_DEFICIENCY
        if (algo == 'health_and_nutrition' and allergy_count ==0) or algo != 'health_and_nutrition':
            user_rate_list = UserRatings.objects.filter(_user_id=user_list[0],_food_item_id=food)
            user_rate = user_rate_list[0].get_ratings()
            row = SuggestionTable(food.get_name(),food.get_price(),food.get_scaled_health(),food.get_scaled_price(),food.get_scaled_time(),user_rate,user_deficiency,0)
            return HttpResponse(row.__str__())
            suggestion_table.append(row)
            count+=1
    calculated_value = 0
    for food_item in suggestion_table:
        return (food_item.get_ratings())
        calculated_value = food_item.ratings*WEIGHT_RATING
        if algo == 'health_and_nutrition':
            if food_item.get_calories()<=user_list[0].get_calories():
                calculated_value += food_item.scaled_health*WEIGHT_HEALTH
                calculated_value += user_deficiency
                return HttpResponse(calculated_value)
            else:
                calculated_value = 0
        elif algo == 'soft_on_the_wallet':
            if food_item.get_price<=user_list[0].get_budget():
                calculated_value += food_item.scaled_price*WEIGHT_PRICE
            else:
                calculated_value = 0
        elif algo == 'in_a_hurry!!':
            calculated_value += food_item.scaled_time*WEIGHT_TIME
        elif algo == 'likeable':
            calculated_value = food_item.ratings
        food_item.calculated_value = calculated_value
    suggestion_table.sort(key=lambda x: x.calculated_value, reverse=True)
    final_suggestion_list = []
    count = 0
    for food_item in suggestion_table:
        final_suggestion_list.append('food_name: '+str(food_item.food_name)+'price: '+str(food_item.price))
        count +=1
        if count == TOTAL_SUGGESTIONS:
            break
    response_data = {}
    response_data['final_suggestion_list'] = str(final_suggestion_list)
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def transaction_complete(request):
    response_data = {}
    if request.method == 'GET':
        response_data['message'] = 'Wrong request sent!!!'
    else:
        rest_id = request.POST['restaurant_id']
        user_id = request.POST['user_id']
        paid = request.POST['paid']
        amount = request.POST['amount']
        date_time = request.POST['date_time']
        user_list = Users.objects.filter(_username=user_id)
        restaurant_list = Restaurant.objects.filter(_rest_id=rest_id)
        if paid == 'True':
            Transaction.objects.create(_date_time=date_time,_user_id=user_list[0],_rest_id=restaurant_list[0],_paid=True,_amount=float(amount))
            response_data['message'] = 'Transaction cleared successfully!!!'
        else:
            response_data['message'] = 'Please pay to complete transaction!'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def update_user_ratings(request):
    response_data = {}
    if request.method == 'GET':
        response_data['message'] = 'Wrong request sent!!!'
    else:
        user_id = request.POST['user_id']
        rest_id = request.POST['restaurant_id']
        item_name = request.POST['item_name']
        user_list = Users.objects.filter(_username=user_id)
        restaurant_list = Restaurant.objects.filter(_rest_id=rest_id)
        food_item_list = FoodItem.objects.filter(_item_name=item_name,_restaurant=restaurant_list[0])
        user_food_item_list = UserRatings.objects.filter(_user_id=user_list[0],_food_item_id=food_item_list[0])
        count = len(user_food_item_list)
        if count != 0:
            old_rate = user_food_item_list[0].get_ratings()
            user_food_item_list[0].set_rate(old_rate+1)
            user_food_item_list[0].save()
            response_data['message'] = 'Ratings updated successfully'
        else:
            UserRatings.objects.create(_user_id=user_list[0],_food_item_id=food_item_list[0],_rate=1)
            response_data['message'] = 'Ratings entered successfully'
    return HttpResponse(json.dumps(response_data),content_type="application/json")