drop table if exists themes;
drop table if exists screenshots;

create table themes (
  id integer primary key autoincrement,
  name text not null,
  sha text not null,
  user text not null,
  repo text not null,
  path text not null,
  html_url text not null
);

create table screenshots (
  id integer primary key autoincrement,
  theme_id integer,
  url text,
  FOREIGN KEY(theme_id) REFERENCES themes(id)
);

-- select themes.id, themes.text, themes.title, screenshots.url
-- FROM themes, screenshots
-- WHERE screenshots.theme_id = themes.id
-- GROUP BY themes.id