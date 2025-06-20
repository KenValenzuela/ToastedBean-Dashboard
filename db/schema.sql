-- 🧾 Category-level sales summary (pivoted → melted from Square exports)
DROP TABLE IF EXISTS category_sales;
CREATE TABLE category_sales (
    category     TEXT NOT NULL,
    date_range   TEXT NOT NULL,
    revenue      NUMERIC NOT NULL CHECK (revenue >= 0)
);

-- 📊 Summary of high-level sales metrics (Net Sales, Discounts, Tax, etc.)
DROP TABLE IF EXISTS sales_summary;
CREATE TABLE sales_summary (
    sales_type   TEXT NOT NULL,
    date_range   TEXT NOT NULL,
    amount       NUMERIC NOT NULL
);

-- 🧩 Item-level sales detail from Square POS exports
DROP TABLE IF EXISTS detail_items;
CREATE TABLE detail_items (
    item               TEXT NOT NULL,
    category           TEXT,
    date               DATE NOT NULL,
    time               TIME,
    gross_sales        NUMERIC NOT NULL CHECK (gross_sales >= 0),
    discounts          NUMERIC DEFAULT 0 CHECK (discounts >= 0),
    refunds            NUMERIC DEFAULT 0 CHECK (refunds >= 0),
    modifiers_applied  TEXT,
    channel            TEXT,
    card_brand         TEXT,
    transaction_id     TEXT,
    customer_id        TEXT,
    customer_name      TEXT,
    datetime           TIMESTAMP GENERATED ALWAYS AS ((date + time)::timestamp) STORED
);

-- 👤 Customer lookup table
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT
);
