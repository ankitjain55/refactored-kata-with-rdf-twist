from rdf_store import RDFItemStore


class GildedRose(object):
    def __init__(self, items):
        self.items = items
        self.store = RDFItemStore()
        # Initialize the Graph
        self.uris = [self.store.item_to_rdf(item, i) for i, item in enumerate(items)]

    def update_quality(self):
        # 1. Execute logic on RDF
        self.store.update_quality()

        # 2. Sync RDF results back to Item objects
        for i, item in enumerate(self.items):
            self.store.rdf_to_item(self.uris[i], item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
