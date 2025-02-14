# AcgDraw

# 二次元模拟寻访

**提供各种二次元模拟的模拟抽卡API**

## 简介

基于python的模拟抽卡图片合成API，使用了flask以及pillow

## 进度

### 全局
- [ ] Web管理面板

### 明日方舟
- [x] 寻访十连
- [ ] 卡池六星up
- [ ] 卡池五星up
- [ ] 一键更新卡池信息
- [x] 一键更新干员信息
- [ ] 指定卡池寻访
- [x] 定时清理缓存
- [x] 自动更新
- [ ] 单次寻访
- [ ] 自定义卡池
- [ ] ~~寻访记录查询~~

### 原神
- [x] 寻访十连
- [ ] 卡池五星up
- [ ] 一键更新卡池信息
- [ ] 一键更新干员信息
- [ ] 指定卡池寻访
- [x] 定时清理缓存


### 崩坏：星穹铁道
**正在咕咕咕**

### 碧蓝档案
**正在咕咕咕**

### Apex
**正在咕咕咕**

~~一个人做不过来QAQ~~
## 文档

https://baimianxiao.github.io/AcgDraw/

## 开始
该项目基于python3.10开发

### Windows运行

### Linux运行

### 源码运行

### Docker运行
1.在编译镜像之前请手动运行一次init以下载素材。如果data中已经下载好素材了(即已经手动运行成功过)则可以跳过这一步 \
请注意运行init也需要先在本机安装requirements.txt中的依赖
```shell
python3 main.py init # Windows请使用python main.py init
```
2.将conf/global.json中的`"host":"127.0.0.1"`改为`"host":"0.0.0.0"`，因为Docker中的127.0.0.1默认不会监听容器外的地址

3.使用仓库中的Dockerfile构建镜像
```shell
docker build -t acgdraw .
```
4.运行容器(端口可根据您设置的config文件自行调整)
```shell
docker run -d -p 11451:11451 --name=acgdraw acgdraw
```

## 配置文件
### 全局配置文件
位于`根目录/conf/global`

## 协议
GPL-3.0 license

## 其他

- API地址：<http://api.elapsetower.com/arknightsdraw>(目前已失效)

- 感谢[@分子](https://github.com/yigefz)对图片素材的处理

- 感谢[@LTY_CK_TS](https://github.com/sahuidhsu)完善的docker部署

- 感谢[@KQDXBWL](https://github.com/kqdxbwl)的BUG反馈

- 快来和咱一起找bug（指有问题在issue中反馈）
