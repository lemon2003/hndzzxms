import os
from bs4 import BeautifulSoup


def process_html_files(directory):
    # 定义新的页脚和标题栏HTML
    new_footer = """    <!-- 页脚（复用原有样式） -->
    <footer>
        <div class="container footer-info">
            <p>单招咨询系统 河南铭书教育专用网站<br/>详细咨询：陈老师:16691532229 <br/>赵老师:18790463281 </p>
            <p>信阳校区地址：信阳师范东门金色童年院内<br/>光山地址：光山老汽车站进站口2楼铭书教育<br/>新县地址：新县二高正对面	<br/>息县地址：息县二高校门口<br/>罗山地址：罗山高级中学对面<br/>潢川地址：滨河北路与迎宾路交叉口西	</p>
            <p style="margin-top: 10px; font-size: 12px;">本系统仅提供咨询服务，最终政策以教育考试院公布为准</p>
        </div>
    </footer>"""

    new_header = """<header>
        <div class="container nav">
            <div class="logo">河南铭书教育单招咨询</div>
            <ul class="nav-menu">
                <li><a href="../shouye.html">首页</a></li>
                <li><a href="../yuanxiao.html">河南单招院校大全</a></li>
                <li><a href="../zhuanye.html">根据专业选院校</a></li>
                <li><a href="../chengji.html">根据成绩选院校</a></li>
                <li><a href="../us.html">关于我们</a></li>
            </ul>
        </div>
    </header>"""

    # 遍历目录中的所有HTML文件
    for filename in os.listdir(directory):
        if filename.endswith(".html") or filename.endswith(".htm"):
            filepath = os.path.join(directory, filename)

            # 读取文件内容
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(content, 'html.parser')

            # 1. 替换页脚
            footer = soup.find('footer')
            if footer:
                footer.replace_with(BeautifulSoup(new_footer, 'html.parser'))
            else:
                # 如果没有页脚，添加到body末尾
                body = soup.find('body')
                if body:
                    body.append(BeautifulSoup(new_footer, 'html.parser'))

            # 2. 替换标题栏
            header = soup.find('header')
            if header:
                header.replace_with(BeautifulSoup(new_header, 'html.parser'))
            else:
                # 如果没有标题栏，添加到body开头
                body = soup.find('body')
                if body:
                    body.insert(0, BeautifulSoup(new_header, 'html.parser'))

            # 3. 修改特定的div标签：将<div class="text-content" style="margin-left:20px;">改为<div class="major-plan-table" style="margin-left:20px;">
            divs = soup.find_all('div', class_='text-content')
            for div in divs:
                style = div.get('style', '')
                if 'margin-left:20px' in style:
                    div['class'] = 'major-plan-table'
                    # 确保保留原有的style属性
                    div['style'] = style

            # 保存修改后的文件
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            print(f"Processed: {filename}")


if __name__ == "__main__":
    # 设置要处理的目录路径（当前目录）
    current_directory = os.getcwd()
    process_html_files(current_directory)
    print("All HTML files have been processed.")