from app.geo.normalization import canonical_location_key, normalize_address_text


def test_arabic_normalization_removes_variants_and_digits():
    assert canonical_location_key("  مـدِينَتِي  ") == "مدينتي"
    assert canonical_location_key("مدينتى") == "مدينتي"
    assert normalize_address_text("المرحلة ٣، القاهرة") == "المرحله 3 القاهره"


def test_english_and_franco_aliases_collapse_to_canonical_keys():
    assert canonical_location_key("Madinaty") == "مدينتي"
    assert canonical_location_key("Madinty") == "مدينتي"
    assert canonical_location_key("sheikh-zayed") == "الشيخ زايد"
    assert canonical_location_key("zayed") == "الشيخ زايد"
    assert canonical_location_key("tagamo3") == "التجمع الخامس"
    assert canonical_location_key("tgamo3") == "التجمع الخامس"
    assert canonical_location_key("fifth settlement") == "التجمع الخامس"
