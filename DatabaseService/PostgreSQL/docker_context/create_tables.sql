rollback;

create table if not exists users (
    user_id varchar(12) primary key
);

create table if not exists account_balances (
    user_id varchar(12) primary key,
    account_balance numeric(12, 2),
    account_reserve numeric(12, 2),
    foreign key (user_id) references users(user_id)
        on delete cascade
        on update cascade,
    constraint non_neg_balance check(account_balance >= 0),
    constraint non_neg_reserve check(account_reserve >= 0)
);

create table if not exists stock_balances (
    user_id varchar(12),
    stock_id varchar(3),
    stock_balance integer,
    stock_reserve integer,
    foreign key (user_id) references users(user_id)
        on delete cascade
        on update cascade,
    primary key (user_id, stock_id),
    constraint non_neg_balance check(stock_balance >= 0),
    constraint non_neg_reserve check(stock_reserve >= 0)
);

 create table if not exists pending_buy_triggers (
     user_id varchar(12),
     stock_id varchar(3),
     stock_amount integer,
     foreign key (user_id) references users(user_id)
         on delete cascade
         on update cascade,
     primary key (user_id, stock_id),
     constraint non_neg_amount check(stock_amount >= 0)
 );

 create table if not exists complete_buy_triggers (
     user_id varchar(12),
     stock_id varchar(3),
     stock_amount integer,
     stock_price numeric(12, 2),
     foreign key (user_id) references users(user_id)
         on delete cascade
         on update cascade,
     primary key (user_id, stock_id),
     constraint non_neg_amount check(stock_amount >= 0),
     constraint non_neg_price check(stock_price >= 0)
 );

 create table if not exists pending_sell_triggers (
     user_id varchar(12),
     stock_id varchar(3),
     stock_amount integer,
     foreign key (user_id) references users(user_id)
         on delete cascade
         on update cascade,
     primary key (user_id, stock_id),
     constraint non_neg_amount check(stock_amount >= 0)
 );

 create table if not exists complete_sell_triggers (
     user_id varchar(12),
     stock_id varchar(3),
     stock_amount integer,
     stock_price numeric(15, 2),
     foreign key (user_id) references users(user_id)
         on delete cascade
         on update cascade,
     primary key (user_id, stock_id),
     constraint non_neg_amount check(stock_amount >= 0),
     constraint non_neg_price check(stock_price >= 0)
 );
