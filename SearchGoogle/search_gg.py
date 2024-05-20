import requests
import SearchGoogle.config as cfg
from bs4 import BeautifulSoup


def get_facebook_result_by_ggsearch(phrase, period):
    url = cfg.url_gg_search 
    start_cur=0
    params = {
    'q': f'site:facebook.com "{phrase}"',
    'tbs': f'qdr:{period}',
    'start':f'{start_cur}'
}
    proxies = {
        "http": "http://172.168.201.4:34007",
        "https": "http://172.168.201.4:34007"
    }
    response = requests.get(url, params=params, proxies=proxies, headers=cfg.headers)
    # response = requests.get(url, proxies=cfg.proxies, headers=cfg.headers)
    # response = requests.get(url, params=params, headers=cfg.headers)
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    # Iterate through search results
    for i, g in enumerate(soup.find_all('div', class_='tF2Cxc')):
        # Extract link, title, and snippet (if available)
        link = g.find('a')['href']
        # Append result to list
        results.append(link)
        # Limit to 100 results
        if i == 50:
            break
    for i, g in enumerate(soup.find_all('div', class_='PmEWq')):
        # Extract link, title, and snippet (if available)
        link = g.find('a')['href']
        # Append result to list
        results.append(link)
        # Limit to 100 results
        if i == 50:
            break
    for i, g in enumerate(soup.find_all('div', class_='yuRUbf')):
        # Extract link, title, and snippet (if available)
        link = g.find('a')['href']
        # Append result to list
        results.append(link)
        # Limit to 100 results
        if i == 50:
            break
    
    return results


def get_youtube_result_by_ggsearch(phrase, period):
    url = cfg.url_gg_search 
    params = {
    'q': f'"{phrase}"',
    'tbs': f'qdr:{period},srcf:H4sIAAAAAAAAANOuzC8tKU1K1UvOz1UryMnXK8tTK8nMLsnPBouUlOZnlhSlgkTTEpNTk_1Kh4imJeSVFmSAmSAoA5e4MJ0UAAAA',
    'tbm': 'vid',
}
    proxies = {
        "http": "http://172.168.201.4:34007",
        "https": "http://172.168.201.4:34007"
    }
    response = requests.get(url, proxies=proxies, headers=cfg.headers)
    # response = requests.get(url, params=params, headers=cfg.headers)
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    # Iterate through search results
    for i, g in enumerate(soup.find_all('div', class_='PmEWq')):
        # Extract link, title, and snippet (if available)
        link = g.find('a')['href']
        # Append result to list
        results.append(link)
        # Limit to top 10 results
        if i == 100:
            break
    return results


def get_tiktok_result_by_ggsearch(phrase, period):
    BOOL=True
    url = cfg.url_gg_search 
    start_cur = 0
    results = []
    while BOOL:
        params = {
                    'q': f'"{phrase}"',
                    'tbs': f'qdr:{period},srcf:H4sIAAAAAAAAAC3KQQqAMAwF0dt0I_1ROaY0aapIqPwVvLxV3A28eD0ThXF0TRj-on0HIw9ICafD2yRVku5Eqr0ITES64eeZGlYv_14wvfk_1x6TwAAAA',
                    'tbm': 'vid',
                    'start': f'{start_cur}' 
}
        proxies = {
                "http": "http://172.168.201.4:34006",
                "https": "http://172.168.201.4:34006"
            }
        response = requests.get(url, params=params, headers=cfg.headers, proxies=proxies)
        # response = requests.get(url, proxies=cfg.proxies, headers=cfg.headers)
        # response = requests.get(url, params=params, headers=cfg.headers)
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Iterate through search results
        for i, g in enumerate(soup.find_all('div', class_='PmEWq')):
            # Extract link, title, and snippet (if available)
            link = g.find('a')['href']
            # Append result to list
            if link not in results:
                if 'video' in link:
                    results.append(link)
            # Limit to top 10 results
        if len(results) >= 50:
            break
        elif start_cur >= 50:
            break
        else:
            start_cur += 10
    return results

# print(get_tiktok_result_by_ggsearch("Bà Trương Mỹ Lan tử hình", period="d"))
# print(len(get_tiktok_result_by_ggsearch("Bà Trương Mỹ Lan tử hình", period="d")))