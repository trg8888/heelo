import csv
import redis
import requests
import random
from sqlalchemy import func
from bluelog.models import Subcategory as Subcategory_sql
from bluelog.models import Picture as Picture_sql
from flask import current_app
from bluelog.extensions import db
import re
import os
from bluelog.Backstage.chaojiying import Chaojiying_Client
import uuid
from lxml import etree
from bluelog.models import basicsettings as basicsettings_sql, Faq as Faq_sql, PaymentMethods as PaymentMethods_sql ,\
ReturnPolicy as ReturnPolicy_sql, About as About_sql, PrivacySecurity as PrivacySecurity_sql
from bluelog.extensions import r


class Configure(object):
    def __init__(self,url,name,pwd,data,data_zd,is_csv=True,):
        self.url = url
        self.name_name = name
        self.name_pwd = pwd
        self.data = data
        self.data_zd = data_zd
        self.is_csv = is_csv
        self.r = r
        self.session = requests.session()
        self.size = []
        self.sku = 1
        self.path = 'csv'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists('img'):
            os.makedirs('img')
        self.fen = 0
        self.name = ''.join(random.sample(
            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f',
             'e',
             'd', 'c', 'b', 'a'], 7)).upper()
        with open(self.path + '/' + self.name + '.csv', 'w', newline='', encoding='utf-8')as files:
            f_csvs = csv.writer(files)
            f_csvs.writerow(
                ['v_sku', 'v_name', 'v_short_description', 'v_description', 'v_image', 'v_url', 'v_attribute',
                 'v_price',
                 'v_specials_price', 'v_specials_expire_date', 'v_date_added', 'v_in_stock', 'v_status', 'v_viewed',
                 'v_ordered', 'v_category_sku', 'v_sort_order', 'v_meta_title', 'v_meta_keywords', 'v_meta_description',
                 'v_brand_filter', 'v_class_filter', 'v_color_filter', 'v_gender_filter', 'v_material_filter',
                 'v_year_filter', 'v_origin_filter', 'v_series_filter', 'v_spec_filter'])
        with open(self.path + '/' + self.name + 'fen.csv', 'w', newline='', encoding='utf-8')as files:
            f_csvs = csv.writer(files)
            f_csvs.writerow(
                ['v_sku', 'v_name', 'v_description', 'v_image', 'v_url', 'v_parent_sku', 'v_date_added', 'v_status',
                 'v_sort_order', 'v_meta_title', 'v_meta_keywords', 'v_meta_description', '', '', '', ''])
        with open(self.path + '/' + self.name + 'size.csv', 'w', newline='', encoding='utf-8')as files:
            f_csvs = csv.writer(files)
            f_csvs.writerow(
                ['v_name', 'v_type', 'v_sort_order', 'v_value'])
        self.req_header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.securityToken = None

    def run(self):
        self.csv()

    def csv(self):
        for _ in self.data:

            data = Subcategory_sql.query.filter_by(disable=False).filter_by(major_id=int(_['id'])).order_by(
                func.random()).limit(int(_.get('int_id'))).all()
            self.csv_make(data=data,data_bool=_['state'])
        for _ in self.data_zd:
            data = Subcategory_sql.query.filter_by(disable=False).filter_by(major_id=int(_['id'])).order_by(
                func.random()).limit(int(_.get('int_id'))).all()
            self.csv_make(data=data, data_bool=_['state'], zhiding=_['zhiding'])
        self.csv_size()

    def csv_make(self,data,data_bool,zhiding=None):
        if data_bool:
            if data[0].major.remarks:
                name = random.choice(data[0].major.remarks.split(','))
            else:
                name = data[0].major.name

            with open(self.path + '/' + self.name + 'fen.csv', 'a+', newline='', encoding='utf-8')as files:
                self.fen += 1
                f_csvs = csv.writer(files)
                f_csvs.writerow([name, name, '', '', '', '', '', '1', str(self.fen), name, name,
                 name])
            for _ in data:
                self.generate(name=_.name,min_=_.major.least,max_=_.major.maximum,id_=_.id,zhiding=zhiding)
                with open(self.path + '/' + self.name + 'fen.csv', 'a+', newline='', encoding='utf-8') as files:
                    self.fen += 1
                    f_csvs = csv.writer(files)
                    f_csvs.writerow([_.name, _.name, '', '', '', name, '', '1', str(self.fen), _.name, _.name,
                                     _.name])
        else:
            for _ in data:
                self.generate(name=_.name, min_=_.major.least, max_=_.major.maximum, id_=_.id,zhiding=zhiding)
                with open(self.path + '/' + self.name + 'fen.csv', 'a+', newline='', encoding='utf-8') as files:
                    self.fen += 1
                    f_csvs = csv.writer(files)
                    f_csvs.writerow([_.name, _.name, '', '', '', '', '', '1', str(self.fen), _.name, _.name,
                                     _.name])

    def generate(self, name, min_, max_,id_,zhiding=None):
        data_all = Picture_sql.query.filter_by(subcategorys_id=int(id_)).order_by(func.random()).limit(random.randint(current_app.config.get('MINIMUM'),current_app.config.get('MAXIMUM_NUMBER'))).all()
        for data in data_all:
            if data.frequency:
                data.frequency = data.frequency + 1
            else:
                data.frequency = 1
            db.session.add(data)
            size = 'Size#'
            name_new = self.name + r'%04d' % self.sku
            if data.color:
                color = data.color.split(',')
                if data.attribute:
                    attribute = data.attribute.split(',')
                else:
                    attribute = None
                for _ in color:
                    if attribute:
                        for i in attribute:
                            size += '%s:' %(_+current_app.config.get('ATTRIBUTE_BLANK','---')+i)
                            self.size.append(_+current_app.config.get('ATTRIBUTE_BLANK','---')+i)
                    else:
                        size += '%s:' % (_)
                        self.size.append(_)
            else:
                if data.attribute:
                    attribute = data.attribute.split(',')
                else:
                    attribute = None
                if attribute:
                    for _ in attribute:
                        size += '%s:%d;' % (_)
                        self.size.append(_)

            if zhiding:
                zhiding_ = zhiding.split(',')
                tejia_ = float(random.choice(zhiding_))
                jiage = round(tejia_ + (tejia_ * round(random.uniform(0.6, 0.85), 2)), 2)
                tejia = tejia_
            else:
                a = random.uniform(min_, max_)
                tejia_ = round(a, 2)
                jiage = round(tejia_ + (tejia_ * round(random.uniform(0.6, 0.85), 2)), 2)
                tejia = tejia_
            with open(self.path + '/' + self.name + '.csv', 'a+', newline="", encoding='utf-8')as file:
                self.sku += 1
                csv_writer = csv.writer(file)
                csv_writer.writerow(
                    [name_new, data.name, '', data.description,
                     'img/' + data.picture + '.jpg', '', size, jiage,
                     tejia, '', '', '1', '1', '',
                     '', name, '', data.name, data.name, data.name,
                     '', '', '', '', '',
                     '', '', '', ''])
            self.r.sadd('img', data.picture + '.jpg-' + name + '--' + str(data.frequency))
        db.session.commit()

    def csv_size(self):
        color_1 = ''
        color_item = {}
        for id_, i in enumerate(list(set(self.size))):
            color_1 += i + ':' + str(id_ + 1) + ';'
            color_item[i] = id_ + 1
        with open(self.path + '/' + self.name + 'size.csv', 'a+', newline="", encoding='utf-8')as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(
                ['size', 'select', '1', color_1])

    def landed(self):
        """
        登录
        """
        link_not =  self.url
        i = 'https://' + link_not + '/index.php'
        response = self.session.get(i, headers=self.req_header).text
        responses = re.findall('<img src="(.*?)" oncl', response)
        if responses:
            responses = responses[0]
        else:
            self.r.sadd('url', self.url+',错误代码9000')
            return '错误' + self.url
        securityToken = re.findall('<input type="hidden" value="(.*?)" name="securityToken" />', response)[0]
        self.securityToken = securityToken
        response = self.session.get(responses, headers=self.req_header).content
        img_sku = uuid.uuid4().hex
        with open('img/' + img_sku + '.jpg' , 'wb')as file:
            file.write(response)
        chaojiying = Chaojiying_Client(current_app.config.get('NAME'), current_app.config.get('PWD'), current_app.config.get('NAME_ID'))
        im = open('img/' + img_sku + '.jpg', 'rb').read()
        yzm = chaojiying.PostPic(im, 1902)['pic_str']
        if not yzm:
            self.r.sadd('url', self.url + ',错误代码5002')
            return '5002'
        link = 'https://' + link_not + '/login.php?action=loginPost'
        data = {
            'securityToken': securityToken,
            'action': 'loginPost',
            'username': 'manager',
            'password': 'WmYEYnPt4CoOAmd7',
            'captcha': yzm
        }
        self.session.post(url=link, data=data, headers=self.req_header)

    def clear_data(self):
        """
        清除数据
        """
        url = 'https://www.' + self.url + '/import_old.php?action=clearProduct'
        self.session.get(url=url, headers=self.req_header)

    def upload(self):
        """
        上传数据
        """
        shangchuan_1_data = {
            'securityToken': self.securityToken,
            'MAX_FILE_SIZE': '100000000',
            'action': 'product_option',

        }
        shangchuan_1_files = {
            'usrfl': ('size.csv', open(self.path + '/' + self.name + 'size.csv', 'r', encoding='utf-8'), 'application/vnd.ms-excel')
        }
        shangchuan_1 = 'https://www.' + self.url + '/import_old.php'
        self.session.post(url=shangchuan_1, data=shangchuan_1_data, files=shangchuan_1_files)

        shangchuan_2_data = {
            'securityToken': self.securityToken,
            'MAX_FILE_SIZE': '100000000',
            'action': 'category',

        }
        wocao_1 = self.path + '/' + self.name + 'fen.csv'
        shangchuan_2_files = {
            'usrfl': ('size.csv', open(wocao_1, 'r', encoding='utf-8'), 'application/vnd.ms-excel')
        }
        shangchuan_2 = 'https://www.' + self.url + '/import_old.php'
        self.session.post(url=shangchuan_2, data=shangchuan_2_data, files=shangchuan_2_files)

        shangchuan_3_data = {
            'securityToken': self.securityToken,
            'MAX_FILE_SIZE': '100000000',
            'action': 'product',

        }
        shangchuan_3_files = {
            'usrfl': ('1.csv', open(self.path + '/' + self.name + '.csv', 'r', encoding='utf-8'), 'application/vnd.ms-excel')
        }
        shangchuan_3 = 'https://www.' + self.url + '/import_old.php'
        self.session.post(url=shangchuan_3, data=shangchuan_3_data, files=shangchuan_3_files)

    def basic_settings(self):
        """
        基本设置
        """
        wangzan = re.findall(r'(.*?)/', self.url)
        panduan = 'https://' + self.url + '/configuration.php?gID=1'
        panduan_post = self.session.get(url=panduan, headers=self.req_header).text
        panduan_one = etree.HTML(panduan_post)
        panduan_new = \
            panduan_one.xpath(
                '/html/body/div/div/div[2]/form/table/tbody/tr[9]/td[2]/select/option[@value!="default"]/text()')
        if not panduan_new:
            return '403'
        panduan_new = panduan_new[0]
        def ranstr(num):
            # 猜猜变量名为啥叫 H
            H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

            salt = ''
            for i in range(num):
                salt += random.choice(H)

            return salt

        def hello(num):
            # 猜猜变量名为啥叫 H
            H = '0123456789'

            salt = ''
            for i in range(num):
                salt += random.choice(H)

            return salt

        salt = ranstr(4)
        sass = hello(3)

        jibenshezhi_link = 'https://' + self.url + '/configuration.php?gID=1&action=save'
        data = basicsettings_sql.query.order_by(func.random()).limit(1).first()
        data_ = []
        data_.append(data.title)
        data_.append(data.Keyword)
        data_.append(data.description)
        random.shuffle(data_)
        jibenshezhi_data = {
            'securityToken': self.securityToken,
            'configuration_group_id': '1',
            'configuration[STORE_NAME]': salt.upper() + sass,
            'configuration[STORE_WEBSITE]': wangzan[0],
            'configuration[STORE_EMAIL]': '',
            'configuration[STORE_TELEPHONE]': '',
            'configuration[STORE_WELCOME]': '',
            'configuration[STORE_CURRENCY]': 'USD',
            'configuration[STORE_COUNTRY]': '234',
            'configuration[STORE_LANGUAGE]': 'en',
            'configuration[STORE_TEMPLATE_DIR]': panduan_new,
            'configuration[STORE_DISABLE_EMAIL]': '@northeastlink.net',
            'configuration[HEAD_DEFAULT_TITLE]': data_[0],
            'configuration[HEAD_TITLE_PREFIX]': '',
            'configuration[HEAD_TITLE_SUFFIX]': '',
            'configuration[HEAD_DEFAULT_KEYWORDS]': data_[1],
            'configuration[HEAD_DEFAULT_DESCRIPTION]': data_[2],
            'configuration[HEADER_LOGO_SRC]': 'logo.png',
            'configuration[HEADER_LOGO_ALT]': 'Logo Alt',
            'configuration[FOOTER_COPYRIGHT]': '©' + wangzan[0] + '. All Rights Reserved.',
            'configuration[FOOTER_ABSOLUTE_FOOTER]': '',
            'configuration[ONLINE_SERVICE]': '',
            'configuration[SHOPPING_CART_MODE]': '0',
            'configuration[POPULAR_SEARCH_KEYWORDS]': '',
            'configuration[POPULAR_SEARCH_LIMIT]': '',
            'configuration[POPULAR_SEARCH_SIDEBAR_LIMIT]': '',
            'configuration[FACEBOOK_ID]': '',
            'configuration[SEND_EMAIL_ACCOUNT]': '',
            'configuration[SEND_EMAIL_PASSWORD]': 'VFa7MncJuGL75muF',
            'configuration[SEND_EMAIL_HOST]': 'smtpdm-ap-southeast-2.aliyun.com',
            'configuration[SEND_EMAIL_PORT]': '465',
            'configuration[OA_API_URL]': 'http://liwenoa.veveveve.com',
            'configuration[OA_API_TOKEN]': 'eYzNKDzDRQbSEh7Y',
            'configuration[OA_API_IP_CHECK_COUNTRY]': '',
            'configuration[OA_API_IP_CHECK_SWITCH]': '1',
            'configuration[OA_API_IP_CHECK_JUMP]': '',
            'configuration[EPAYPAL_API_URL]': 'http://liwenapi.vipsmerchant.com/v1/',
            'configuration[EPAYPAL_API_TOKEN]': 'LogLq39yiSYJUnbR',
            'configuration[EPAYPAL_PAYMENT_MD5KEY]': '55zEcsG9LbdtvmHh',
        }

        self.session.post(url=jibenshezhi_link, data=jibenshezhi_data, headers=self.req_header)

    def product_list(self,):
        """
        产品列表
        """
        url = 'https://www.%s/category.php' % self.url
        data = self.session.get(url, headers=self.req_header).text
        html = etree.HTML(data)
        data = html.xpath('/html/body/div/div/div[2]/div/form/table/tbody/tr/td[2]/text()')
        sadasdsadsa = ['price_asc', 'price_desc', 'date_added_desc', 'viewed_desc'][random.randint(0, 3)]
        qidong = random.randint(0,1)
        ggg = 3
        ggg_ = 4
        canpin = ['12,24,36,48', '16,32,48,64'][qidong]
        canpins = ['12', '16'][qidong]
        liebiao = []
        for i in random.sample(data, ggg):
            linksss = 'https://www.' + self.url + '/product.php?filter_category_id=%s' % i
            sad = self.session.get(linksss, headers=self.req_header).text
            sadsadsad = re.findall('(?s)src=".*" /></td>.*?<td>\d{1,3}</td>', sad)
            liebiao_ = []
            for isss in sadsadsad:
                asdasdsadaasdsa = re.findall('<td>(\d{1,})</td>', isss)
                for issss in asdasdsadaasdsa:
                    liebiao_.append(issss)
            try:
                liebiao.extend(random.sample(liebiao_, k=ggg_))
            except ValueError:
                self.r.sadd('url', self.url+',错误代码5000')
                return '404'
        ssss = liebiao
        canpingyouhua_data = {
            'securityToken': self.securityToken,
            'configuration_group_id': '3',
            'configuration[CATEGORY_PAGE_SHOW_MODE]': '0',
            'configuration[INDEX_CATEGORY_LIST]': '',
            'configuration[PRODUCT_LIST_MODE]': 'grid-list',
            'configuration[PRODUCT_LIST_SORT]': sadasdsadsa,
            'configuration[PRODUCT_GRID_PER_PAGE_VALUES]': canpin,
            'configuration[PRODUCT_GRID_PER_PAGE]': canpins,
            'configuration[PRODUCT_GRID_PER_ROW]': '4',
            'configuration[PRODUCT_LIST_PER_PAGE_VALUES]': '5,10,15',
            'configuration[PRODUCT_LIST_PER_PAGE]': '5',
            'configuration[PRODUCT_LIST_SHORT_DESCRIPTION_LENGTH]': '150',
            'configuration[PRODUCT_NAME_MAX_LENGTH]': '50',
            'configuration[PRODUCT_NAME_SIDEBAR_MAX_LENGTH]': '20',
            'configuration[REVIEW_CONTENT_MAX_LENGTH]': '150',
            'configuration[REVIEW_LIMIT]': '10',
            'configuration[REVIEW_CONTENT_SIDEBAR_MAX_LENGTH]': '100',
            'configuration[REVIEW_SIDEBAR_LIMIT]': '5',
            'configuration[PRODUCT_LIST_SHOW_FILTER]': '1',
            'configuration[PRODUCT_SHOW_SAVE_OFF]': '1',
            'configuration[PRODUCT_SIDEBAR_SHOW_SAVE_OFF]': '1',
            'configuration[PRODUCT_PAGE_SHOW_SAVE_OFF]': '1',
            'configuration[ALSO_PURCHASED_LIMIT]': '4',
            'configuration[ALSO_PURCHASED_PER_ROW]': '4',
            'configuration[ALSO_PURCHASED_SIDEBAR_LIMIT]': '3',
            'configuration[BESTSELLERS_IDS]': ssss[0] + ',' + ssss[1] + ',' + ssss[2] + ',' + ssss[3] + ',' + ssss[
                4] + ',' + ssss[5] + ',' + ssss[6] + ',' + ssss[7] + ',' + ssss[8] + ',' + ssss[9] + ',' + ssss[
                                                  10] + ',' + ssss[11],
            'configuration[BESTSELLERS_SKUS]': '',
            'configuration[BESTSELLERS_LIMIT]': '15',
            'configuration[BESTSELLERS_PER_ROW]': '4',
            'configuration[BESTSELLERS_SIDEBAR_LIMIT]': '3',
            'configuration[BESTSELLERS_PAGE_LIMIT]': '30',
            'configuration[FEATURED_IDS]': '',
            'configuration[FEATURED_SKUS]': '',
            'configuration[FEATURED_LIMIT]': '12',
            'configuration[FEATURED_PER_ROW]': '4',
            'configuration[FEATURED_SIDEBAR_LIMIT]': '3',
            'configuration[FEATURED_PAGE_LIMIT]': '30',
            'configuration[NEW_PRODUCTS_IDS]': '',
            'configuration[NEW_PRODUCTS_SKUS]': '',
            'configuration[NEW_PRODUCTS_LIMIT]': '0',
            'configuration[NEW_PRODUCTS_PER_ROW]': '4',
            'configuration[NEW_PRODUCTS_SIDEBAR_LIMIT]': '3',
            'configuration[NEW_PRODUCTS_PAGE_LIMIT]': '30',
            'configuration[RECENT_VIEWED_LIMIT]': '4',
            'configuration[RECENT_VIEWED_PER_ROW]': '4',
            'configuration[RECENT_VIEWED_SIDEBAR_LIMIT]': '3',
            'configuration[RELATED_SHOW]': '1',
            'configuration[RELATED_LIMIT]': '3',
            'configuration[RELATED_PER_ROW]': '3',
            'configuration[RELATED_SIDEBAR_LIMIT]': '3',
            'configuration[SPECIALS_IDS]': '',
            'configuration[SPECIALS_SKUS]': '',
            'configuration[SPECIALS_LIMIT]': '8',
            'configuration[SPECIALS_PER_ROW]': '4',
            'configuration[SPECIALS_SIDEBAR_LIMIT]': '3',
            'configuration[SPECIALS_PAGE_LIMIT]': '30',
            'configuration[ORDERED_PRODUCTS_IDS]': '',
            'configuration[ORDERED_PRODUCTS_SKUS]': '',
            'configuration[ORDERED_PRODUCTS_LIMIT]': '8',
            'configuration[ORDERED_PRODUCTS_PER_ROW]': '4',
            'configuration[ORDERED_PRODUCTS_SIDEBAR_LIMIT]': '3',
            'configuration[RECENT_ORDERS_SIDEBAR_LIMIT]': '10',
            'configuration[PRODUCT_FILTER_1]': 'Filter 1',
            'configuration[PRODUCT_FILTER_2]': 'Filter 2',
            'configuration[PRODUCT_FILTER_3]': 'Filter 3',
            'configuration[PRODUCT_FILTER_4]': 'Filter 4',
            'configuration[PRODUCT_FILTER_5]': 'Filter 5',
            'configuration[PRODUCT_FILTER_6]': 'Filter 6',
            'configuration[PRODUCT_FILTER_7]': 'Filter 7',
            'configuration[PRODUCT_FILTER_8]': 'Filter 8',
            'configuration[PRODUCT_FILTER_9]': 'Filter 9',
            'configuration[PRODUCT_FILTER_10]': 'Filter 10',
            'configuration[PRODUCT_FILTER_11]': 'Filter 11',
            'configuration[PRODUCT_FILTER_12]': 'Filter 12',
            'configuration[PRODUCT_FILTER_13]': 'Filter 13',
            'configuration[PRODUCT_FILTER_14]': 'Filter 14',
            'configuration[PRODUCT_FILTER_15]': 'Filter 15',
            'configuration[PRODUCT_FILTER_16]': 'Filter 16',
            'configuration[PRODUCT_FILTER_17]': 'Filter 17',
            'configuration[PRODUCT_FILTER_18]': 'Filter 18',
            'configuration[PRODUCT_FILTER_19]': 'Filter 19',
            'configuration[PRODUCT_FILTER_20]': 'Filter 20',
        }

        self.session.post(url='https://' + self.url + '/configuration.php?gID=3&action=save',
                                          data=canpingyouhua_data, headers=self.req_header)

    def faq(self):
        """
        常见问题
        """
        Faq_link = 'https://' + self.url + '/cms_page.php?action=save'
        data = Faq_sql.query.order_by(func.random()).limit(1).first()
        Faq_data = {
            'securityToken': self.securityToken,
            'cms_page[cms_page_id]': '7',
            'cms_page[name]': 'Faq',
            'cms_page[content]': data.name,
            'cms_page[meta_title]': 'Faq',
            'cms_page[meta_keywords]': '',
            'cms_page[meta_description]': '',
            'cms_page[status]': '1',
            'cms_page[sort_order]': '70'
        }

        self.session.post(url=Faq_link, data=Faq_data, headers=self.req_header)

    def delivery_methods(self):
        """
        送货
        """
        songhuofanshi_link = 'https://' + self.url + '/cms_page.php?action=save'
        data = PaymentMethods_sql.query.order_by(func.random()).limit(1).first()
        songhuofanshi_data = {
            'securityToken': self.securityToken,
            'cms_page[cms_page_id]': '4',
            'cms_page[name]': 'Shipping & Delivery',
            'cms_page[content]': data.name,
            'cms_page[meta_title]': 'Shipping & Delivery',
            'cms_page[meta_keywords]': '',
            'cms_page[meta_description]': '',
            'cms_page[status]': '1',
            'cms_page[sort_order]': '40'
        }
        self.session.post(url=songhuofanshi_link, data=songhuofanshi_data, headers=self.req_header)

    def delivery_and_returns(self):
        """
        退货
        """
        data = ReturnPolicy_sql.query.order_by(func.random()).limit(1).first()
        tuihuo_link = 'https://' + self.url + '/cms_page.php?action=save'
        tuihuo_data = {
            'securityToken': self.securityToken,
            'cms_page[cms_page_id]': '5',
            'cms_page[name]': 'Return Policy',
            'cms_page[content]': data.name,
            'cms_page[meta_title]': 'Return Policy',
            'cms_page[meta_keywords]': '',
            'cms_page[meta_description]': '',
            'cms_page[status]': '1',
            'cms_page[sort_order]': '50'
        }

        self.session.get(url=tuihuo_link,data=tuihuo_data,headers=self.req_header)

    def about_us(self):
        """
        关于我们
        """
        data = About_sql.query.order_by(func.random()).limit(1).first()
        url = 'https://' + self.url + '/cms_page.php?action=save'
        data = {
            'securityToken': self.securityToken,
            'cms_page[cms_page_id]': '1',
            'cms_page[name]': 'About Us',
            'cms_page[content]': data.name,
            'cms_page[meta_title]': 'About Us',
            'cms_page[meta_keywords]': '',
            'cms_page[meta_description]': '',
            'cms_page[status]': '1',
            'cms_page[sort_order]': '10'
        }
        self.session.post(url=url, data=data, headers=self.req_header)

    def privacy_security(self):
        """
        隐私安全
        """
        data = PrivacySecurity_sql.query.order_by(func.random()).limit(1).first()
        yingsianquan_link = 'https://' + self.url + '/cms_page.php?action=save'
        yingsianquan_data = {
            'securityToken': self.securityToken,
            'cms_page[cms_page_id]': '3',
            'cms_page[name]': 'Privacy & Security',
            'cms_page[content]': data.name,
            'cms_page[meta_title]': 'Privacy & Security',
            'cms_page[meta_keywords]': '',
            'cms_page[meta_description]': '',
            'cms_page[status]': '1',
            'cms_page[sort_order]': '30'
        }
        self.session.post(url=yingsianquan_link, data=yingsianquan_data, headers=self.req_header)

    def calculation_method(self):
        """
        运送方式
        """
        url = 'https://www.'+ self.url+ '/shipping_method.php?action=save'
        data = {
            "securityToken": self.securityToken,
            "shipping_method[shipping_method_id]": "2",
            "shipping_method[code]": "standard",
            "shipping_method[name]": "Standard Shipping",
            "shipping_method[description]": "",
            "shipping_method[fee]": '%d.0000' % random.sample([8, 9, 10, 11, 12, 13, 8.9, 9.9, 10.9, 11.9, 12.9, 14, 15],1)[0],
            "shipping_method[max_fee]": "0.0000",
            "shipping_method[insurance_fee]": "0.0000",
            "shipping_method[free_shipping_qty]": "0",
            "shipping_method[free_shipping_amount]": '%d.0000' % random.sample([49,59, 69, 79, 89,99],1)[0],
            "shipping_method[free_shipping_country]": "",
            "shipping_method[status]": "1",
            "shipping_method[is_item]": "0",
            "shipping_method[sort_order]": "20",
        }
        self.session.post(url=url,data=data,headers=self.req_header)

    def clean_up_data(self):
        """
        最后清理数据
        """
        for i in self.r.smembers('url'):
            url = i.split(',')[0]
            if url == self.url:
                self.r.srem('url',i)
        r.set(self.url,self.session.cookies.values()[0])
        r.expire(self.url, 86400)

    def run(self):
        self.csv()  # 配置产品分类表
        if r.get(self.url):
            self.session.cookies.set('PHPSESSID',r.get(self.url))
        else:
            self.landed()  # 登录
        self.clear_data() # 清楚数据
        self.upload() # 上传数据
        self.basic_settings() # 基本设置
        self.product_list() # 产品列表
        self.faq() # 常见问题
        self.delivery_methods() # 交付方法
        self.delivery_and_returns() # 送货与退货
        self.about_us() # 关于我们
        self.privacy_security() # 隐私安全
        self.calculation_method() # 运送方式
        self.clean_up_data() # 清除