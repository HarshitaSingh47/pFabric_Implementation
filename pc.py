import math
import threading
import time
import logging
import random
import csv
try:
    import queue
except ImportError:
    import Queue as queue

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

BUF_SIZE = 3
q = queue.PriorityQueue(BUF_SIZE)
# input_string = [[2, 'a'], [3, 'b'], [2, 'a'], [7, 'c'], [7, 'c'], [2, 'a'], [3, 'b']]
input_string = []
drop = []

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while True:
            # threadLock.acquire()
            if not q.full() and len(input_string) > 0:
                # print(len(input_string))
                item = input_string.pop(random.randrange(len(input_string)))
                q.put(item)

                print(q.queue)
                logging.debug('Putting ' + str(item)
                              + ' : ' + str(q.qsize()) + ' items in queue')

                # enqueue operation for the queue

                time.sleep(random.random())
            elif q.full():
                logging.debug('Encountered a full queue...\n Waiting for Dequeue\n\n')
                if len(input_string) != 0:
                    item = input_string.pop(random.randrange(len(input_string)))
                    priority = item[0]
                    list_queue = {}
                    list_queue = list(q.queue)
                    sorted(list_queue, key=lambda x: x[0])
                    # print("This is the sorted list :\n")
                    # print(list_queue)
                    buffer_decision_1 = q.queue[2]
                    buffer_decision_2 = q.queue[1]
                    # print(buffer_decision[0])
                    # print(buffer_decision[0])
                    # print(priority)
                    if priority < buffer_decision_2[0]:
                        top_ele = q.get()
                        next_ele = q.get()
                        dropped_ele = q.get()
                        input_string.append(dropped_ele)
                        q.put(top_ele)
                        q.put(next_ele)
                        q.put(item)
                        logging.debug('Dropped lower priority packet in favor of queued packet. Packet Dropped : '
                                      + str(dropped_ele) + " " + '...\n\n')
                    else:
                        logging.debug(
                            'Dropping incoming packet since the queue is full...\n\n Dropped packet : \t ' + str(item))
                        #packet appended back to input stream since it will be retransmitted later
                        input_string.append(item)
                        # drop.append(item)

                        # if len(drop) > 5 :
                        #     logging.debug('*********Packet Drop Threshold exceeded, entering probe mode*********\n\n')
                        #     drop = []
                        # q.put(buffer_decision)

                    # q.put(item)
                print(q.queue)
                ## The queue is full here, hence the next element that can be added to the queue
                # has to have a priority > existing elements in the queue
                ## If the next element has a lower priority, continue to wait
                # else pop element with low priority and return
                time.sleep(random.random())
            # threadLock.release()
        return


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread, self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logging.debug('Getting ' + str(item)
                              + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(random.random())
        return


def get_input() -> list:
    count = input("Enter the number of flows: \n")
    count = int(count)
    flow = []
    ele = []
    while count  :
        flow_id = input("Enter flow ID: \t")
        flow_size = input("Enter flow size: \t")
        ele = []
        ele.append(flow_id)
        ele.append(flow_size)
        # print(ele)
        flow.append(ele)
        # ele.clear()
        count = count - 1

    print(flow)
    return flow


def generate_priority(flow) -> list:
    priority_list = []
    packet_size = 5

    for ele in flow:
        item = []
        priority = int(ele[1])/packet_size
        priority = math.floor(priority)

        item.append(priority)
        item.append(ele[0])
        priority_list.append(item)

    # print(priority_list)
    for idx in priority_list:
        print("\nPriority of element ", idx[1] , " is ", idx[0], "\n")
    return priority_list


def generate_packet_list(priority_list):
    output_str = []

    for ele in priority_list:

        p = ele[0]
        p = int(p)
        while p != 0:
            item = []
            item.append(ele[0])
            item.append(ele[1])
            output_str.append(item)
            p = p - 1
    # print(output_str)
    return output_str


def read_csvfile(choice):
    file = 'flow_input_simple.csv'
    print(choice)
    choice = int(choice)
    if choice == 2:
        file = 'flow_input.csv'
    elif choice == 1:
        file = 'flow_input_simple.csv'
    with open(file , 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        flow = []
        for row in reader:
            flow.append(row)
            print(row)
    return flow


if __name__ == '__main__':
    p = ProducerThread(name='enqueue')
    c = ConsumerThread(name='dequeue')
    i = 0
    flow = []

    choice = input('Enter \n1. for simple flow \n2. for complex flow: \n\t')
    flow = read_csvfile(choice)
    #Get input from user
    #generate priority based on flow size
    priority_list = generate_priority(flow)

    #generate list of packets of random sizes
    input_string = generate_packet_list(priority_list)

    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
    # ConsumerThread.join(self=)
    # ProducerThread.join()
    # print("Finished all processes\n")
