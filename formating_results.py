def format_search_results(search_results):
    names = ''
    ids =  ''
    for titles in search_results:
        names = f"{names}{titles.get('name')}\n"
        ids = f"{ids}{titles.get('animeid')}\n"
    names = names.split('\n')
    ids = ids.split('\n')
    names.pop(-1)
    ids.pop(-1)
    return (names, ids)

def format_download_results(download_results):
    qualitys = list(download_results)
    links = []
    for i in qualitys:
        links.append(download_results.get(i))
    result = ''
    for i in range(len(links)):
        result = f'{result}[{qualitys[i]}]({links[i]})\n'

    return result

def format_home_results(home_results):
    names = []
    animeid = []
    epnum = []
    for i in home_results:
        names.append(i.get('name'))
        animeidep = (i.get('Id-Epnum'))
        animeidep = animeidep.split('-')
        ids = animeidep[:-2]
        animeid.append('-'.join(ids))
        epnum.append(animeidep[-1])
    return (names, animeid, epnum)
