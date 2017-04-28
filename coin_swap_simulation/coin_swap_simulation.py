# coding: utf-8

"""
This is a simulation of a random game, that goes like this:

    * From a group of N people, we pick a random pair.
    * Then we toss a coin. (random.random() < 0.5)
    * if the result is heads, we take one coin from person A and give it to B.
    * if the result is tails, we take one coin from person B and give it to A.
    * and... loop until the results are interesting...

    * optionally - remove someone from the game if they get down to 0 coins.

PROTIP: use pypy since it can get slow very quickly.
"""

from __future__ import print_function

from pprint import pprint
import random
import time


class Person:

    def __init__(self, id, coins):
        self.id = id
        self.coins = coins

        # adding bias.
        self.skill = random.random()

    def __repr__(self):
        return "Person(id={}, coins={}, skill={})".format(
            self.id, self.coins, self.skill
        )


def swap_coins(A, B):
    A.coins -= 1
    B.coins += 1


def population(people, coins):
    return [Person(i, coins) for i in range(people)]


def random_two_people(people):
    return random.sample(people, 2)


def flush_bankrupts(people):
    for b in people:
        if b.coins <= 0:
            people.remove(b)


def xor(a, b):
    """For function arguments"""
    return (a or b) and not (a and b)


def single_iteration(people, chance=0, skill_weight=0):

    assert xor(chance, skill_weight)
    A, B = random_two_people(people)

    if chance:
        if random.random() < chance:
            swap_coins(A, B)
        else:
            swap_coins(B, A)

    elif skill_weight:
        # normal skill weight is 0.5
        # anything above 0.5 is skewing towards more skillful
        # anything below 0.5 is skewing towards less skillful
        if A.skill > B.skill and random.random() < skill_weight:
            swap_coins(B, A)
        else:
            swap_coins(A, B)

    flush_bankrupts(people)


def game(N, coins, chance=0, skill_weight=0):
    assert xor(chance, skill_weight)

    people = population(N, coins)
    debug = False
    i = 0
    t = time.time()

    while True:
        i += 1
        single_iteration(people, chance, skill_weight)

        if debug:
            print("On {}-th iteration, {}".format(i, len(people)))
        if len(people) <= (N / 10):
            print("\n"*10)
            print({
                "finished": "with top 10%",
                "people": N,
                "coins_per_person": coins,
                "iterations": i,
                "chance": chance,
                "skill_weight": skill_weight,
            })
            people = sorted(people, key=lambda x: x.coins, reverse=True)
            pprint(people[:5])
            pprint(people[-5:])
            break

    print("Finished in", time.time() - t)


game(N=int(1000), coins=10, chance=0.5)
game(N=int(1000), coins=10, skill_weight=0.5)
game(N=int(10000), coins=5, skill_weight=0.5)
game(N=int(10000), coins=5, skill_weight=1)
