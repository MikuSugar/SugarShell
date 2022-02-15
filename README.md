# SugarShell
简易SSH远程连接工具
![QQ20220215-214234-HD](https://cdn.jsdelivr.net/gh/mikusugar/PictureBed@master/uPic/2022/02/QQ20220215-214234-HD.gif)
## 安装&使用

### 前置条件

密码登录功能依赖**sshpass**

### 本地安装

```shell
git clone https://github.com/MikuSugar/SugarShell.git
cd SugarShell
pip install .
#或者
pip3 install .
```

### PiP 安装

```shell
#python版本为3.x
pip install sugar_shell
```



### 使用

执行psh命令

## 配置

使用 **~/.ssh/config**的配置文件

详细参考 https://www.ssh.com/academy/ssh/config

简单例子

```basic
#远程主机名
Host utility01
#远程主机地址
HostName utility01
#用户
User mikusugar
#密钥文件地址
Identityfile ~/.ssh/id_rsa
```

原生的ssh config 文件不支持 密码登录，我们拓展了ssh config 配置文件项

首先需要在文件开头添加

```basic
IgnoreUnknown Password
```

添加这个是让原生的配置检查不至于报错

密码登录例子

```basic
Host testpw
HostName 192.168.xx.xx
User mikusugar
#这里写密码
Password 12345678
```



