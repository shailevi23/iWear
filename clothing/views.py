from datetime import date
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from clothing.forms import ItemCreationForm, WornEventCreationForm, WeatherRangeForm
from clothing.models import ClothCategory, ClothingItem, WornEvent
from users.views import get_user
import requests

@login_required()
def show_item(request, tag_id):
    user = get_user(request.user.id)
    if not user:
            return redirect('home')
    else:
        item_to_show = get_item(tag_id)
        if(item_to_show is None or item_to_show.owner != user):
            messages.warning(request, f"The item tag id - {tag_id}, isn't in your closet!")
            return redirect('home')
        return render(request, 'clothing/show-item.html', {
        'item': item_to_show,
        'numOfTimesWorn' : item_to_show.numOfTimesWorn,
        'idealWearTemp' :item_to_show.ideal_temperture,
        'dateOfFirstUse' : item_to_show.dateOfFirstUse,
        'dateOfLastUse' : item_to_show.dateOfLastUse,
        })

@login_required()
def show_category(request, category):
    user = get_user(request.user.id)
    if not user:
            return redirect('home')
    else:
        category_total_worn_events = 0
        items_in_category, category_name = get_items_in_category(category, request.user)
        for curr_item in items_in_category:
            category_total_worn_events +=  curr_item.total_worn_events
        num_of_items = len(items_in_category)
        random.shuffle(items_in_category)
        
        return render(request, 'clothing/show-category.html', {
        'items_in_category': items_in_category,
        'category_name': category_name,
        'num_of_items': num_of_items,
        'total_worn_events': category_total_worn_events,
        })


@login_required()
def show_closet(request):
    user = get_user(request.user.id)
    if not user:
            return redirect('home')
    else:
        items_in_closet = user.all_items
        num_of_items = user.number_of_items_in_closet
        first_worn_item_date = date.max
        last_worn_item_date = date.min
        closet_total_worn_events = 0
        items_worn = 0
        categories_dic = {}
        first_worn_item = None
        last_worn_item = None
        least_worn_category = None
        most_worn_category = None
        ideal_temperature = None

        if(len(items_in_closet) != 0):
            first_worn_item = list(items_in_closet)[0]
            last_worn_item =  list(items_in_closet)[0]
            ideal_temperature = 0

            for curr_item in items_in_closet:
                closet_total_worn_events = closet_total_worn_events  + curr_item.total_worn_events

                if curr_item.category not in categories_dic:
                    categories_dic[curr_item.category] = curr_item.category
                
                if first_worn_item_date > curr_item.first_worn_event_date:
                    first_worn_item = curr_item
                    first_worn_item_date = first_worn_item.first_worn_event_date

                if last_worn_item_date < curr_item.last_worn_event_date:
                    last_worn_item = curr_item 
                    last_worn_item_date = last_worn_item.last_worn_event_date
                
                if(curr_item.total_worn_events > 0):
                    ideal_temperature += curr_item.ideal_temperture
                    items_worn += 1
            
            if(items_worn > 0):
                ideal_temperature = ideal_temperature / items_worn
                ideal_temperature = round(ideal_temperature, 1)
        
        num_of_categories = len(categories_dic)

        if(num_of_categories != 0):
            least_worn_category = list(categories_dic.keys())[0]
            most_worn_category = list(categories_dic.keys())[0]

            for category in categories_dic.values():
                curr_cat_total_worn_events = user.get_total_worn_events(category)
                if user.get_total_worn_events(least_worn_category) > curr_cat_total_worn_events:
                    least_worn_category = category
                elif user.get_total_worn_events(most_worn_category) < curr_cat_total_worn_events:
                    most_worn_category = category
            
        if(first_worn_item):
            first_worn_item_worn_event_date = first_worn_item.first_worn_event_date
        else:
            first_worn_item_worn_event_date = None

        if(last_worn_item):
            last_worn_item_worn_event_date = last_worn_item.last_worn_event_date
        else:
            last_worn_item_worn_event_date = None

        if(closet_total_worn_events != 0):
            least_worn_category_percentage = int((user.get_total_worn_events(least_worn_category)/closet_total_worn_events)*100)
            most_worn_category_percentage = int((user.get_total_worn_events(most_worn_category)/closet_total_worn_events)*100)
        else:
            least_worn_category_percentage = 0
            most_worn_category_percentage = 0
        
        return render(request, 'clothing/show-closet.html', {
        'user' : user,
        'numOfItems' : num_of_items,
        'totalWornEvents' : closet_total_worn_events,
        'first_worn_item' : first_worn_item,
        'first_worn_item_worn_event_date' : first_worn_item_worn_event_date,
        'lastWornItem' : last_worn_item,
        'ideal_temperature' : ideal_temperature,
        'last_worn_item_worn_event_date' : last_worn_item_worn_event_date,
        'numOfCategories' : num_of_categories,
        'leastWornCategory' : least_worn_category,
        'leastWornCategorytotalwornevent' : user.get_total_worn_events(least_worn_category),
        'least_worn_category_percentage' :least_worn_category_percentage,
        'mostWornCategory' : most_worn_category,
        'mostWornCategorytotalwornevent' : user.get_total_worn_events(most_worn_category),
        'most_worn_category_percentage' : most_worn_category_percentage,
        'categories' : list(categories_dic.values()),
        })

