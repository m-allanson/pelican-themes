drop table if exists themes CASCADE;
drop table if exists screenshots CASCADE;

create table themes (
  id serial primary key,
  name text not null,
  sha text not null,
  user_name text not null,
  repo text not null,
  path text not null,
  html_url text not null
);

create table screenshots (
  id serial primary key,
  theme_id integer,
  url text,
  FOREIGN KEY(theme_id) REFERENCES themes(id)
);

-- select themes.id, themes.text, themes.title, screenshots.url
-- FROM themes, screenshots
-- WHERE screenshots.theme_id = themes.id
-- GROUP BY themes.id