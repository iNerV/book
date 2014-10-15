# -*- coding: UTF-8 -*-
from grab import Grab
import logging
import re

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

q = 1
host = 'https://www.goodreads.com'
g = Grab()
g.setup(charset='utf8', timeout=4096, connect_timeout=4096)
# ####CONSTANTS-START######
title = []
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
cover = ''
url = []
author_link = ''
author = ''
photo = ''
gender = ''
birth_date = ''
site = ''
# ####CONSTANTS-END######

while q <= 1:
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
                photo = g2.doc.select('//div[contains(@class, "leftContainer")]').select('..//img').attr("src")
                if 'nophoto' in photo:
                    cover = 'https://s.gr-assets.com/assets/nophoto/book/blank-133x176-99d2cd1a7cf8ae9ed346e75dda60b54b.jpg'
                else:
                    print('Photo: '+photo)  # Photo
            except IndexError:
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
                    print('title:')
                    print(set(list(title)))
                    print('isbn:')
                    print(list(isbn))
                    print('isbn13:')
                    print(list(isbn13))
                    print('asin:')
                    print(list(asin))
                    print('url:')
                    print(list(url))
                    print()

                    print('Lang: '+lang)  # Lang
                    print('Original title: '+original_title)  # orig. title
                    print('Num in series: '+num_series)  # series
                    print('series name: '+series_name)  # series
                    print('series: '+series)  # series

                    print('OTHER Description: '+other_desc)  # description
                    print('EN Description: '+en_desc)  # description
                    print('RU Description: '+ru_desc)  # description

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

                url.append(str(re.search('[\d]+', g3.response.url).group()))  # url

                try:
                    if lang != 'English' and lang != 'Russian' and other_desc == '':
                        other_desc = g3.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                    elif lang == 'English' and en_desc == '':
                        en_desc = g3.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                    elif lang == 'Russian' and ru_desc == '':
                        ru_desc = g3.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                except IndexError:
                    try:
                        if lang != 'English' and lang != 'Russian' and other_desc == '':
                            other_desc = g3.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                        elif lang == 'English' and en_desc == '':
                            en_desc = g3.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                        elif lang == 'Russian' and ru_desc == '':
                            ru_desc = g3.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                    except IndexError:
                        print('desc Error out')  # test
                        pass

                try:
                    cover = g3.doc.select('//div[contains(@class, "bookCoverPrimary")]/a').select('.//img').attr("src")
                except IndexError:
                    cover = 'https://s.gr-assets.com/assets/nophoto/book/blank-133x176-99d2cd1a7cf8ae9ed346e75dda60b54b.jpg'

                if 'nophoto' in cover:
                    cover = 'https://s.gr-assets.com/assets/nophoto/book/blank-133x176-99d2cd1a7cf8ae9ed346e75dda60b54b.jpg'
                else:
                    print('cover: '+cover)  # cover

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
                    isbn.append(g4.doc.select('//div[contains(@class, "dataValue")]')[1].text().split('(')[0])  # isbn10
                    try:
                        isbn13.append(re.sub(r'ISBN13: ', '', g4.doc.select('//div[contains(@class, "dataValue")]')[1].text().split('(')[1][:-1]))  # isbn13
                    except IndexError:
                        pass
                elif g4.doc.text_search(u'ISBN13:'):
                    isbn13.append(g4.doc.select('//div[contains(@class, "dataValue")]')[1].text())  # isbn13
                elif g4.doc.text_search(u'ASIN:'):
                    asin.append(g4.doc.select('//div[contains(@class, "dataValue")]')[1].text())  # asin
                q2 += 1
            # ####OTHER EDITIONS-END#####

        # ####NO OTHER EDITIONS-START#####
        except IndexError:
            try:
                title = g.doc.select('//h1[contains(@class, "bookTitle")]').text().split(' (')[0]
                print('Title: '+title)  # title
            except IndexError:
                print('title Error / No Book Error')  # test
                pass

            try:
                original_title = g.doc.select('//div[contains(@class, "infoBoxRowItem")]')[0].text()  # orig. title
                print('Original title: '+original_title)  # orig. title
            except IndexError:
                print('Original title Error')  # test
                pass

            try:
                cover = g.doc.select('//div[contains(@class, "bookCoverPrimary")]/a').select('.//img').attr("src")
            except IndexError:
                cover = 'https://s.gr-assets.com/assets/nophoto/book/blank-133x176-99d2cd1a7cf8ae9ed346e75dda60b54b.jpg'

            if 'nophoto' in cover:
                cover = 'https://s.gr-assets.com/assets/nophoto/book/blank-133x176-99d2cd1a7cf8ae9ed346e75dda60b54b.jpg'
            else:
                print('cover: '+cover)  # cover

            try:
                if g.doc.text_search(u'ISBN13'):
                    isbn13 = g.doc.select('//*[contains(@itemprop, "isbn")]').text()
                    print('ISBN13: '+isbn13)  # ISBN13
                elif g.doc.text_search(u'ASIN'):
                    asin = g.doc.select('//*[contains(@itemprop, "isbn")]').text()
                    print('ASIN: '+asin)  # ASIN
            except IndexError:
                print('ISBN13/ASIN Error')  # test
                pass

            try:
                lang = g.doc.select('//div[contains(@itemprop, "inLanguage")]').text()
                print('Lang: '+lang)  # Lang
            except IndexError:
                print('Lang Error')  # test
                pass

            try:
                if lang != 'English' and lang != 'Russian':
                    other_desc = g.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                    print('OTHER Description: '+other_desc)  # description
                elif lang == 'English' and en_desc == '':
                    en_desc = g.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                    print('EN Description: '+en_desc)  # description
                elif lang == 'Russian' and ru_desc == '':
                    ru_desc = g.doc.select('//div[contains(@id, "description")]/span')[1].text().rsplit('(less)')[0]
                    print('RU Description: '+ru_desc)  # description
            except IndexError:
                try:
                    if lang != 'English' and lang != 'Russian' and other_desc == '':
                        other_desc = g.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                        print('OTHER Description: '+other_desc)  # description
                    elif lang == 'English' and en_desc == '':
                        en_desc = g.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                        print('EN Description: '+en_desc)  # description
                    elif lang == 'Russian' and ru_desc == '':
                        ru_desc = g.doc.select('//div[contains(@id, "description")]/span')[0].text().rsplit('(less)')[0]
                        print('RU Description: '+ru_desc)  # description
                except IndexError:
                    print('desc Error out')  # test
                    pass

            try:
                series = g.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].attr("href").split('/')[2].rsplit('-')[0]
                print('series: '+series)  # series
            except IndexError:
                print('series error')  # test
                pass

            try:
                series_name = g.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].text().split('(')[1].rsplit('#')[0]
                print('series name: '+series_name)  # series
            except IndexError:
                print('series name error')  # test
                pass

            try:
                num_series = g.doc.select('//h1[contains(@class, "bookTitle")]//a')[0].text().split('(')[1].rsplit('#')[1].rsplit(')')[0]
                print('Num in series: '+num_series)  # series
            except IndexError:
                print('Num in series error')  # test
                pass

            url = str(re.search('[\d]+', g.response.url).group())  # url
            print('URL: '+url)
            q += 1
        # ####NO OTHER EDITIONS-END#####
    except IndexError:
        print('PROBLEM, While STOP!!!')  # test

# values = ['abc', 'def', 'ghi']
# a list of unsaved Entry model instances
# aList = [Entry(headline=val) for val in values]
# Entry.objects.bulk_create(aList)
