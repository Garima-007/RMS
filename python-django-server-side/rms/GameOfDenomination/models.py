from django.db import models

MAX_LEN_OF_NAME = 50

class Game(models.Model):
    host_user_id = models.CharField(max_length = MAX_LEN_OF_NAME)
    client_user_id = models.CharField(max_length = MAX_LEN_OF_NAME)
    def __str__(self):
        return self.host_user_id+' - '+self.client_user_id
    class Meta:
        unique_together = ('client_user_id', 'host_user_id')

class GameRecord(models.Model):
    game = models.ForeignKey(Game)
    currentPlayer = models.IntegerField(default=1)
    currentCoinPos = models.IntegerField(default=10)  #The state of the game which is to be created on other person's PC
    def __str__(self):
        return str(self.game) + ' - '+ str(self.currentPlayer) + ' - ' + str(self.currentCoinPos)