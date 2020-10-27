DROP TABLE IF exists `etlprojectdb`.`companies`;

CREATE TABLE companies (
    id INT SERIAL DEFAULT VALUE,
    comp_tick VARCHAR(5) PRIMARY KEY,
    comp_name TEXT,
    sect_id INT,
    sect_name TEXT,
    sub_sect_id VARCHAR(55),
    first_trade_date DATE
);
    
SELECT 
    *
FROM
    companies;

DROP TABLE IF exists `etlprojectdb`.`sub_sectors`;

CREATE TABLE sub_sectors (
    id SERIAL,
    sub_sect_id VARCHAR(55),
    sect_id INT,
    sect_name TEXT,
    sub_sect_name TEXT
);
  
  
-- alter table sub_sec-- tors ADD FOREIGN KEY (sub_sect_id) REFERENCES companies (sub_sect_id);

SELECT 
    *
FROM
    sub_sectors;
    
DROP TABLE IF exists  `etlprojectdb`.`price`;


CREATE TABLE price (
    id SERIAL,
    comp_tick VARCHAR(5),
    FOREIGN KEY (comp_tick)
        REFERENCES companies (comp_tick),
    date DATE,
    close_price FLOAT,
    volume FLOAT,
    currency TEXT
);

SELECT 
    *
FROM
    price;