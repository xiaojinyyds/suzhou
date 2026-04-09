create table if not exists desserts
(
    id           int auto_increment
        primary key,
    name         varchar(100)                         not null comment '甜品名称',
    price        decimal(10, 2)                       not null comment '价格',
    description  text                                 null comment '甜品描述',
    ingredients  text                                 null comment '配料信息',
    calories     int                                  null comment '热量(卡路里)',
    image_url    varchar(500)                         null comment '甜品图片URL',
    category     varchar(50)                          null comment '分类',
    stock        int        default 0                 null comment '库存数量',
    is_available tinyint(1) default 1                 null comment '是否可售',
    created_at   timestamp  default CURRENT_TIMESTAMP null comment '创建时间',
    updated_at   timestamp  default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '更新时间'
)
    comment '甜品表' collate = utf8mb4_unicode_ci;

create index idx_category
    on desserts (category);

create index idx_desserts_available
    on desserts (is_available, stock);

create index idx_name
    on desserts (name);

create index idx_price
    on desserts (price);

create table if not exists statues
(
    id             int auto_increment
        primary key,
    name           varchar(100)                         not null comment '景点名称',
    latitude       decimal(10, 8)                       not null comment '纬度',
    longitude      decimal(11, 8)                       not null comment '经度',
    check_radius   int        default 100               null comment '打卡半径(米)',
    description    text                                 null comment '景点介绍',
    history        text                                 null comment '历史背景',
    cultural_value text                                 null comment '文化价值',
    image_url      varchar(500)                         null comment '景点图片URL',
    is_active      tinyint(1) default 1                 null comment '是否启用',
    created_at     timestamp  default CURRENT_TIMESTAMP null comment '创建时间',
    updated_at     timestamp  default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '更新时间'
)
    comment '石像景点表' collate = utf8mb4_unicode_ci;

create index idx_location
    on statues (latitude, longitude);

create index idx_name
    on statues (name);

create table if not exists users
(
    id            int auto_increment
        primary key,
    username      varchar(50)                            not null comment '用户名',
    email         varchar(100)                           not null comment '邮箱',
    password_hash varchar(255)                           not null comment '密码哈希',
    nickname      varchar(50)                            null comment '昵称',
    avatar_url    varchar(500)                           null comment '头像URL',
    phone         varchar(20)                            null comment '手机号',
    is_active     tinyint(1)   default 1                 null comment '是否激活',
    is_verified   tinyint(1)   default 0                 not null comment '是否验证',
    created_at    timestamp    default CURRENT_TIMESTAMP null comment '创建时间',
    updated_at    timestamp    default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '更新时间',
    role          varchar(255) default 'user'            null comment '角色（admin,user）',
    constraint email
        unique (email),
    constraint username
        unique (username)
)
    comment '用户表' collate = utf8mb4_unicode_ci;

create table if not exists check_ins
(
    id              int auto_increment
        primary key,
    user_id         int                                  not null comment '用户ID',
    statue_id       int                                  not null comment '景点ID',
    check_latitude  decimal(10, 8)                       not null comment '打卡纬度',
    check_longitude decimal(11, 8)                       not null comment '打卡经度',
    distance        decimal(8, 2)                        null comment '距离景点距离(米)',
    ip_address      varchar(45)                          null comment 'IP地址',
    device_info     varchar(500)                         null comment '设备信息',
    is_valid        tinyint(1) default 1                 null comment '是否有效打卡',
    created_at      timestamp  default CURRENT_TIMESTAMP null comment '打卡时间',
    check_date      date as (cast(`created_at` as date)) stored,
    constraint uk_user_statue_day
        unique (user_id, statue_id, check_date),
    constraint check_ins_ibfk_1
        foreign key (user_id) references users (id)
            on delete cascade,
    constraint check_ins_ibfk_2
        foreign key (statue_id) references statues (id)
            on delete cascade
)
    comment '打卡记录表' collate = utf8mb4_unicode_ci;

create index idx_checkins_user_statue
    on check_ins (user_id, statue_id);

create index idx_created_at
    on check_ins (created_at);

create index idx_statue_id
    on check_ins (statue_id);

create index idx_user_id
    on check_ins (user_id);

create table if not exists orders
(
    id               int auto_increment
        primary key,
    order_no         varchar(32)                                                                                             not null comment '订单号',
    user_id          int                                                                                                     not null comment '用户ID',
    total_amount     decimal(10, 2)                                                                                          not null comment '订单总金额',
    discount_amount  decimal(10, 2)                                                                default 0.00              null comment '优惠金额',
    delivery_fee     decimal(10, 2)                                                                default 0.00              null comment '配送费',
    final_amount     decimal(10, 2)                                                                                          not null comment '实付金额',
    status           enum ('pending', 'paid', 'preparing', 'delivering', 'completed', 'cancelled') default 'pending'         null comment '订单状态',
    payment_method   varchar(50)                                                                                             null comment '支付方式',
    payment_time     timestamp                                                                                               null comment '支付时间',
    delivery_address json                                                                                                    null comment '配送地址',
    remark           text                                                                                                    null comment '订单备注',
    created_at       timestamp                                                                     default CURRENT_TIMESTAMP null comment '创建时间',
    updated_at       timestamp                                                                     default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '更新时间',
    constraint order_no
        unique (order_no),
    constraint orders_ibfk_1
        foreign key (user_id) references users (id)
            on delete cascade
)
    comment '订单表' collate = utf8mb4_unicode_ci;

create table if not exists order_items
(
    id          int auto_increment
        primary key,
    order_id    int                                 not null comment '订单ID',
    dessert_id  int                                 not null comment '甜品ID',
    quantity    int                                 not null comment '数量',
    unit_price  decimal(10, 2)                      not null comment '单价',
    total_price decimal(10, 2)                      not null comment '小计',
    created_at  timestamp default CURRENT_TIMESTAMP null comment '创建时间',
    constraint order_items_ibfk_1
        foreign key (order_id) references orders (id)
            on delete cascade,
    constraint order_items_ibfk_2
        foreign key (dessert_id) references desserts (id)
            on delete cascade
)
    comment '订单明细表' collate = utf8mb4_unicode_ci;

create index idx_dessert_id
    on order_items (dessert_id);

create index idx_order_id
    on order_items (order_id);

create index idx_created_at
    on orders (created_at);

create index idx_order_no
    on orders (order_no);

create index idx_orders_user_status
    on orders (user_id, status);

create index idx_status
    on orders (status);

create index idx_user_id
    on orders (user_id);

create table if not exists photos
(
    id              int auto_increment
        primary key,
    user_id         int                                 not null comment '用户ID',
    image_url       varchar(500)                        not null comment '图片URL',
    thumbnail_url   varchar(500)                        null comment '缩略图URL',
    decoration_type varchar(50)                         null comment '装饰类型',
    file_size       int                                 null comment '文件大小(字节)',
    width           int                                 null comment '图片宽度',
    height          int                                 null comment '图片高度',
    created_at      timestamp default CURRENT_TIMESTAMP null comment '创建时间',
    constraint photos_ibfk_1
        foreign key (user_id) references users (id)
            on delete cascade
)
    comment '拍照记录表' collate = utf8mb4_unicode_ci;

create index idx_created_at
    on photos (created_at);

create index idx_user_id
    on photos (user_id);

create index idx_email
    on users (email);

create index idx_username
    on users (username);

