from bs4 import BeautifulSoup as BS
import requests
import openpyxl
import warnings
warnings.filterwarnings("ignore")

import warnings
def fxn():
    warnings.warn("deprecated", DeprecationWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def get_links(html):
    soup = BS(html, 'html.parser')
    links = []
    main_content = soup.find('div', class_='search-results-table')
    posts = main_content.find_all('div', class_='list-item list-label')
    for post in posts:
        link = post.find('a').get('href')
        full_link = "https://www.mashina.kg" + link
        links.append(full_link)
    return links


def get_posts(html):
    soup = BS(html, 'html.parser')
    main_content = soup.find('div', class_='content-wrapper details-wrapper clr')
    title = main_content.find('div', class_='head-left').find('h1').text.strip()
    sale = 'Продажа '
    no_sale_title = title.replace(sale, "")
    price_dollar = main_content.find('div', class_='price-dollar').text.strip()
    price_som = main_content.find('div', class_='price-som').text.strip()#.replace(' сом', "")
    phone_number = main_content.find('div', class_='number').text.strip()
    characteristics = main_content.find_all('div', class_='field-row clr')
    for characteristic in characteristics[0:4]:
        label = characteristic.find('div', class_='field-label').text.strip()
        value = characteristic.find('div', class_='field-value').text.strip()
        print(f'{label} -- {value}')
    print(f'{no_sale_title}\n{price_dollar}\n{price_som}\n{phone_number}')
    # data = {
    #     'title': no_sale,
    #     'price_dollar': price_dollar,
    #     'price_som': price_som,
    #     'phone_number': phone_number,
    # }
    #   return data

# def save_to_excel(data):
#     wb = openpyxl.Workbook()
#     sheet = wb.active
#     sheet['A1'] = 'Название'
#     sheet['B1'] = 'Цена USD'
#     sheet['C1'] = 'Цена KGZ'
#     sheet['D1'] = 'Номер продавца'

    
#     for i,item in enumerate(data,2):
#         sheet[f'A{i}'] = item['title']
#         sheet[f'B{i}'] = item['price_dollar']
#         sheet[f'C{i}'] = item['price_som']
#         sheet[f'D{i}'] = item['phone_number']
        
#     wb.save('cars.xlsx')


def get_last_page(html):
    soup = BS(html, 'html.parser')
    main_content = soup.find('div', class_='search-results clr')
    pagination = main_content.find('ul', class_='pagination')
    last = pagination.find('a', class_='page-link', text='Последняя') 
    last_page = last.get("data-page")
    return int(last_page)


def main():
    URL = 'https://www.mashina.kg/search'
    html = get_html(URL)
    last_page = get_last_page(html)

    for i in range(1,last_page):
        page_url = f'{URL}/?page={i}'
        page = get_html(page_url)
        links = get_links(page)
        data = []

        for link in links:
            detail_html = get_html(link)
            get_posts(detail_html)
        # save_to_excel(data)

if __name__ == '__main__':
    main()