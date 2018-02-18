# coding=utf-8


def status_to_value(status_str):
    """确定域名状态值,将域名状态转换成状态值

    Args:
        status_str (string): 域名状态字符串

    Returns:
        string: 域名状态值数组
    """

    # 状态值字典
    status_dict = {
        # EPP
        'ADDPERIOD': '1',
        'AUTORENEWPERIOD': '2',
        'INACTIVE': '3',
        'OK': '4',
        'PENDINGCREATE': '5',
        'PENDINGDELETE': '6',
        'PENDINGRENEW': '7',
        'PENDINGRESTORE': '8',
        'PENDINGTRANSFER': '9',
        'PENDINGUPDATE': '10',
        'REDEMPTIONPERIOD': '11',
        'RENEWPERIOD': '12',
        'SERVERDELETEPROHIBITED': '13',
        'SERVERHOLD': '14',
        'SERVERRENEWPROHIBITED': '15',
        'SERVERTRANSFERPROHIBITED': '16',
        'SERVERUPDATEPROHIBITED': '17',
        'TRANSFERPERIOD': '18',
        'CLIENTDELETEPROHIBITED': '19',
        'CLIENTHOLD': '20',
        'CLIENTRENEWPROHIBITED': '21',
        'CLIENTTRANSFERPROHIBITED': '22',
        'CLIENTUPDATEPROHIBITED': '23',
        # RRP
        'ACTIVE': '24',
        'REGISTRYLOCK': '25',
        'REGISTRARLOCK': '26',
        'REGISTRYHOLD': '27',
        'REGISTRARHOLD': '28',
        'NOTEXIST': '29',  # 域名不存在
        'NOSTATUS': '30',  # 无状态值
        'CONNECT': '31'  # de服务器状态
    }
    
    return status_dict[status_str.upper()]
