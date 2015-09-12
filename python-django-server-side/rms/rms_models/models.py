from django.db import models

#Some Important Parameters
MAX_LEN_OF_USERNAME = 15
MAX_LEN_OF_NAME = 200
MAX_LEN_OF_PASSWORD = 30
MAX_LEN_OF_FOOD_ITEM_CODE = 50
DEFAULT_CALORIE_INTAKE = 100
DEFAULT_BUDGET = 300
DEFAULT_FIELD_VALUE = None

class Users(models.Model):
    _username = models.CharField(primary_key=True,max_length=MAX_LEN_OF_USERNAME,null=False,default=DEFAULT_FIELD_VALUE)  #Primary Key
    name = models.CharField(max_length=MAX_LEN_OF_NAME,null=False,default=DEFAULT_FIELD_VALUE)
    _password = models.CharField(max_length=MAX_LEN_OF_PASSWORD,null=False,default=DEFAULT_FIELD_VALUE)
    _calorie_intake_per_meal = models.FloatField(default=DEFAULT_CALORIE_INTAKE)
    _per_meal_cost = models.FloatField(default=DEFAULT_BUDGET)
    def __str__(self):
        return self._username
    def get_username(self):
        return self._username
    def set_password(self,password):
        self._password = password
    def get_calories(self):
        return self._calorie_intake_per_meal
    def set_calories(self,calorie):
        self._calorie_intake_per_meal = calorie
    def get_budget(self):
        return self._per_meal_cost
    def set_budget(self,budget):
        self._per_meal_cost = budget

class Restaurant(models.Model):
    _rest_id = models.CharField(max_length=MAX_LEN_OF_FOOD_ITEM_CODE)
    _rest_name = models.CharField(max_length=MAX_LEN_OF_FOOD_ITEM_CODE)
    _rest_location = models.CharField(max_length=MAX_LEN_OF_FOOD_ITEM_CODE)
    _rest_ratings = models.FloatField(default=0)
    def __str__(self):
        return self._rest_id
    def get_location(self):
        return self._rest_location
    def set_location(self,location):
        self._rest_location = location
    def get_ratings(self):
        return self._rest_ratings
    def set_ratings(self,ratings):
        self._rest_ratings = ratings
    def get_id(self):
        return self._rest_id
    def get_name(self):
        return self._rest_name
    def set_name(self,name):
        self._rest_name = name

class BasicFoodItem(models.Model):
    """
        These are the ones whose values we will be assuming and using them to calculate for other items
    """
    _item_id = models.CharField(primary_key=True,max_length=MAX_LEN_OF_FOOD_ITEM_CODE,null=False,default=DEFAULT_FIELD_VALUE) #Primary key
    _calorie_content = models.FloatField(null=False,default=0)
    def __str__(self):
        return self._item_id
    def get_calories(self):
        return self._calorie_content
    def set_calories(self,calorie):
        self._calorie_content = calorie

class FoodItem(models.Model):
    _item_name =  models.CharField(max_length=MAX_LEN_OF_FOOD_ITEM_CODE,null=False,default=DEFAULT_FIELD_VALUE)
    _restaurant = models.ForeignKey(Restaurant)
    _calorie_content = models.FloatField(null=False,default=0)
    _price = models.FloatField(default=0)
    _time = models.FloatField(default=0)
    _scaled_health = models.FloatField(default=0)
    _scaled_price = models.FloatField(default=0)
    _scaled_time = models.FloatField(default=0)
    def __str__(self):
        self.set_calorie_value()
        return self._item_name
    def get_name(self):
        return self._item_name
    def set_calorie_value(self):
        food_content_list = FoodContent.objects.filter(_food_id=self)
        basic_food_list = []
        for food in food_content_list:
            basic_food_list.append(food.get_content_id())
        self._calorie_content = 0
        for basic_food in basic_food_list:
            self._calorie_content += basic_food.get_calories()
    def set_calorie(self,calories):
        self._calorie_content = calories
    def get_calories(self):
        return self._calorie_content
    def get_price(self):
        return self._price
    def set_price(self,price):
        self._price = price
    def get_time(self):
        return self._time
    def set_time(self,time):
        self._time = time
    def get_scaled_health(self):
        return self._scaled_health
    def get_scaled_price(self):
        return self._scaled_price
    def get_scaled_time(self):
        return self._scaled_time
    def set_scaled_health(self):
        max_calorie= FoodItem.objects.filter(_restaurant=self._restaurant).aggregate(Max('_calorie_content'))
        cal = self.get_calories()
        self._scaled_health = cal/max_calorie
    def set_scaled_price(self):
        max_price= FoodItem.objects.filter(_restaurant=self._restaurant).aggregate(Max('_price'))
        price = self.get_price()
        self._scaled_price = price/max_price
    def set_scaled_time(self):
        max_time= FoodItem.objects.filter(_restauarnt=self._restaurant).aggregate(Max('_time'))
        time = self.get_time()
        self._scaled_time = time/max_time

