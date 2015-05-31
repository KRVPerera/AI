from __future__ import print_function
__author__ = 'krv'
"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    The brackets are not part of the input but tells that
    parameter is optional.

    $python a_priori.py [-n] [-p] [-o OUTPUT] support filename

    -n If given the program will consider that the objects are
    numbers (not strings). Otherwise it considers the strings.

    -p If given parameter the program considers that the minimum
     support price given by the -s parameter is the percentage
     of baskets that should be an itemset to be significant.
"""

import sys
import re
import argparse
from collections import *


def main():
    parser = argparse.ArgumentParser(description='Data mining')
    parser.add_argument('-n', help='Consider data as numeric', action="store_true")
    parser.add_argument('-p', help='Considers that minimum support '
                                    'given is the percentage of baskets '
                                    'that should be an itemset to be significant', action="store_true")
    parser.add_argument('-o', help='Save output to a file', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('support', help='support price', type=float)
    parser.add_argument('filename', help='file name of DATASET', type=argparse.FileType('r'),
                        default=sys.stdin)
    args = parser.parse_args()

    x = getData(args.filename, args.n)
    frq = aPriori(x, args.support, args.p)
    if args.o:
       sys.stdout = args.o
    for k, v in frq.items():
        print (k, ':', v, ';', end='')
    print()

def getData(infile, numbers=False):
    """
        This will read input file and save them in a list
    :param infile: DATASET in CSV format
    :return: return a list of all the data
    """
    dataList = []
    lines = infile.read()
    lines = lines.splitlines()

    for line in lines:
        tmpList = []
        words = re.findall(r"[\w'&]+", line)
        for word in words:
            word = word.rstrip(',')
            if numbers:  # check whether the word is a number before
                value = int(word)
                tmpList.append(value)
            else:

                tmpList.append(word)  # over kill for string as already split

        dataList.append(tmpList)
    return dataList


def apriori_first_pass(dataList, s=1, p=True):
    """
        Create the first pass data set
    :param dataList: list of items
    :return: return a dictionary of candidate item sets of size one
    """


    candidateList = defaultdict(int)
    for itemset in dataList:
        for item in itemset:
            candidateList[(item,)] += 1

    frqList = defaultdict(int)
    if p:
        for item, count in candidateList.items():
            support = float(count)/len(dataList)
            if support >= s:
                frqList[item] = support
    else:
        for item, count in candidateList.items():
            if count >= s:
                frqList[item] = count

    return frqList


def pairs(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def aPrioriPass(dataList, k, freqk, s=1, p=True):
    """
        Generate k+1 pass using k pass list
    :param dataList: Dataset
    :param k: length of the set
    :param freqk: k length frequency dictionary
    :param s: minimum support
    :param p: percentage flag
    :return: k+1 length frequency list
    """
    counts = defaultdict(int)
    for itemset in dataList:
        items = set(itemset)
        item_set = map(frozenset, freqk.keys())
        itemset_pairs = pairs(item_set, k+1)
        candidates = []
        for pair in itemset_pairs:
            candidate = tuple(pair)
            if candidate not in candidates:
                candidates.append(candidate)
                if len(candidate) == k+1 and pair.issubset(items):
                    counts[candidate] += 1

    frqList = defaultdict(int)
    if p:
        for item, count in counts.items():
            support = float(count)/len(dataList)
            if support >= s:
                frqList[item] = support
    else:
        for item, count in counts.items():
            if count >= s:
                frqList[item] = count

    return frqList


def aPriori(dataList, s=1, p=True):
    """
        Return all freq list
    :param dataList: Dataset
    :param s: minimum support
    :param p: percentage support flag
    :return: all frequency list
    """
    allFreq = defaultdict(int)
    k = 1
    freqk = apriori_first_pass(dataList, s, p)
    while freqk:
        allFreq.update(freqk)
        freq = aPrioriPass(dataList, k, freqk, s, p)
        freqk = freq
        k += 1
    return allFreq


if __name__ == '__main__':
    main()