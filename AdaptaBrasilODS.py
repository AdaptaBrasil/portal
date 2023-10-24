import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path('.').absolute().parent))
import src.layers.py.python.sismoi_commons as sisCommons

url_base = 'https://sistema.adaptabrasil.dev.apps.rnp.br'
url_base = 'https://sistema.adaptabrasil.mcti.gov.br/'

def odsMetas():
    df = pd.read_sql(f"""select h.id, title, ods, ods_group, min_year, sep_id,
    targets, resolution, s.name as sep_name, o.name as ods_group_name
    from {sisCommons.rds['defaultSchema']}.mv_hierarchy h
    left join {sisCommons.rds['defaultSchema']}.sep s 
    on h.sep_id = s.id
    left join {sisCommons.rds['defaultSchema']}.ods_group o 
    on h.ods_group = o.id
    where (level = 0 or indicator_id_master is not null) and ods is not null
    order by sep_id,cast(ods_group as int),level,simple_description""",
                     sisCommons.connectDB())
    sep = 0
    ods_group = -1
    Html = '<h1>Descrição Completa dos Indicadores</h1>'
    count = 0
    for _, row in df.iterrows():
        try:
            if not (row.ods == row.ods) or (row.ods == ''):  # test null
                continue
            if not (row.min_year == row.min_year):  # nan
                continue
            if row.ods_group != row.ods_group:  # test null
                continue
            if row.sep_id != sep:
                Html += '<h2>{0}</h2>\r\r\r'.format(row.sep_name)
                sep = row.sep_id
            if row.ods_group != ods_group:
                Html += '<h3>{0}</h3>\r\r\r'.format(row.ods_group_name)
                ods_group = int(row.ods_group)
            print(row.id, ';', row.title)
            to = row.title
            addSuffix = not f'{row.ods_group_name}' in to
            if addSuffix:
                to += f' para {row.ods_group_name}'
            Html += f"""<ul><li><a href="{url_base}/{int(row['id'])}/1/{int(row['min_year'])}/null/BR/{row['resolution']}/" target="_blank">{to}</a>"""

            Html += f""": {'ODSs' if ',' in row.ods else 'ODS'}&nbsp;{row.ods} e {'Metas Nacionais' if ',' in row.targets else 'Meta Nacional'} {row.targets}.</li></ul>\r"""
        except Exception as e:
           print(e)
           raise e
    print(len(Html))
    htmlfile = open(r'd:\temp\ods_metas.html', 'w')
    htmlfile.write(Html)
    htmlfile.close()


def generalDescription():
    df = pd.read_sql(f"""select h.id, title, simple_description, level, ods, ods_group, min_year, sep_id,
    targets, resolution,  s.name as sep_name, o.name as ods_group_name 
    from {sisCommons.rds['defaultSchema']}.mv_hierarchy h
    left join {sisCommons.rds['defaultSchema']}.sep s 
    on h.sep_id = s.id
    left join {sisCommons.rds['defaultSchema']}.ods_group o 
    on h.ods_group = o.id   where level = 0 or indicator_id_master is not null
    order by sep_id,cast(ods_group as int),level,id""",
                     sisCommons.connectDB())
    sep = 0
    ods_group = -1
    level = 0
    Html = '<h1>Descrição Completa de Todos os Indicadores</h1>'
    for _, row in df.iterrows():
        try:
            if not (row.min_year == row.min_year):  # nan
                continue

            if row.sep_id != sep:
                Html += '<h2>{0}</h2>\r\r\r'.format(row.sep_name)
                sep = row.sep_id
            if (row.ods_group == row.ods_group) and (row.ods_group != ods_group):
                Html += '<h3>{0}</h3>\r\r\r'.format(row.ods_group_name)
                ods_group = int(row.ods_group)
            if row.level != level:
                Html += '<h4>Nível {0}</h4>\r\r\r'.format(row.level - 1)
                level = row.level
            print(row.id, ';', row.title)
            to = row['title']
            addSuffix = not f'{row.ods_group_name}' in to
            if addSuffix:
                to += f' para {row.ods_group_name}'
            Html += f"""<ul><li><a href="{url_base}/{int(row['id'])}/1/{int(row['min_year'])}/null/BR/{row['resolution']}/" target="_blank">{to}</a>: """
            Html += row.simple_description.replace('<b>', '') + \
                    '.</li></ul>\r'
        except Exception as e:
           print(e)
           raise e
    print(len(Html))
    htmlfile = open(r'd:\temp\indicadores.html', 'w')
    htmlfile.write(Html)
    htmlfile.close()


if __name__ == "__main__":
    odsMetas()
    generalDescription()
