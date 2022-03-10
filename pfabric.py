from operator import itemgetter
from random import random


def rank_flows(flows):
    # list_name.sort(key=lambda x:x[1],reverse=True)
    return sorted(flows, key=lambda x: x[1], reverse=True)
    pass


def generate_flow(flows):
    r = random.randint(1,len(flows))


    pass


def dequeue(order, priority_queue):
    order.sort()
    i = 0
    for ele in order:
        print(priority_queue[ele][1])
        # order.remove(order[i])
        # order.remove(ele)







    pass


def scheduling_order(input_flow, priority_queue):
    n = 5
    chunks = [input_flow[i:i + n] for i in range(0, len(input_flow), n)]
    print(chunks)
    order = []
    for ele in chunks:
        for i in ele:
            j = 0
            while i != priority_queue[j][1]:
                j = j+1
            # print(j)
            order.append(j)

        print(order)
        dequeue(order,priority_queue)
        order = []


    pass


def main():
    a = [15, 'a']
    b = [10, 'b']
    c = [5, 'c']

    flows = [a, b, c]
    priority_queue = rank_flows(flows)
    print(priority_queue)
    input_flow = 'aabccaccc'
    scheduling_order(input_flow,priority_queue)
    # generate_flow(flows)

    


if __name__ == "__main__":
    main()
