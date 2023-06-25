
drop table user_cocktail;
drop table user_liquor;
drop table cocktail_liquor;
drop table cocktail;
drop table liquor;
drop table user;


create table user(
    id int not null,
    username varchar(255) not null,
    primary key (id)
);

create table liquor(
    id int not null,
    name varchar(255) not null,
    img_src varchar(255) not null,
    primary key (id)
);

create table user_liquor(
    id int not null,
    user_id int not null,
    liquor_id int not null,
    primary key (id),
    foreign key (user_id) references user(id),
    foreign key (liquor_id) references liquor(id)
);

create table cocktail(
    id int not null,
    name varchar(255) not null,
    desc varchar(255) not null,
    img_src varchar(255),
    primary key (id)
);

create table cocktail_liquor(
    id int not null,
    cocktail_id int not null,
    liquor_id int not null,
    primary key (id),
    foreign key (cocktail_id) references cocktail(id),
    foreign key (liquor_id) references liquor(id)
);

create table user_cocktail(
    id int not null,
    user_id int not null,
    cocktail_id int not null,
    rating int not null,
    primary key (id),
    foreign key (user_id) references user(id),
    foreign key (cocktail_id) references cocktail(id)
);


-- Insert statements for table 'user'
INSERT INTO user (id, username)
VALUES (1, 'JohnDoe');

INSERT INTO user (id, username)
VALUES (2, 'JaneSmith');

INSERT INTO user (id, username)
VALUES (3, 'MikeJohnson');


-- Insert statements for table 'liquor'
INSERT INTO liquor (id, name, img_src)
VALUES (1, 'Whiskey', 'images/whiskey.jpeg');

INSERT INTO liquor (id, name, img_src)
VALUES (2, 'Vodka', 'images/vodka1.jpeg');

INSERT INTO liquor (id, name, img_src)
VALUES (3, 'Rum', 'images/rum.webp');

INSERT INTO liquor (id, name, img_src)
VALUES (4, 'Gin',  'images/Gin.jpeg');

INSERT INTO liquor (id, name, img_src)
VALUES (5, 'Tequila', 'images/teq1.jpeg');

-- Insert statements for table 'user_liquor'
INSERT INTO user_liquor (id, user_id, liquor_id)
VALUES (1, 1, 1);

INSERT INTO user_liquor (id, user_id, liquor_id)
VALUES (2, 1, 2);

INSERT INTO user_liquor (id, user_id, liquor_id)
VALUES (3, 2, 3);

INSERT INTO user_liquor (id, user_id, liquor_id)
VALUES (4, 2, 4);

INSERT INTO user_liquor (id, user_id, liquor_id)
VALUES (5, 3, 5);

-- Insert statements for table 'cocktail'
INSERT INTO cocktail (id, name, desc, img_src)
VALUES (1, 'Old Fashioned', 'Classic whiskey cocktail', 'images/old_fashion.jpeg');

INSERT INTO cocktail (id, name, desc, img_src)
VALUES (2, 'Cosmopolitan', 'Vodka-based cocktail', 'images/cosmopolitan.webp');

INSERT INTO cocktail (id, name, desc, img_src)
VALUES (3, 'Mojito', 'Refreshing rum cocktail', 'images/Mojito.webp');

INSERT INTO cocktail (id, name, desc, img_src)
VALUES (4, 'Gin and Tonic', 'Classic gin cocktail', 'images/gintonic.jpeg');

INSERT INTO cocktail (id, name, desc, img_src)
VALUES (5, 'Margarita', 'Tequila-based cocktail', 'images/marg.jpeg');

-- Insert statements for table 'cocktail_liquor'
INSERT INTO cocktail_liquor (id, cocktail_id, liquor_id)
VALUES (1, 1, 1);

INSERT INTO cocktail_liquor (id, cocktail_id, liquor_id)
VALUES (2, 2, 2);

INSERT INTO cocktail_liquor (id, cocktail_id, liquor_id)
VALUES (3, 2, 4);

INSERT INTO cocktail_liquor (id, cocktail_id, liquor_id)
VALUES (4, 3, 3);

INSERT INTO cocktail_liquor (id, cocktail_id, liquor_id)
VALUES (5, 4, 4);

INSERT INTO cocktail_liquor (id, cocktail_id, liquor_id)
VALUES (6, 5, 5);

-- Insert statements for table 'user_cocktail'
INSERT INTO user_cocktail (id, user_id, cocktail_id, rating)
VALUES (1, 1, 1, 5);

INSERT INTO user_cocktail (id, user_id, cocktail_id, rating)
VALUES (2, 1, 2, 5);

INSERT INTO user_cocktail (id, user_id, cocktail_id, rating)
VALUES (3, 2, 3, 5);

INSERT INTO user_cocktail (id, user_id, cocktail_id, rating)
VALUES (4, 2, 4, 5);

INSERT INTO user_cocktail (id, user_id, cocktail_id, rating)
VALUES (5, 3, 5, 5);

INSERT INTO user_cocktail (id, user_id, cocktail_id, rating)
VALUES (6, 1, 5, 1);


