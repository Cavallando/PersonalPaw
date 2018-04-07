drop table if exists menus;
create table menus (
  id integer primary key autoincrement,
  menu_date text not null,
  dining_commons text not null,
  menu text not null,
  food_items text null
);