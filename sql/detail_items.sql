SELECT
    item,
    category,
    date,
    time,
    gross_sales,
    discounts,
    refunds,
    modifiers_applied,
    channel,
    card_brand,
    (date + time)::timestamp AS datetime  -- <-- include this!
FROM detail_items;
