from snippets.models import Stock, FriendList, Client, StockList

test_user = Client(name="Job")
test_user2 = Client(name="Elijah")
test_user.save()
test_user2.save()

jlist = FriendList(owner=test_user)
jlist.save()
jlist.friends.add(test_user2)

jstocks = StockList(sl_owner=test_user)
jstocks.save()


stock = Stock(name="MSQ",price="124.12")
stock.save()
jstocks.stocks.add(stock)



