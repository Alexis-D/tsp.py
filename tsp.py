#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from copy import copy

import random

class TSP:
    """Use a genetic algorithm to find the shortest way to visit all cities."""

    def __init__(self, cities, **kwd):
        """cities is a list of tuple (x, y) where x and y are the coordinates
           of each city

           named args:
               crossover_rate: the crossover_rate, default to .7
               mutation_rate: the mutation_rate, default to .01
               chromosomes: the number of chromosomes, default to 100
               generations: the number of generations, default to 100
               contestants: the number of contestants to select fathers &
                            mothers, default to 5
               cycle: the salesman does a cycle (start from A, ends in A),
                      default to True
               elite: the number of "best" chromosomes to keep between
                      two generations"""
        self.crossover_rate = kwd.get('crossover_rate', .7)
        self.mutation_rate = kwd.get('mutation_rate', .01)
        self.chromosomes = kwd.get('chromosomes', 100)
        self.generations = kwd.get('generations', 100)
        self.contestants = kwd.get('contestants', 5)
        self.cycle = kwd.get('cycle', True)
        self.elite = kwd.get('elite', 10)
        self.cities = cities
        self.gen = []
        self.next_gen = []

    def _first_gen(self):
        """Generate the first generation of chromosomes"""
        for i in range(self.chromosomes):
            l = copy(self.cities)
            random.shuffle(l)
            self.gen.append((l, 0))

    def _euclidean_distance(self, a, b):
        """Return the euclidean distance between a & b"""
        xa, ya = a
        xb, yb = b
        return ((xb - xa) ** 2 + (yb - ya) ** 2) ** .5

    def _fitness(self, gen):
        """Evaluate each chromosome by using euclidean distance"""
        for i, (c, f) in enumerate(gen):
            if f != 0:
                break

            d = 0
            for j in range(1, len(c)):
                d += self._euclidean_distance(c[j - 1], c[j])

            if self.cycle:
                d += self._euclidean_distance(c[-1], c[0])

            gen[i] = (c, 1 / d)

    def _contest(self):
        """Run a contest between the chromosomes to find the best ones"""
        l = random.sample(self.gen, self.contestants)
        return max(l, key=lambda x: x[1])[0]

    def _crossover(self, father, mother):
        """Run the crossover step if needed, otherwise return a copy of
           the father"""
        if random.random() <= self.crossover_rate:
            crossover_index = random.randint(0, len(self.cities) - 1)
            begin_father = father[:crossover_index]
            end_father = father[crossover_index:]
            begin_mother = mother[:crossover_index]
            end_mother = mother[crossover_index:]

            child = begin_father + end_mother

            orphans = list(set(end_father) & set(begin_mother))
            dups = []

            for i, c in enumerate(child):
                if c in dups:
                    child[i] = orphans.pop()

                else:
                    dups.append(c)

            return child

        else:
            return copy(father)

    def _mutate(self, child):
        """Mutate the child according to the mutation_rate"""
        for i, c in enumerate(child):
            if random.random() <= self.mutation_rate:
                j = random.randint(0, len(self.cities) - 1)
                child[i], child[j] = child[j], c

    def run(self):
        """Compute the shortest path and returns it"""
        self._first_gen()

        best_fitness_so_far = 0

        for i in range(self.generations):
            self._fitness(self.gen)
            self.next_gen = []

            if max(self.gen, key=lambda x: x[1])[1] > best_fitness_so_far:
                best_fitness_so_far = max(self.gen, key=lambda x: x[1])[1]
                print i, best_fitness_so_far

            for j in range(self.chromosomes):
                father = self._contest()
                mother = self._contest()
                child = self._crossover(father, mother)
                self._mutate(child)
                self.next_gen.append((child, 0))

            self._fitness(self.next_gen)
            self.gen.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
            self.next_gen.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
            self.gen = self.gen[:self.elite] + self.next_gen[
                      :self.chromosomes - self.elite]

        self._fitness(self.gen)
        self.gen.sort(cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
        return self.gen[0][0]

if __name__ == '__main__':
    n = 15
    cities = []

    for i in range(n):
        cities.append((random.randint(0, 255), random.randint(0, 255)))

    best = TSP(cities, chromosomes=250, generations=100, elite=25,
               contestants=5, mutation_rate=.15, cycle=True).run()

    from pylab import axis, clf, plot, show

    clf()
    axis([-10, 265, -10, 265])
    x, y = zip(*cities)
    plot(x, y, 'b.', ms=20)
    x, y = zip(*best)
    plot(x + (x[0],), y + (y[0],), 'r-')
    show()

