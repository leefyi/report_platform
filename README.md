1.python 测试报表平台（Demo） - 抛砖引玉

2.Django + pyecharts + MySql

===============================================
此项目借鉴了仁兄的布局和思路：https://github.com/testerSunshine/auto_ui
感谢！多多交流！

由于开始的时候本地运行不起来，加上对python3更熟悉一些，
索性python3+pyecharts重写了结构和图表渲染。

项目依赖（可以直接都使用最新版，兼容性不是问题）
    
    PyYAML==3.13
    requests==2.19.1
    PyMySQL==0.9.2
    djangorestframework==3.8.2
    redis==2.10.6
    Django==2.1
    pyecharts==0.5.8
    echarts-themes-pypkg==0.0.3
    django-redis==4.9.0
    django-redis-cache==1.7.1

项目配置

    安装依赖，项目根目录执行命令 pip install -r requirements.txt
    mysql建表，并设置为utf-8

    create database report_platform DEFAULT CHARACTER set utf8;

    根目录创建执行合表,全部ok表示成功
    
    python3 manage.py makemigrations   
    python3 manage.py migrate

    建连接db的配置文件(隐私，存在自己电脑或某服务器的位置，yaml文件注意缩进)

    # config_report.yaml
    ---
    db:
      ip: localhost
      port: 3306
      schema: report_platform
      uname: root
      passwd: XXXXXXX

    设置文件访问路径--Config.py 文件修改路径,利用PyYAML解析yaml配置

    if platform.system() == "Windows":
        path = os.path.join('d:\config_report.yaml')
    else:
        path = os.path.join('/usr/local/autoConfig/config_report.yaml')
    f = open(path)
    s = yaml.load(f)
    f.close()
    return s

    启动, 允许外网访问

    python3 manage.py runserver 0.0.0.0:8000

    
    本项目只是一个大概框架和思路。不过报表展示确实酷炫的一B。推荐大家使用echarts,并选用自己习惯的语言库。
    有想法欢迎随时联系笔者！如果有觉得还成的老铁给个小星星～