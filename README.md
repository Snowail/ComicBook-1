# ComicBook

漫画爬虫、漫画下载工具，支持腾讯漫画、哔哩哔哩漫画、有妖气漫画、快看漫画、漫画柜等站点

[漫画源收录情况](https://github.com/lossme/ComicBook/projects/1)

尊重版权，请支持正版，通过本工具下载或生成的资源**禁止传播分享！禁止利用本项目进行商业活动！**

## 本项目特点

- [x] 漫画批量下载
- [x] 分目录按章节保存
- [x] 支持多个漫画源，易于扩展
- [x] 支持生成pdf、zip
- [x] 支持发送到邮箱
- [x] 支持设置代理
- [x] 支持API调用 [API-README](API-README.md)
- [x] 支持登录、下载自己账号下已购买的付费资源

## 安装/升级步骤

自己找安装Python的教程

### 方式一（推荐）

```sh
# 在线安装/升级（最新版本）
# 由于网络环境不好导致安装失败 可以搜索关键词尝试解决: github host 修改
python3 -m pip install -U git+https://github.com/Snowail/ComicBook-1

# 查看帮助
python3 -m onepiece --help

# 安装指定版本
python3 -m pip install git+https://github.com/Snowail/ComicBook-1@v0.3.20
```

### 方式二（源码安装）

```sh
# clone项目 或从这里下载最新的代码并解压 https://github.com/lossme/ComicBook/releases
git clone git@github.com:Snowail/ComicBook-1.git
# 切换工作目录
cd ComicBook

# 安装
python3 setup.py clean --all install

# 查看帮助
python3 -m onepiece --help

# 更新并安装至最新版本
git pull && python3 setup.py clean --all install
```

如果在使用过程中，发现问题可以先更新代码再试下，说不定已经修复了。

Star防止失联，欢迎大家提建议和issue，本项目持续更新。

## 常规使用

```sh
# 注意参数里的 - 和 -- 的区别
# 从章节列表页面的URL 下载漫画的最新一集
python3 -m onepiece --url "http://ac.qq.com/Comic/ComicInfo/id/505430"

# 下载漫画 id=505430 最新一集 注意不同站点的漫画id区别
python3 -m onepiece -s qq -id=505430

# 下载所有章节
python3 -m onepiece -s qq -id 505430 --all

# 下载第800集
python3 -m onepiece -s qq -id 505430 -c 800

# 下载倒数第二集
python3 -m onepiece -s qq -id 505430 -c -2

# 下载1到5集,7集，9到10集
python3 -m onepiece -s qq -id 505430 -c 1-5,7,9-10

# 拼接成长图
python3 -m onepiece -s qq -id 505430 --single-image --quality 95 --max-height 20000

# 设置代理
python3 -m onepiece -s qq -id 505430 --proxy "socks5://127.0.0.1:1080"

# 自定义保存目录
python3 -m onepiece -s qq -id=505430 --output MyComicBook

# 将多话合并到单个文件夹和zip文件
python3 -m onepiece -s manhuagui -id 1128 -c 320-322 --merge --merge-zip

# 下载单行本
python3 -m onepiece -s manhuagui -id 1128 --ext-name 单行本 -c -1


# 通过指定的URL文件列表批量下载
# 文件示例: https://github.com/lossme/ComicBook/blob/master/test/test-url-file.txt
python3 -m onepiece --url-file test/test-url-file.txt

# 跟据名字搜索comicid
python3 -m onepiece -s qq --name 海贼

# 生成pdf文件
# 注意: 生成pdf文件需要额外安装依赖，需要先执行 python3 -m pip install img2pdf 或 python3 -m pip install reportlab
python3 -m onepiece -s qq -id 505430 --pdf

# 推送到邮箱
# 注意: 发送到邮箱需预先配置好信息 配样例参照 https://github.com/lossme/ComicBook/blob/master/config.ini.example
# 并根据实际情况调整，将配置文件保存为 config.ini
python3 -m onepiece -s qq -id 505430 --pdf --mail --config config.ini
```

从其它站点下载，注意不同站点的comicid区别
```sh
# 从哔哩哔哩漫画下载
python3 -m onepiece -s bilibili -id mc24742 -c 1
# 从有妖气漫画下载
python3 -m onepiece -s u17 -id 195 -c 1

# 其它已支持的站点 https://github.com/lossme/ComicBook/projects/1
# 从章节列表页面的URL下载
python3 -m onepiece --url "https://manga.bilibili.com/detail/mc28603" -c 1
```

### 关于登录

1. [安装EditThisCookie插件](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
2. 在浏览器上登录某个站点，然后通过插件导出某个站点的cookies，并保存到本地文件 如`qq.json`
```sh
python3 -m onepiece -s qq -id=505430 -c -1 --cookies-path="qq.json"
```

### 高级批量下载

```sh
# 有些站点不一定支持，其它的通用参数也适用，可自行组合
# 下载最近更新页面的1到10页 所有漫画的最新一集
python3 -m onepiece -s nvshens --latest-all --latest-page 1-10

# 展示支持的标签
python3 -m onepiece -s nvshens --show-tags

# 下载标签搜索结果页面的1到10页 所有漫画的全集
python3 -m onepiece -s nvshens --tag-all --tag 女神 --tag-page 1-10 --all

# 下载搜索结果的所有漫画的全集
python3 -m onepiece -s nhentai --search-all --search-name 汉化 --search-page 1 --all
```

### 高级配置

#### 通过环境变量配置默认参数
```sh
# 可以将以下命令添加到 ~/.bashrc 或 ~/.zshrc 文件末尾
# 配置默认的配置文件路径 配置文件示例 https://github.com/lossme/ComicBook/blob/master/config.ini.example
export ONEPIECE_CONFIG_FILE="/home/key/MyConfig/config.ini"
```

### 一个意义不明的群
https://t.me/onecomicbook
