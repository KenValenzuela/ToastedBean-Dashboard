-- ====================================
-- 💎 Toasted Bean Clean Warehouse Schema (v2)
-- Includes employee tracking and proper date handling
-- ====================================

-- 🔁 Drop tables to avoid duplicate definitions
DROP TABLE IF EXISTS sales_summary;
DROP TABLE IF EXISTS category_sales;
DROP TABLE IF EXISTS detail_items;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;

-- ========================
-- 🧑‍💼 employees
-- Normalized employee table for joinable metadata
-- ========================
CREATE TABLE employees (
    employee_id   TEXT PRIMARY KEY,
    employee_name TEXT NOT NULL
);
COMMENT ON TABLE employees IS 'Unique list of employees who process transactions.';

-- ========================
-- 👤 customers
-- Customer lookup
-- ========================
CREATE TABLE customers (
    customer_id    TEXT PRIMARY KEY,
    customer_name  TEXT
);

-- ========================
-- 📊 sales_summary
-- Top-level summaries (e.g. Net Sales, Tips, etc.)
-- ========================
CREATE TABLE sales_summary (
    sales_type     TEXT NOT NULL CHECK (sales_type IN ('Sale', 'Tip', 'Discount', 'Tax', 'Refund', 'Other')),
    start_date     DATE NOT NULL,
    end_date       DATE NOT NULL,
    amount         NUMERIC(10,2) NOT NULL CHECK (amount >= 0)
);
COMMENT ON TABLE sales_summary IS 'Aggregate Square summary metrics by sales_type over a date range.';

-- ========================
-- 📈 category_sales
-- Daily revenue by category
-- ========================
CREATE TABLE category_sales (
    category       TEXT NOT NULL,
    date           DATE NOT NULL,
    revenue        NUMERIC(10,2) NOT NULL CHECK (revenue >= 0)
);

-- ========================
-- 🧾 detail_items
-- Item-level POS detail w/ employee tracking
-- ========================
CREATE TABLE detail_items (
    transaction_id     TEXT NOT NULL,
    item               TEXT NOT NULL,
    category           TEXT,
    date               DATE NOT NULL,
    time               TIME,
    gross_sales        NUMERIC(10,2) NOT NULL CHECK (gross_sales >= 0),
    discounts          NUMERIC(10,2) DEFAULT 0 CHECK (discounts >= 0),
    refunds            NUMERIC(10,2) DEFAULT 0 CHECK (refunds >= 0),
    modifiers_applied  TEXT, -- Consider normalizing (see below)
    channel            TEXT,  -- e.g., 'Window', 'Preorder'
    card_brand         TEXT,
    employee_id        TEXT,
    employee_name      TEXT,  -- Optionally denormalize for quick visual use
    customer_id        TEXT,
    customer_name      TEXT,
    datetime           TIMESTAMP GENERATED ALWAYS AS ((date + time)::timestamp) STORED
);
COMMENT ON TABLE detail_items IS 'Granular transaction-level sales data with employee and customer context.';

-- ========================
-- OPTIONAL: Normalized modifier table for advanced analytics
-- ========================
-- UNNEST(modifiers_applied) could populate this with item link
-- CREATE TABLE modifiers (
--     modifier_id SERIAL PRIMARY KEY,
--     transaction_id TEXT,
--     modifier_name TEXT NOT NULL
-- );
-- COMMENT ON TABLE modifiers IS 'Exploded view of modifiers from orders for lift and attach rate analysis.';

-- Indexes for fast query time
CREATE INDEX idx_detail_items_datetime ON detail_items(datetime);
CREATE INDEX idx_detail_items_transaction_id ON detail_items(transaction_id);
CREATE INDEX idx_detail_items_employee_id ON detail_items(employee_id);
