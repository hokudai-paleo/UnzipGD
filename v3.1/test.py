import time
from concurrent.futures import ThreadPoolExecutor
from logging import StreamHandler, Formatter, INFO, getLogger


def init_logger():
     handler = StreamHandler()
     handler.setLevel(INFO)
     handler.setFormatter(Formatter("[%(asctime)s] [%(threadName)s] %(message)s"))
     logger = getLogger()
     logger.addHandler(handler)
     logger.setLevel(INFO)


def task(v):
     getLogger().info("%s start", v)
     time.sleep(1.0)
     getLogger().info("%s end", v)
     return v * 2


def main():
     target = [1,1,1,1,1]
     first = True
     n = 0

     init_logger()
     getLogger().info("main start")
     with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
          futures = []
          #for i in range(len(target)):
          while (n != len(target)):
               print(n,len(target))
               if first==True:
                    target.append(20)
                    first = False
               futures.append(executor.submit(task, n))
               n = n + 1
          getLogger().info("submit end")
          getLogger().info([f.result() for f in futures])
     getLogger().info("main end")


if __name__ == "__main__":
     main()    