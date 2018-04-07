drop table if exists menus;
create table menus (
  id INT NOT NULL AUTO_INCREMENT, 
  menu_date VARCHAR(10) NOT NULL ,
  dining_commons VARCHAR(30) NOT NULL,
  menu VARCHAR(10) NOT NULL,
  food_items TEXT,
  PRIMARY KEY(id));