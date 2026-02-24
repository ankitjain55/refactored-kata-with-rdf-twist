import pytest
from gilded_rose import Item, GildedRose

@pytest.mark.parametrize("name, sell_in, quality, expected_sell_in, expected_quality", [
# 1. Standard Items
("+5 Dexterity Vest", 10, 20, 9, 19),
("+5 Dexterity Vest", 0, 20, -1, 18), # Degrades double after expiration
("+5 Dexterity Vest", 5, 0, 4, 0),# Never negative

# 2. Aged Brie
("Aged Brie", 2, 0, 1, 1),
("Aged Brie", 0, 10, -1, 12), # Increases double after expiration
("Aged Brie", 5, 50, 4, 50), # Max 50

# 3. Sulfuras
("Sulfuras, Hand of Ragnaros", 0, 80, 0, 80),
("Sulfuras, Hand of Ragnaros", -1, 80, -1, 80),

# 4. Backstage Passes
("Backstage passes to a TAFKAL80ETC concert", 15, 20, 14, 21),
("Backstage passes to a TAFKAL80ETC concert", 10, 20, 9, 22), # +2 when <= 10 days
("Backstage passes to a TAFKAL80ETC concert", 5, 20, 4, 23), # +3 when <= 5 days
("Backstage passes to a TAFKAL80ETC concert", 0, 20, -1, 0), # 0 after concert

# 5. Conjured Items
("Conjured Mana Cake", 3, 6, 2, 4),  # Degrades by 2
("Conjured Mana Cake", 0, 6, -1, 2), # Degrades by 4 after expiration
])

def test_update_quality(name, sell_in, quality, expected_sell_in, expected_quality):
    items = [Item(name, sell_in, quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    assert items[0].sell_in == expected_sell_in
    assert items[0].quality == expected_quality
