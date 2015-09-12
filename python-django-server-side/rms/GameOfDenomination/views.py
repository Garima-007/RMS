# Create your views here.
import json
from rms.GameOfDenomination.models import Game,GameRecord
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def host_game(request):
    host_id = request.POST['host_id']
    Game.objects.create(host_user_id=host_id)
    response_data={}
    response_data['message'] = 'HOST_CREATED'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def join_host(request):
    host_id = request.POST['host_id']
    client_id = request.POST['client_id']
    game_list = Game.objects.filter(host_user_id=host_id)
    game = game_list[0]
    game.client_user_id = client_id
    game.save()
    response_data = {}
    response_data['connection_name'] = str(game)
    response_data['message'] = 'HOST_ADDED'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def start_game(request):
    host_id = request.POST['host_id']
    client_id = request.POST['client_id']
    num_of_coins = request.POST['num_of_coins']
    player = request.POST['player']
    coin_pos = num_of_coins
    game_list = Game.objects.filter(host_user_id=host_id,client_user_id=client_id)
    game = game_list[0]
    GameRecord.objects.create(game=game,currentPlayer=player,currentCoinPos=coin_pos)
    response_data = {}
    response_data['number_of_coins'] = num_of_coins
    response_data['message'] = 'GAME_STARTED'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def update_move(request):
    host_id = request.POST['host_id']
    client_id = request.POST['client_id']
    player = request.POST['player']
    coin_pos = request.POST['pos']
    game_list = Game.objects.filter(host_user_id=host_id,client_user_id=client_id)
    game = game_list[0]
    record_list = GameRecord.objects.filter(game=game)
    record = record_list[0]
    record.currentPlayer = player
    record.currentCoinPos = coin_pos
    record.save()
    response_data = {}
    response_data['message'] = 'MOVE_UPDATED_TO_'+str(record)
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def get_move(recquest):
    host_id = recquest.POST['host_id']
    client_id = recquest.POST['client_id']
    game_list = Game.objects.filter(host_user_id=host_id,client_user_id=client_id)
    game = game_list[0]
    record_list = GameRecord.objects.filter(game=game)
    record = record_list[0]
    response_data = {}
    response_data['pos'] = record.currentCoinPos
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@csrf_exempt
def end_game(request):
    host_id = request.POST['host_id']
    client_id = request.POST['client_id']
    game_list = Game.objects.filter(host_user_id=host_id,client_user_id=client_id)
    game = game_list[0]
    record_list = GameRecord.objects.filter(game=game)
    record = record_list[0]
    record.delete()
    game.delete()
    response_data = {}
    response_data['message'] = 'GAME_ENDED'
    return HttpResponse(json.dumps(response_data),content_type="application/json")