@login_required()
def recommendations_category(request):
    user = get_user(request.user.id)
    if not user:
        return redirect('home')
    else:
        items_in_closet = user.all_items
        categories_dic = {}
        categories = None
        numOfCategories = None

        if(len(items_in_closet) != 0):
            for curr_item in items_in_closet:
                if curr_item.category not in categories_dic:
                    categories_dic[curr_item.category] = curr_item.category
            categories = list(categories_dic.values())
            numOfCategories = len(categories)

        return render(request, 'clothing/recommendations-category.html', {
        "categories": categories,
        'numOfCategories':numOfCategories,
        })

@login_required()
def recommendations_weather(request):
    user = get_user(request.user.id)
    if not user:
        return redirect('home')
    else:
        if request.method == 'POST':
            weather_range_form = WeatherRangeForm(request.POST)
            if weather_range_form.is_valid():
                minimum_temperature = weather_range_form.cleaned_data['minimum_temperature']
                maximum_temperature = weather_range_form.cleaned_data['maximum_temperature']
                recommended_items = []
                all_items = user.all_items
                if(len(all_items) > 0):
                    for curr_item in  all_items:
                        curr_item_ideal_temperture = curr_item.ideal_temperture
                        if (curr_item_ideal_temperture is not None):
                            if ((minimum_temperature <= curr_item_ideal_temperture) and (curr_item_ideal_temperture <= maximum_temperature)):
                                recommended_items.append(curr_item)
                    num_of_items = len(recommended_items)
                else:
                    recommended_items = None

                return render(request, 'clothing/recommendations-weather.html', {
                'recommended_items': recommended_items,
                'num_of_items': num_of_items,
                "minimum_temperature": minimum_temperature,
                "maximum_temperature": maximum_temperature,
                })
        else:
            weather_range_form = WeatherRangeForm(initial={'minimum_temperature':20, 'maximum_temperature':35})
            items_in_closet = user.all_items
            num_of_items = len(items_in_closet) 

        return render(request, 'clothing/recommendations-weather-form.html', {
        "weather_range_form": weather_range_form,
        'num_of_items': num_of_items,
        })

@login_required()
def recommendations_randomly(request):
    user = get_user(request.user.id)
    if not user:
        return redirect('home')
    else:
        random_index = None
        random_item = None
        items_in_closet = user.all_items

        if(len(items_in_closet) != 0):
            random_index = random.randint(1, items_in_closet.count())
            random_item = items_in_closet[random_index-1]

        return render(request, 'clothing/recommendations-randomly.html', {
        'random_index': random_index,
        'random_item': random_item,
        })

@login_required()
def add_item(request):
    if request.method == 'POST':
        item_creation_form = ItemCreationForm(request.POST)
        if item_creation_form.is_valid():
            item = item_creation_form.save(commit=False)
            item.save()
            path = 'item/' + item_creation_form.cleaned_data['tag_id']
            messages.success(request, f"Item: {item} was add successfully!")
            return redirect(path)
    else:
        item_creation_form = ItemCreationForm(initial={'owner': request.user})
    return render(request, 'clothing/new-item.html', {
    "item_creation_form": item_creation_form,
    })



@login_required()
def add_worn_event(request):
    def get_temp():
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = 'cdbf57cae65a0dc7c5809763f13c67c1'
        CITY = 'Tel Aviv'
        UNIT = 'metric'
        URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY + "&units=" + UNIT
        response = requests.get(URL)
        
        return int(response.json()['main']['temp'])

    if request.method == 'POST':
        worn_event_creation_form = WornEventCreationForm(request.POST)
        if worn_event_creation_form.is_valid():
            tag_id = worn_event_creation_form.cleaned_data['tag_id']
            item = ClothingItem.objects.filter(owner = request.user, tag_id = tag_id).first()
            if(item):
                temperture = get_temp()
                worn_event = WornEvent(item=item, temperture=temperture)
                worn_event.save()
                path = 'item/' + tag_id
                messages.success(request, f"Worn event was add successfully!")
                return redirect(path)
        messages.warning(request, f"The item tag id - {tag_id}, isn't in your closet!")
    else:
        worn_event_creation_form = WornEventCreationForm()
    return render(request, 'clothing/new-worn-event.html', {
    "worn_event_creation_form": worn_event_creation_form,
    })

def get_item(tag_id):
    try:   
        return ClothingItem.objects.filter(tag_id=tag_id).first()
    except:
        return None

def get_items_in_category(category, owner):
    category = ClothCategory.objects.filter(category_name=category).first()
    category_id = category.id
    category_name = category.category_name
    items_in_category = list(ClothingItem.objects.filter(owner=owner, category=category_id))
    return items_in_category, category_name
