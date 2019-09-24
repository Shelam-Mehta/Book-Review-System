import time
from concurrent.futures import ThreadPoolExecutor
s=time.time()
from multiprocessing import Pool
def parse(a):
    print(a)
    return 5

if(__name__=='__main__'):
    p = Pool()  # Pool tells how many at a time
    cars_links=[0]*(10**6)
    records = p.map(parse, cars_links)
    p.close()
    p.join()

    # with ThreadPoolExecutor(max_workers = 3) as executor:
    #       results = executor.map(parse, cars_links)
    e=time.time()
    print(e-s)