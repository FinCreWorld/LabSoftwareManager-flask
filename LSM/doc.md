房间设计

页面主体，显示当前的所有房间以及信息

|房间名|位置|容量|电脑信号|管理员|备注|
|:---:|:---:|:---:|:---:|:---:|:---:|

`room_id` 虽然不显示，但是需要存在

支持单个条目修改，但只有当前管理员能够修改。

支持创建房间，自动生成管理员姓名
|房间名|位置|容量|电脑信号|
|:---:|:---:|:---:|:---:|

支持删除房间，但是只能由当前管理员进行操作


教师页

支持教师增加

教师修改

教师权限修改
只有教师权限为 1 时才可以进入教师管理界面
教师权限为 1 可以做任何事，权限为 0 仅可以修改自己拥有的教室，无法修改教师
特权可以授予


软件总表
软件小表 针对每一个房间修改软件，或者修改电脑配置

log 用来记录所有的软件修改记录

课程查看

由于创建教师之后，会产生较多依赖，同时为了便于回溯历史信息，
因此只提供删除无依赖教师的功能

初始设计没有明确需求，对于前端需求没有考量

并不是所有的都要建立对应的互联数据库，有时候建立成文本也是比较好的选择

关于删除部分处理不够优，没有较好的办法

很多地方都不够完善，有很多漏洞

修改与不能修改未能说明