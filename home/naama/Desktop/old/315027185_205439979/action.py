import sys
import persistance
import printdb
from persistance import repo


def run(args):
    f = open(args, "r")
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        splited = line.split(',')
        product = repo.products.find(splited[0])
        q = int(product.quantity)
        l = int(splited[1])
        sum = l + q
        if sum >= 0:
            repo.products.updateProduct(splited[0], sum)
            activity = persistance.Activity(splited[0], splited[1], splited[2], splited[3])
            repo.activities.insert(activity)
    printdb.run()


if __name__ == '__main__':
    run(sys.argv[1])
