CREATE TABLE tb_daily_stocks (
    nm_symbol VARCHAR(10) NOT NULL,
    dt_reference DATE NOT NULL,
    vl_open NUMERIC(10, 4) NOT NULL,
    vl_high NUMERIC(10, 4) NOT NULL,
    vl_low NUMERIC(10, 4) NOT NULL,
    vl_close NUMERIC(10, 4) NOT NULL,
    qt_volume INTEGER NOT NULL,
    PRIMARY KEY (nm_symbol, dt_reference),
    CONSTRAINT unique_symbol_date UNIQUE (nm_symbol, dt_reference)
);