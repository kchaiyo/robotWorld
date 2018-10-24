import random
def update():
    actions = ['TL','TR','G','G']
    queue = []
    queue.append(random.choice(actions))
    return queue