#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 爬取小说http://biqugu.net/
import requests
import time
import re


# 获取html
def get_html(book_id):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}
    url = r'http://biqugu.net/%s/' % book_id
    response = requests.get(url, headers=headers)
    html = response.text
    return html


# 获取标题/建立文件
def get_title(html, book_id):
    book_title = re.findall(r'<a href="/%s/">(.*?)</a>' % book_id, html)[0]

    return book_title


# 获取章节列表
def get_list(html):
    dl = re.findall(r'<div id="content">.*?<div class="footer">', html, re.S)[0]
    chapter_info_list = re.findall(r'<a href="(.*?)" title="(.*?)">', dl)
    return chapter_info_list


# 下载章节内容
def down_chapter(chapter_url):
    chapter_response = requests.get(chapter_url)
    chapter_html = chapter_response.text
    chapter_content = re.findall(r'</table>(.*?)<input', chapter_html, re.S)[0]
    return chapter_content


# 清洗数据
def replace_date(chapter_content):
    chapter_content = chapter_content.replace(' ', '')
    chapter_content = chapter_content.replace('<br/>', '')
    chapter_content = chapter_content.replace('</div>', '')
    chapter_content = chapter_content.replace('\n', '')
    chapter_content = chapter_content.replace('\r', '')
    return chapter_content


# 显示进度
def str_date(fb, chapter_title, chapter_content):
    fb.write(chapter_title)
    fb.write(chapter_content)
    fb.write('\n\n')
    print("获取", chapter_title)

# 主函数
def get_novel(book_id):
    html = get_html(book_id)
    book_title = get_title(html, book_id)
    chapter_info_list = get_list(html)
    fb = open('%s.txt' % book_title, 'w')
    for chapter_info in chapter_info_list:
        chapter_url, chapter_title = chapter_info
        chapter_url = r'http://biqugu.net/%s' % chapter_url
        content = down_chapter(chapter_url)
        content = replace_date(content)
        str_date(fb, chapter_title, content)
        time.sleep(0.5)


book_id = input('请输入小说id:')
# '177913'

get_novel(book_id)
