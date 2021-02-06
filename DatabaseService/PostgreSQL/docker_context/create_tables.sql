rollback;

create table if not exists users (
    user_id varchar(255) primary key
);

create table if not exists account_balances (
    user_id varchar(255) primary key,
    account_balance real,
    account_reserve real,
    foreign key (user_id) references users(user_id)
        on delete cascade
        on update cascade,
    constraint non_neg_balance check(account_balance >= 0),
    constraint non_neg_reserve check(account_reserve >= 0)
);

create table if not exists stock_balances (
    user_id varchar(255),
    stock_id varchar(255),
    stock_balance integer,
    stock_reserve integer,
    foreign key (user_id) references users(user_id)
        on delete cascade
        on update cascade,
    primary key (user_id, stock_id),
    constraint non_neg_balance check(stock_balance >= 0),
    constraint non_neg_reserve check(stock_reserve >= 0)
);