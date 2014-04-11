HostAdmin
=========

# 功能
 1. 编辑某个文件，如/etc/hosts
 2. 多人同时编辑，如果被覆盖会实时提示是否重新加载
 3. 内容高亮
 4. 所有提供服务节点列表

#依赖
 1. tornado, python-redis
 2. 对要编辑的文件有读写权限

# 配置参数
 1. file_name: 要编辑的文件
 2. server_config: 提供服务的地址
 3. redis用来存储节点列表，请自行修改为能够访问的地址。如果不希望节点被录入，去掉index.py中的发送请求即可
 4. valid_user是验证用户登录
