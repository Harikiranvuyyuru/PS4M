from engine.itemManager import getNonAggregatorItem
from engine.userManager import getUser
from main import init

init()

user = getUser('Toby')
votes = user.getVotes()

for i, v in enumerate(votes):
    if not v.item.source.isAggregator():
        continue

    new_items = getNonAggregatorItem(v.item, silent=True)
    if new_items != v.item and new_items is not None and not new_items.source.isAggregator():
        print("update ignore votes set id = %s where id = %s;" % (new_items.id, v.item.id))
