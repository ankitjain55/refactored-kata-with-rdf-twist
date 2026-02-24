# -*- coding: utf-8 -*-
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
import os

GR = Namespace("http://example.org/gilded-rose#")
INST = Namespace("http://example.org/gilded-rose/items/")

class RDFItemStore:
    def __init__(self):
        self.graph = Graph()
        self.graph.bind("gr", GR)
        self._load_schema()

    def _load_schema(self):
        #Load schema.ttl
        schema_path = "schema.ttl"
        if os.path.exists(schema_path):
            self.graph.parse(schema_path, format="turtle")

    def item_to_rdf(self, item, item_id: int) -> URIRef:
        #Extracts data from Item class into RDF triples.
        item_uri = INST[f"item_{item_id}"]

        self.graph.add((item_uri, RDF.type, GR.Item))
        self.graph.add((item_uri, GR.name, Literal(item.name)))
        self.graph.add((item_uri, GR.sellIn, Literal(item.sell_in, datatype=XSD.integer)))
        self.graph.add((item_uri, GR.quality, Literal(item.quality, datatype=XSD.integer)))

        #Link the item to its semantic type for logic processing
        self.graph.add((item_uri, GR.itemType, self._determine_item_type(item.name)))
        return item_uri

    def rdf_to_item(self, item_uri: URIRef, item):
        #Syncs the processed RDF values back into the legacy Item object.
        item.sell_in = int(self.graph.value(item_uri, GR.sellIn))
        item.quality = int(self.graph.value(item_uri, GR.quality))

    def update_quality(self):
        query = """
        SELECT ?uri ?type ?sellIn ?quality
        WHERE {
            ?uri rdf:type gr:Item ;
                 gr:itemType ?type ;
                 gr:sellIn ?sellIn ;
                 gr:quality ?quality .
        }
        """
        for row in self.graph.query(query):
            uri, itype, sell_in, quality = row
            s, q = int(sell_in), int(quality)

            # --- Business Logic ---
            if itype != GR.Sulfuras:
                s -= 1

            if itype == GR.AgedBrie:
                q = q + 1 if s >= 0 else q + 2
            elif itype == GR.BackstagePass:
                if s < 0:
                    q = 0
                elif s < 5:
                    q += 3
                elif s < 10:
                    q += 2
                else:
                    q += 1
            elif itype == GR.ConjuredItem:
                q = q - 2 if s >= 0 else q - 4
            elif itype != GR.Sulfuras: #Normal Items
                q = q - 1 if s >= 0 else q - 2

            #Enforce bounds (Sulfuras is always 80)
            if itype != GR.Sulfuras:
                q = max(0, min(50, q))

            #Update the Triple Store
            self.graph.set((uri, GR.sellIn, Literal(s, datatype=XSD.integer)))
            self.graph.set((uri, GR.quality, Literal(q, datatype=XSD.integer)))

    def _determine_item_type(self, name: str) -> URIRef:
        n = name.lower()
        if "aged brie" in n:
            return GR.AgedBrie
        if "sulfuras" in n:
            return GR.Sulfuras
        if "backstage passes" in n:
            return GR.BackstagePass
        if "conjured" in n:
            return GR.ConjuredItem
        return GR.NormalItem
