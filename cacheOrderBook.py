from omnidex import getOrderbook
import redis, json

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def updateOrderbookCache():
  while True:
    time.sleep(20)
    print "Checking for orderbook updates"
    try:
      lasttrade = r.get("omniwallet:omnidex:lasttrade")
      if lasttrade == None:
        lasttrade=0

      lastpending = r.get("omniwallet:omnidex:lastpending")
      if lastpending == None:
        lastpending = 0

      ret = getOrderbook(lasttrade,lastpending)
      if ret['updated']:
        print "Orderbook cache updated. Lasttrade: "+str(lasttrade)+" Lastpending: "+str(lastpending)
        r.set("omniwallet:omnidex:lasttrade",ret['lasttrade'])
        r.set("omniwallet:omnidex:lastpending",ret['lastpending'])
        r.set("omniwallet:omnidex:book",json.dumps(ret['book']))
    except Exception as e:
      print "Error updating orderbook cache "+str(e)

  
def main():
  updateOrderbookCache()


if __name__ == "__main__":main() ## with if
  