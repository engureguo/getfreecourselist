# getfreecourselist
Get freecourse list when I select course in the university from our school‘s course selection system.

#### 思路
1. POST方式下请求 json 【requests库，需要配置 headers 和 data】
2. 解析数据，发送想要的邮箱 【使用 qq 的 smtp服务】

#### version
1. `select` 需要 kch.txt 和 email.txt 提供课程号和邮箱号，只根据课程号查找信息
2. `select.2` kch、kcm、email、cookie、seesion相关信息都放在 `getinfo.txt`中(smtp的密钥没放，忘记辽)，kcm使用子串匹配提取数据

#### 说明
1. `testlongestconn` 类似`心跳检测`，保证连接alive
2. linux下 **永久挂起** : `nohup python3 getdatabypost.py &`
