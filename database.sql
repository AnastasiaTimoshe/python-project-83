Drop table if exists url_checks;

drop table if exists urls;

create table urls(
    id bigint primary key generated always as identity,
    name VARCHAR(255) unique,
    created_at timestamp default now()
);

create table "urls_checks"(
    id bigint primary key generated always as identity,
    "url_id" int8,
    "status_code" int4,
    "h1" varchar(512),
    "title" varchar(512),
    "description" varchar(512),
    "created_at" timestamp DEFAULT now()
    CONSTRAINT "urls_checks_url_id_key"
        FOREIGN KEY ("url_id")
            REFERENCES "urls"("id")
);