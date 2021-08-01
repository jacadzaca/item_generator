USE world;
SET SQL_SAFE_UPDATES = 0;
CREATE TEMPORARY TABLE tmp SELECT *FROM item_template WHERE entry = {{ template_entry }};

UPDATE tmp SET entry = {{ first_entry - 1 }} WHERE entry = {{ template_entry }};
{% for item in items %}

UPDATE tmp SET entry={{ item.entry }} WHERE entry = {{ item.entry - 1 }};
INSERT INTO item_template SELECT * FROM tmp WHERE entry = {{ item.entry }};
UPDATE item_template SET StatsCount={{ attribute_count }},{% for (i, attribute) in enumerate(item.attributes, start=1) %} stat_type{{ i }}={{ attribute.id }}, stat_value{{ i }}={{ attribute.value }},{% endfor %}name="{{ item.name }}", displayid={{ item.display_id }} WHERE entry = {{ item.entry }};
{% endfor %}

DROP TABLE tmp;
