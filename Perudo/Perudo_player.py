from die import die
from .String_en import DUDO, COMPTE_EXACT, BAD_BET_ERROR, INVALID_BET_EXCEPTION, INVALID_DIE_VALUE_ERROR, \
                INVALID_NON_WILDCARD_QUANTITY, INVALID_WILDCARD_QUANTITY, NON_PALIFICO_CHANGE_ERROR
from bet_exceptions import NonPalificoChangeException, InvalidBetException, InvalidDieValueException,\
                             InvalidNonWildcardQuantityException, InvalidWildcardQuantityException
from bet import create_bet


class Perudo_player():
    """
    The perudo player class, transform a discord person class into a player of Perudo

    args:
            discord person:

    attributes:
            discord_member: 
            n_dice (int) : number of dice
            name (str) : discord mention of the person
            dice (list) : list of dice
    """

    def __init__(self, discord_member, ndice, instance):
        self.discord_member = discord_member
        self.ndice = ndice
        self.name = discord_member.mention
        self.mention = discord_member.mention

        self.dices = []
        self.instance = instance

        self.palifico_round = -1

        for i in range(0, ndice):
            self.dices.append(die())

    def roll_dice(self):
        for die in self.dices:
            die.roll()
        # Sort dice into value order e.g. 4 2 5 -> 2 4 5
        self.dices = sorted(self.dice, key=lambda die: die.value)

    def count_dice(self, value):
        number = 0
        for die in self.dices:
            if die.value == value or (not self.instance.is_palifico_round() and die.value == 1):
                number += 1
        return number

    def check_bet(self):
        return lambda m: m.author == self.joueur and m.channel == self.instance.ctx.channel

    async def make_bet(self, current_bet):
        string = "C'est à toi de jouer, voici tes dés :"
        await self.instance.ctx.send("C'est à {0.mention} de jouer" .format(self.joueur))
        for die in self.dices:
            string += ' {0}'.format(die.value)
        # print(self.name + string)
        await self.discord_member.send(self.name + string)

        bet = None
        while bet is None:
            bet_input = await self.instance.bot.wait_for('message', check=self.check_bet())
            bet_input = bet_input.content
            print(str(bet_input))

            if bet_input.lower() == 'dudo':
                return DUDO
            if bet_input.lower() == 'exact':
                return COMPTE_EXACT

            if '*' not in bet_input:
                await self.instance.ctx.send(BAD_BET_ERROR)
                print(BAD_BET_ERROR)
                continue
            bet_fields = bet_input.split('*')
            if len(bet_fields) < 2:
                await self.instance.ctx.send(BAD_BET_ERROR)
                print(BAD_BET_ERROR)
                continue

            try:
                quantity = int(bet_fields[0])
                value = int(bet_fields[1])

                try:
                    bet = create_bet(
                        quantity, value, current_bet, self, self.client)
                except InvalidDieValueException:
                    bet = None
                    print(INVALID_DIE_VALUE_ERROR)
                    await self.instance.ctx.send(INVALID_DIE_VALUE_ERROR)
                except NonPalificoChangeException:
                    bet = None
                    print(NON_PALIFICO_CHANGE_ERROR)
                    await self.instance.ctx.send(NON_PALIFICO_CHANGE_ERROR)
                except InvalidNonWildcardQuantityException:
                    bet = None
                    print(INVALID_NON_WILDCARD_QUANTITY)
                    await self.instance.ctx.send(INVALID_NON_WILDCARD_QUANTITY)
                except InvalidWildcardQuantityException:
                    bet = None
                    print(INVALID_WILDCARD_QUANTITY)
                    await self.instance.ctx.send(INVALID_WILDCARD_QUANTITY)
                except InvalidBetException:
                    bet = None
                    print(INVALID_BET_EXCEPTION)
                    await self.instance.ctx.send(INVALID_BET_EXCEPTION)
            except ValueError:
                print(BAD_BET_ERROR)
                await self.instance.ctx.send(BAD_BET_ERROR)

        return bet

    async def send_dice(self):
        string = "Here are your dices :"
        for die in self.dices:
            string += ' {0}'.format(die.value)
            # print(self.name + string)
        await self.discord_member.send(self.name + string)
