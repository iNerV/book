# -*- coding: UTF-8 -*-
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(r'C:\Users\NerV\PycharmProjects\myLibrary\myLibrary')  # FIXME не забыть поменять на боевом

import django
django.setup()

from grab import Grab
from books.models import Book, Author, Series, GrId, Titles, ISBN10, ISBN13, ASIN, Covers, Photos
import logging
import re
import requests

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

q = 14582711
host = 'https://www.goodreads.com'
g = Grab()
g.setup(charset='utf8', timeout=160000, connect_timeout=160000)


# isbn converter
def check_digit_10(isbn):
    assert len(isbn) == 9
    sum = 0
    for i in range(len(isbn)):
        c = int(isbn[i])
        w = i + 1
        sum += w * c
    r = sum % 11
    if r == 10:
        return isbn + 'X'
    else:
        return isbn + str(r)

# start parser
while q <= 14582711:
    # ####CONSTANTS-START######
    title = set([])
    original_title = ''
    isbn13 = []
    isbn = []
    asin = []
    lang = ''
    en_desc = ''
    ru_desc = ''
    other_desc = ''
    series = ''
    num_series = ''
    series_name = ''
    covers = []
    cover_name = ''
    url = []
    author_link = ''
    author = ''
    photo = ''
    gender = ''
    birth_date = ''
    site = ''
    # ####CONSTANTS-END######
    try:
        try:
            g = Grab()
            g.go(host+str('/book/show/')+str(q))
            # g.proxylist.set_source('file', location='proxy.txt')
            print(g.response.headers.get('Status'))
            status = g.response.headers.get('Status')
            if status == '302 Found':
                q += 1
                continue
            if status == '301 Moved Permanently':
                location = g.response.headers.get('Location')
                print(g.response.headers.get('Status'))
                g.go(str(location))
                # g.proxylist.set_source('file', location='proxy.txt')
        except IndexError:
            print('No Book Error')
            q += 1

        # ####AUTHOR-START#####
        try:
            g2 = Grab()
            # g2.proxylist.set_source('file', location='proxy.txt')
            g2.setup(charset='utf8', timeout=30, connect_timeout=40)
            author_link = g.doc.select('//a[contains(@class, "authorName")]')[0].attr("href").split('/')[5].rsplit('.')[0]
            g2.go(host+'/author/show/'+str(author_link))

            try:
                author = g2.doc.select('//h1[contains(@class, "authorName")]').text()  # AuthorName
                print(author)  # AuthorName
            except IndexError:
                print('AuthorName Error')  # test
                pass

            try:

                p_a = requests.get(re.sub(r'p5', 'p8', g2.doc.select('//div[contains(@class, "leftContainer")]').select('..//img').attr("src")))
                photo = g2.doc.select('//div[contains(@class, "leftContainer")]').select('..//img').attr("src").split('/')[5]
                photo = re.sub(r'p5', 'p8', photo)
                out = open(r"../media/authors_photo/"+photo, "wb")
                out.write(p_a.content)
                out.close()
                if 'nophoto' in photo:
                    photo = 'no_photo.png'
                else:
                    print('Photo: '+photo)  # Photo
            except IndexError:
                photo = 'no_photo.png'
                print('Photo Error')  # test
                pass

            try:
                gender = g2.doc.select('//div[contains(@itemprop, "gender")]').text()
                print(gender)  # gender
            except IndexError:
                print('gender Error')  # test
                pass

            try:
                birth_date = g2.doc.select('//div[contains(@itemprop, "birthDate")]').text()
                print(birth_date)  # birthDate
            except IndexError:
                print('birthDate Error')  # test
                pass

            try:
                site = g2.doc.select('//div[contains(@class, "bigGreyBoxContent")]').select('.//a[contains(@itemprop, "url")]').attr("href")
                print(site)  # WebSite
            except IndexError:
                print('WebSite Error')  # test
                pass
        except IndexError:
            print('AuthorPage Error')  # test
            pass
        # ####AUTHOR-END#####

        try:
            other_editions = re.search('[\d]+', g.doc.select('//div[contains(@class, "otherEditionsLink")]/a').attr("href")).group()

            # ####OTHER EDITIONS-START#####
            q2 = 1
            while q2 >= 0:
                try:
                    g4 = Grab()
                    # g4.proxylist.set_source('file', location='proxy.txt')
                    g4.setup(charset='utf8', timeout=30, connect_timeout=40)
                    g4.go(host+'/work/editions/'+str(other_editions)+'?page='+str(q2)+'&per_page='+str(1)+'&utf8='+str(1))
                except NameError:
                    pass

                try:
                    g3 = Grab()
                    # g3.proxylist.set_source('file', location='proxy.txt')
                    g3.setup(charset='utf8', timeout=30, connect_timeout=40)
                    book_link = str(g4.doc.select('//div[contains(@class, "dataRow")]/a')[0].attr("href"))
                    g3.go(host+book_link)

                    try:
                        title.append(g3.doc.select('//h1[contains(@class, "bookTitle")]').text().split(' (')[0])  # title
                    except IndexError:
                        print('Title Error')  # test
                        pass

                except IndexError:
                    b, created = Book.objects.get_or_create(title=original_title, gr_id=q, ru_desc=ru_desc, en_desc=en_desc, num_series=num_series)
                    s, created = Series.objects.get_or_create(gr_id=series, name=series_name)
                    b.series.add(s)
                    a, created = Author.objects.get_or_create(name=author, gender=gender, birth_date=birth_date, site=site)
                    b.author.add(a)
                    for val in url:
                        grid, created = GrId.objects.get_or_create(gr_id=val)
                    for val in isbn:
                        isbn10db, created = ISBN10.objects.get_or_create(isbn10=val, book=b)
                    for val in isbn13:
                        isbn13db, created = ISBN13.objects.get_or_create(isbn13=val, book=b)
                    for val in asin:
                        asindb, created = ASIN.objects.get_or_create(asin=val, book=b)
                    for val in title:
                        titledb, created = Titles.objects.get_or_create(title=val, book=b)
                    for val in covers:
                        covers, created = Covers.objects.get_or_create(cover=val, book=b)
                    photos, created = Photos.objects.get_or_create(photo='authors_photo/'+photo, author=a)
                    q += 1
                    break

                try:
                    original_title = g3.doc.select('//div[contains(@class, "infoBoxRowItem")]')[0].text()  # orig. title
                except IndexError:
                    print('Original title Error')  # test
                    pass

                try:
                    lang = g3.doc.select('//div[contains(@itemprop, "inLanguage")]').text()  # lang
                except IndexError:
                    print('Lang Error')  # test
                    pass

                url.append(str(re.search('[\d]+', g3.response.url).group()).strip())  # url

                try:
                    if lang == 'English' and en_desc == '':
                        en_desc = g3.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                    elif lang == 'Russian' and ru_desc == '':
                        ru_desc = g3.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                except IndexError:
                    try:
                        if lang == 'English' and en_desc == '':
                            en_desc = g3.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                        elif lang == 'Russian' and ru_desc == '':
                            ru_desc = g3.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                    except IndexError:
                        print('desc Error out')  # test
                        pass

                try:
                    p = requests.get(g.doc.select('//div[contains(@class, "bookCoverPrimary")]/a').select('.//img').attr("src"))
                    cover_name = g.doc.select('//div[contains(@class, "bookCoverPrimary")]/a').select('.//img').attr("src").split('/')[5]
                    out = open(r"../media/covers/"+cover_name, "wb")
                    out.write(p.content)
                    out.close()
                    covers.append('covers/'+cover_name)
                except IndexError:
                    pass

                try:
                    series = g3.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].attr("href").split('/')[2].rsplit('-')[0]
                except IndexError:
                    print('series error')  # test
                    pass

                try:
                    series_name = g3.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].text().split('(')[1].rsplit('#')[0]
                except IndexError:
                    print('series name error')  # test
                    pass

                try:
                    num_series = g3.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].text().split('(')[1].rsplit('#')[1].rsplit(')')[0]
                except IndexError:
                    print('Num in series error')  # test
                    pass

                if g4.doc.text_search(u'ISBN:'):
                    isbn.append(str(g4.doc.select('//div[contains(@class, "dataValue")]')[1].text().split('(')[0]).strip())  # isbn10
                    try:
                        isbn13.append(str(re.sub(r'ISBN13: ', '', g4.doc.select('//div[contains(@class, "dataValue")]')[1].text().split('(')[1][:-1])).strip())  # isbn13
                    except IndexError:
                        pass
                elif g4.doc.text_search(u'ISBN13:'):
                    isbn13.append(str(g4.doc.select('//div[contains(@class, "dataValue")]')[1].text()).strip())  # isbn13
                elif g4.doc.text_search(u'ASIN:'):
                    asin.append(str(g4.doc.select('//div[contains(@class, "dataValue")]')[1].text()).strip())  # asin
                q2 += 1
            # ####OTHER EDITIONS-END#####

        # ####NO OTHER EDITIONS-START#####
        except IndexError:
            try:
                title = g.doc.select('//h1[contains(@class, "bookTitle")]').text().split(' (')[0]  # title
            except IndexError:
                print('title Error / No Book Error')  # test
                pass

            try:
                original_title = g.doc.select('//div[contains(@class, "infoBoxRowItem")]')[0].text()  # orig. title
            except IndexError:
                print('Original title Error')  # test
                pass

            try:
                p = requests.get(g.doc.select('//div[contains(@class, "bookCoverPrimary")]/a').select('.//img').attr("src"))
                cover_name = g.doc.select('//div[contains(@class, "bookCoverPrimary")]/a').select('.//img').attr("src").split('/')[5]
                out = open(r"../media/covers/"+cover_name, "wb")
                out.write(p.content)
                out.close()
            except IndexError:
                cover_name = 'no_cover.png'
                pass

            try:
                if g.doc.text_search(u'ISBN13'):
                    isbn13 = g.doc.select('//*[contains(@itemprop, "isbn")]').text().strip()  # ISBN13
                elif g.doc.text_search(u'ASIN'):
                    asin = str(g.doc.select('//div[contains(@class, "dataValue")]')[1].text()).strip()  # ASIN
            except IndexError:
                print('ISBN13/ASIN Error')  # test
                pass

            try:
                lang = g.doc.select('//div[contains(@itemprop, "inLanguage")]').text()  # Lang
            except IndexError:
                print('Lang Error')  # test
                pass

            try:
                if lang == 'English' and en_desc == '':
                    en_desc = g.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]  # description
                elif lang == 'Russian' and ru_desc == '':
                    ru_desc = g.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]  # description
            except IndexError:
                try:
                    if lang == 'English' and en_desc == '':
                        en_desc = g.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]  # description
                    elif lang == 'Russian' and ru_desc == '':
                        ru_desc = g.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]  # description
                except IndexError:
                    print('desc Error out')  # test
                    pass

            try:
                series = g.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].attr("href").split('/')[2].rsplit('-')[0]  # series url
            except IndexError:
                print('series error')  # test
                pass

            try:
                series_name = g.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].text().split('(')[1].rsplit('#')[0]  # series name
            except IndexError:
                print('series name error')  # test
                pass

            try:
                num_series = g.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].text().split('(')[1].rsplit('#')[1].rsplit(')')[0]  # num in series
            except IndexError:
                print('Num in series error')  # test
                pass

            url = str(re.search('[\d]+', g.response.url).group())  # url

            b, created = Book.objects.get_or_create(title=original_title, gr_id=q, ru_desc=ru_desc, en_desc=en_desc, num_series=num_series)
            s, created = Series.objects.get_or_create(gr_id=series, name=series_name)
            b.series.add(s)
            a, created = Author.objects.get_or_create(name=author, gender=gender, birth_date=birth_date, site=site)
            b.author.add(a)
            grid, created = GrId.objects.get_or_create(gr_id=url)
            isbn10db, created = ISBN10.objects.get_or_create(isbn10=check_digit_10(isbn13[3:-1]), book=b)
            isbn13db, created = ISBN13.objects.get_or_create(isbn13=isbn13, book=b)
            if asin:
                asindb, created = ASIN.objects.get_or_create(asin=asin, book=b)
            covers, created = Covers.objects.get_or_create(cover='covers/'+cover_name, book=b)
            photos, created = Photos.objects.get_or_create(photo='authors_photo/'+photo, author=a)

            q += 1
        # ####NO OTHER EDITIONS-END#####
    except IndexError:
        print('PROBLEM, While STOP!!!')  # test