class FoodContent(models.Model):
    _food_id =  models.ForeignKey(FoodItem,null=False,default=DEFAULT_FIELD_VALUE)
    _content_id = models.ForeignKey(BasicFoodItem,null=False,default=DEFAULT_FIELD_VALUE)
    def __str__(self):
        return str(self._food_id)+'-'+str(self._content_id)
    def get_content_id(self):
        return self._content_id
    def get_food_id(self):
        return self._food_id

class Quality(models.Model):
    _name = models.CharField(max_length=MAX_LEN_OF_FOOD_ITEM_CODE)
    def __str__(self):
        return str(self._name)
    def get_name(self):
        return self._name
    def set_name(self,name):
        self._name = name

class BasicFoodQuality(models.Model):
    _basic_food_id = models.ForeignKey(BasicFoodItem)
    _qual_id = models.ForeignKey(Quality)
    def __str__(self):
        return str(self._basic_food_id)+'-'+str(self._qual_id)
    def get_basic_food(self):
        return self._basic_food_id
    def get_quality(self):
        return self._qual_id

class Deficiency(models.Model):
    _user_id = models.ForeignKey(Users)
    _def_id = models.ForeignKey(Quality)
    def __str__(self):
        return str(self._user_id)+'-'+str(self._def_id)
    def get_user(self):
        return self._user_id
    def get_deficiency(self):
        return self._def_id

class Allergic(models.Model):
    _user_id = models.ForeignKey(Users)
    _qual_id = models.ForeignKey(Quality)
    def __str__(self):
        return str(self._user_id)+'-'+str(self._qual_id)
    def get_user(self):
        return self._basic_food_id
    def get_allergy(self):
        return self._qual_id

class UserRatings(models.Model):
    _user_id = models.ForeignKey(Users)
    _food_item_id = models.ForeignKey(FoodItem)
    _rate = models.FloatField(default=0)
    def __str__(self):
        return str(self._user_id)+'-'+str(self._food_item_id)
    def set_rate(self,new_rate):
        self._rate = new_rate
    def get_ratings(self):
        return self._rate

class Transaction(models.Model):
    _user_id = models.ForeignKey(Users)
    _rest_id = models.ForeignKey(Restaurant)
    _paid = models.BooleanField(default=False)
    _date_time = models.CharField(max_length=MAX_LEN_OF_USERNAME,default='abc')
    _amount = models.FloatField(default=0)
    def __str__(self):
        return str(self._user_id)+'-'+str(self._rest_id)+'-'+str(self._paid)+'-'+str(self._date_time)
    def set_paid(self,new_paid):
        self._paid = new_paid
    def set_date_time(self,new_date_time):
        self._date_time = new_date_time
    def get_paid(self):
        return self._paid
    def get_date_time(self):
        return self._date_time
    def set_amount(self,amount):
        self._amount = amount
    def get_amount(self):
        return self._amount

"""
class GenericTable(models.Model):
    _food_item = models.ForeignKey(FoodItem)
    _scaled_health = models.FloatField(default=0)
    _scaled_price = models.FloatField(default=0)
    _scaled_time = models.FloatField(default=0)
    def __str__(self):
        return str(self._food_item)
    def get_food(self):
        return self._food_item
    def get_health(self):
        return self._scaled_health
    def get_price(self):
        return self._scaled_price
    def get_time(self):
        return self._scaled_time
    def set_health(self):
        max_calorie = FoodItem.objects.all().aggregate(Max('_calorie_content'))
        cal = self._food_item.get_calories()
        self._scaled_health = cal/max_calorie
    def set_time(self):
        max_time = FoodItem.objects.all().aggregate(Max('_time'))
        time = self._food_item.get_time()
        self._scaled_time = time/max_time
    def set_price(self):
        max_price = FoodItem.objects.all().aggregate(Max('_price'))
        price = self._food_item.get_price()
        self._scaled_price = price/max_price
"""