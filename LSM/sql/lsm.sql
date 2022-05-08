/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/10/25 23:21:30                          */
/*==============================================================*/


drop database labsoftwaremanager;
create database labsoftwaremanager;
use labsoftwaremanager;

/*==============================================================*/
/* Table: account                                               */
/*==============================================================*/
create table account
(
   account_id           int not null auto_increment,
   teacher_id           int not null,
   account_password     text not null,
   account_priviledge   int not null default 0,
   account_name         char(20) not null,
   primary key (account_id)
);

/*==============================================================*/
/* Table: category                                              */
/*==============================================================*/
create table category
(
   category_id          int not null auto_increment,
   category_name        char(20) not null,
   primary key (category_id)
);

/*==============================================================*/
/* Table: computer                                              */
/*==============================================================*/
create table computer
(
   computer_id          int not null auto_increment,
   computer_model       char(20) not null,
   computer_memory      int not null,
   computer_cpu         char(20) not null,
   computer_gpu         char(20) not null,
   computer_disk        int not null,
   computer_disk_used   int not null,
   computer_os1         char(20) not null,
   computer_os2         char(20),
   primary key (computer_id)
);

/*==============================================================*/
/* Table: department                                            */
/*==============================================================*/
create table department
(
   department_id        int not null auto_increment,
   department_name      char(20) not null,
   primary key (department_id)
);

/*==============================================================*/
/* Table: lectures                                              */
/*==============================================================*/
create table lectures
(
   lectures_id          int not null auto_increment,
   department_id        int not null,
   lectures_name        char(20) not null,
   lectures_teacher     char(100) not null,
   lectures_hours       int not null,
   lectures_total_num   int not null,
   lectures_class_num   int not null,
   lectures_semester    char(20) not null,
   lectures_notes       varchar(100),
   primary key (lectures_id)
);

/*==============================================================*/
/* Table: lectures_room                                         */
/*==============================================================*/
create table lectures_room
(
   room_id              int not null,
   lectures_id          int not null,
   primary key (room_id, lectures_id)
);

/*==============================================================*/
/* Table: lectures_teacher                                      */
/*==============================================================*/
create table lectures_teacher
(
   lectures_id          int not null,
   teacher_id           int not null,
   primary key (lectures_id, teacher_id)
);

/*==============================================================*/
/* Table: room                                                  */
/*==============================================================*/
create table room
(
   room_id              int not null auto_increment,
   computer_id          int,
   account_id           int not null,
   room_name            char(20),
   room_location        char(20) not null,
   room_capacity        int not null,
   room_notes           varchar(100),
   primary key (room_id)
);

/*==============================================================*/
/* Table: softwares                                              */
/*==============================================================*/
create table software
(
   category_id          int not null,
   software_id          int not null auto_increment,
   software_name        char(20) not null,
   software_description varchar(100),
   software_configuration varchar(100),
   software_notes       varchar(100),
   primary key (software_id)
);

/*==============================================================*/
/* Table: software_room                                         */
/*==============================================================*/
create table software_room
(
   category_id          int not null,
   software_id          int not null,
   room_id              int not null,
   primary key (category_id, software_id, room_id)
);

/*==============================================================*/
/* Table: teacher                                               */
/*==============================================================*/
create table teacher
(
   teacher_id           int not null auto_increment,
   account_id           int,
   teacher_name         char(20) not null,
   teacher_phone        char(11),
   primary key (teacher_id)
);

/*==============================================================*/
/* Table: unload_log                                            */
/*==============================================================*/
create table unload_log
(
   category_id          int not null,
   software_id          int not null,
   room_id              int not null,
   account_id           int not null,
   user_name            char(20) not null,
   unload_id            int not null auto_increment,
   unload_time          datetime not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   primary key (unload_id)
);

/*==============================================================*/
/* Table: update_log                                            */
/*==============================================================*/
create table update_log
(
   category_id          int not null,
   software_id          int not null,
   room_id              int not null,
   account_id           int not null,
   user_name            char(20) not null,
   update_id            int not null auto_increment,
   update_time          datetime not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   primary key (update_id)
);

alter table account add constraint FK_user_teacher foreign key (teacher_id)
      references teacher (teacher_id) on delete restrict on update restrict;

alter table lectures add constraint FK_lectures_department foreign key (department_id)
      references department (department_id) on delete restrict on update restrict;

alter table lectures_room add constraint FK_lectures_room foreign key (room_id)
      references room (room_id) on delete restrict on update restrict;

alter table lectures_room add constraint FK_lectures_room1 foreign key (lectures_id)
      references lectures (lectures_id) on delete restrict on update restrict;

alter table lectures_teacher add constraint FK_lectures_teacher foreign key (teacher_id)
      references teacher (teacher_id) on delete restrict on update restrict;

alter table lectures_teacher add constraint FK_lectures_teacher1 foreign key (lectures_id)
      references lectures (lectures_id) on delete restrict on update restrict;

alter table room add constraint FK_administrator foreign key (account_id)
      references account (account_id) on delete restrict on update restrict;

alter table room add constraint FK_room_computer foreign key (computer_id)
      references computer (computer_id) on delete restrict on update restrict;

alter table software add constraint FK_software_category foreign key (category_id)
      references category (category_id) on delete restrict on update restrict;

alter table software_room add constraint FK_software_room foreign key (software_id)
      references software (software_id) on delete restrict on update restrict;

alter table software_room add constraint FK_software_room1 foreign key (room_id)
      references room (room_id) on delete restrict on update restrict;

alter table teacher add constraint FK_teacher_user foreign key (account_id)
      references account (account_id) on delete restrict on update restrict;

alter table unload_log add constraint FK_unload_log foreign key (software_id)
      references software (software_id) on delete restrict on update restrict;

alter table unload_log add constraint FK_unload_log1 foreign key (account_id)
      references account (account_id) on delete restrict on update restrict;

alter table unload_log add constraint FK_unload_log2 foreign key (room_id)
      references room (room_id) on delete restrict on update restrict;

alter table update_log add constraint FK_update_log foreign key (software_id)
      references software (software_id) on delete restrict on update restrict;

alter table update_log add constraint FK_update_log1 foreign key (account_id)
      references account (account_id) on delete restrict on update restrict;

alter table update_log add constraint FK_update_log2 foreign key (room_id)
      references room (room_id) on delete restrict on update restrict;
