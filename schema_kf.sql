DROP TABLE IF exists `etlprojectdb`.`sub_sectors`;

CREATE TABLE sub_sectors (
    sect_id INT SERIAL,
    sub_sect_id SERIAL PRIMARY KEY,
    sect_name VARCHAR(50) Not Null,
    sub_sect_name VARCHAR(50) Not Null
);
  
SELECT 
    *
FROM
    sub_sectors;

DROP TABLE IF exists `etlprojectdb`.`companies`;

CREATE TABLE companies (
    id INT SERIAL DEFAULT VALUE,
    comp_tick VARCHAR(5) PRIMARY KEY,
    comp_name VARCHAR(50) Not Null,
    sect_id INT REFERENCES sub_sectors(sect_id),
    sect_name VARCHAR(50) Not Null,
    sub_sect_id VARCHAR(55) REFERENCES sub_sectors(sub_sect_id),
    first_trade_date DATE
);
    
SELECT 
    *
FROM
    companies;


DROP TABLE IF exists  `etlprojectdb`.`price`;


CREATE TABLE price (
    id SERIAL PRIMARY KEY,
    comp_tick VARCHAR(5) REFERENCES companies(comp_tick),
    date DATE,
    close_price FLOAT,
    volume FLOAT,
    currency VARCHAR(3)
);

SELECT 
    *
FROM
    price;
