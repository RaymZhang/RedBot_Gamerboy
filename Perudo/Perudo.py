from redbot.core import commands 
from .Perudo_player import Perudo_player
from .. import	Coggameinstance
from String_en import *


class Perudo(Coggameinstance):
	"""
	The Perudo cogs and class 

	"""

	def __init__(self, bot, ctx):
		super().__init__(bot,ctx) # supper init from the Coggameinstance
		self.ndice = 0
		self.ndice_player = None
		self.players = None
		self.first_player = None

	
	async def run_game(self):
		self.round = 0
		self.game_on = 2
		self.players = []


		for joueur in self.players:
			self.players.append(
				perudo_player(
					joueur = joueur,
					dice_number = self.ndice_player,
					instance = self

				)
			)

		random.shuffle(self.players)

		print(welcome_message(self.players))
		await self.ctx.send(welcome_message(self.players))

		self.first_player = random.choice(self.players)

		while len(self.players) > 1:
			await self.run_round()

		print(winner(self.players[0].name))
		self.game_on = 0

		await self.ctx.send(winner(self.players[0].name))

	async def run_round(self):
		self.round += 1
		for player in self.players:
			player.roll_dice()
			await player.send_dice()


		print(round_title(round_number = self.round, is_palifico_round=self.is_palifico_round()))
		await self.ctx.send(\
			round_title(round_number = self.round, is_palifico_round=self.is_palifico_round()))

		round_over = False
		current_bet = None
		current_player = self.first_player
		print('{0} play first...'.format(current_player.name))
		await self.ctx.send('{0} play first...'.format(current_player.name))

		while not round_over:
			next_player = self.get_next_player(current_player)
			next_bet = await current_player.make_bet(current_bet)
			bet_string = None
			if next_bet == DUDO:
				bet_string = 'MENTEUR!'
			elif next_bet == COMPTE_EXACT:
				bet_string = 'Compte exacte !'
			else:
				bet_string = next_bet
			print('{0}: {1}'.format(current_player.name, bet_string))
			await self.ctx.send('{0}: {1}'.format(current_player.name, bet_string))

			if next_bet == DUDO:
				self.pause(0.5)
				await self.run_dudo(current_player, current_bet)
				round_over = True
			elif next_bet == COMPTE_EXACT:
				self.pause(0.5)
				await self.run_compte_exact(current_player, current_bet)
				round_over = True
			else:
				current_bet = next_bet

			if len(self.players) > 1:
				current_player = next_player

			self.pause(0.5)

		self.pause(1)

	async def run_dudo(self, player, bet):
		dice_count = self.count_dice(bet.value)
		if dice_count >= bet.quantity:
			print(incorrect_dudo(dice_count, bet.value))
			await self.ctx.send(incorrect_dudo(dice_count, bet.value))

			self.first_player = player
			await self.remove_die(player)
		else:
			print(correct_dudo(dice_count, bet.value))
			await self.ctx.send(correct_dudo(dice_count, bet.value))
			previous_player = self.get_previous_player(player)
			self.first_player = previous_player
			await self.remove_die(previous_player)

	async def run_compte_exact(self, player, bet):
		dice_count = self.count_dice(bet.value)

		if dice_count != bet.quantity:
			print(incorrect_compte_exacte(dice_count, bet.value))
			await self.ctx.send(incorrect_compte_exacte(dice_count, bet.value))
			self.first_player = player
			await self.remove_die(player)
		else:
			print(correct_compte_exacte(dice_count, bet.value))
			await self.ctx.send(correct_compte_exacte(dice_count, bet.value))
			previous_player = self.get_previous_player(player)
			self.first_player = player
			await self.add_die(player)


	def count_dice(self, value):
		number = 0
		for player in self.players:
			number += player.count_dice(value)

		return number

	async def remove_die(self, player):
		player.dices.pop()
		msg = '{0} loose a dice'.format(player.name)
		if len(player.dices) == 0:
			msg += ' {0} adios !'.format(player.name)
			self.first_player = self.get_next_player(player)
			self.players.remove(player)
		elif len(player.dices) == 1 and player.palifico_round == -1:
			player.palifico_round = self.round + 1
			msg += ' Last dice ! {0} is palifico!'.format(player.name)
		else:
			msg += ' Only {0} dices left!'.format(len(player.dices))
		# print(msg)
		await self.ctx.send(msg)

	async def add_die(self, player):
		if len(player.dices) < self.dice_number :
			player.dices.append(Die())
			msg = '{0} Earn a dice'.format(player.name)
			msg += ' He has now {0} !'.format(len(player.dices))
		else :
			msg = '{0} Has already the maximun number of dice'.format(player.name)
		# print(msg)
		await self.ctx.send(msg)


	def is_palifico_round(self):
		# if len(self.players) < 3:
		# 	return False
		for player in self.players:
			if player.palifico_round == self.round:
				return True
		return False

	# def get_random_name(self):
	# 	random.shuffle(bot_names)
	# 	return bot_names.pop()

	def get_next_player(self, player):
		return self.players[(self.players.index(player) + 1) % len(self.players)]

	def get_previous_player(self, player):
		return self.players[(self.players.index(player) - 1) % len(self.players)]

	def pause(self, duration):
		if config.play_slow:
			time.sleep(duration)


