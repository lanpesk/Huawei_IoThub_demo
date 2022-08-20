# 总览

此代码是用于华为云接入IoT与应用连接的应用demo。完成了查询相关设备属性以及设备指令下法的功能。



# 相关函数：

## 1、GetToken

```python
GetToken(username: str, password: str, domains: str, url: str, scope="cn-north-4")
```

本函数用于获取认证使用的Token，使用的是IMA验证方式，KeystoneCreateUserTokenByPassword API。此方法用于通过IMA账户的用户密码以及IMA拥有者的用户名来获得授权Token。

### 参数

* username: IMA用户名
* password: IMA用户密码
* domains: IMA所属用户的用户名
* url: 相关API的接入点，例如：https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens
* scope: 相关资源属于的大区， 这里默认位 北京四(cn-north-4)

### 返回值

None 或者 str类型的token值

## 2、GetDeviceProperties

```python
GetDeviceProperties(project_id: str, device_id: str, service_id: str, url: str, token: str)
```

本函数用于获取指定设备的最新上报的数据属性。

### 参数

project_id: 项目id，请在“我的凭证”-“API凭证”-“项目列表”中找到对于大区的项目ID值

device_id: 指定设备的id。请在相关控制台获取

service_id: 服务ID。请在指定设备所属的产品详情中获取。

url: 接入IoT的应用API接入点。在接入IoT控制台中，点击“平台接入地址”，查询相关接入地址。例如：https://\****.iotda.cn-north-4.myhuaweicloud.com

token: 鉴权Token

### 返回值

None 或者 调用成功返回的json字符串



## 3、ShowDeviceList

```python
ShowDeviceList(project_id: str, url: str, token)
```

本函数用于查看设备列表。

### 参数

project_id， url， token：  同GetDeviceProperties

### 返回值

None 或者 调用成功返回的json字符串。



## 4、CreateDeviceCommand

```python
CreateDeviceCommand(project_id: str, device_id: str, url: str, token, service_id: str, command_name: str,paras: dict)
```

本函数用于向指定的设备发送指定的命令与参数。

### 参数

project_id, device_id, url, token, service_id: 同GetDeviceProperties

command_name: 下发的指令名称， 相关信息在设备所属的产品信息中。

paras: 下发的相关指令所需的参数。字典形式，例如指令func(value, message)，那么其paras为{"value": 10, "message": "this is message"}

### 返回值

None 或者 调用成功的返回信息。

