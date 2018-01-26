#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from app.OK_Utils import *
except Exception as e:
    from OK_Utils import *


class Ok_Services:

    def __init__(self):

        #为了账户的安全性，API_KEY和SECRET_KEY取环境变量的值
        if 'API_KEY' in os.environ:
            OK_PARAMS['api_key'] = os.environ['API_KEY']
        if 'SECRET_KEY' in os.environ:
            OK_PARAMS['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.utils = OK_Utils(OK_PARAMS)
        print(self.utils.params)


    def get_accounts(self):
        pass

    def get_balance(self):
        pass

    def get_depth(self,symbol):
        '''
        获取OKEX币币市场深度
        :param symbol:
        :return:
        '''
        path = OK_API['DEPTH'][0]
        params = {'symbol': symbol}

        return self.utils.api_key_get(params, path)

    def get_ticker(self,symbol):
        '''
        #获取OKex币币市场行情
        :param symbol:
        :return:
        '''
        path = OK_API['TICKER'][0]
        params = {'symbol': symbol}

        return self.utils.api_key_get(params,path)

    def get_trade_detail(self,symbol,start_date='',end_date=''):
        '''
        获取OKex币币交易信息(600条)
        :param symbol:
        :param start_date:
        :param end_date:
        :return:
        '''
        path = OK_API['TRADES'][0]
        params = {'symbol': symbol}

        return self.utils.api_key_get(params,path)

    def get_kline(self,symbol,period,size = 60):
        '''
        获取OKex币币K线数据 每个周期条数2000左右
        :param symbol:
        :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
        :param size:
        :return:
        '''
        path = OK_API['KLINE'][0]
        params = {'symbol': symbol,
                  'type':period
                  }
        return self.utils.api_key_get(params,path)
    #----------------------------合约行情信息---------------------#

    def get_future_ticker(self,symbol,contract_type='this_week'):
        '''
        #获取Okex合约账户信息（全仓）
        :param symbol:
        :param contract_type:
        :return:
        '''
        path = OK_API['F_TICKER'][0]
        params = {'symbol': symbol,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_get(params,path)

    def get_future_depth(self,symbol,contract_type='this_week'):
        '''
        #获取OKex 合约深度信息
        :param symbol:
        :param contract_type:
        :return:
        '''
        path = OK_API['F_DEPTH'][0]
        params = {'symbol': symbol,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_get(params, path)

    def get_future_trades(self,symbol,contract_type='this_week'):
        """
        获取OKex合约成交信息
        :param symbol:
        :param contract_type:
        :return:
        """
        path = OK_API['F_TRADES'][0]
        params = {'symbol': symbol,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_get(params, path)

    def get_future_index(self,symbol):
        '''
        #获取OKEX合约指数信息
        :param symbol:
        :return:
        '''
        path = OK_API['F_INDEX'][0]
        params = {'symbol': symbol}
        return self.utils.api_key_get(params, path)

    def get_exchange_usdcnyrate(self):
        '''
        #获取美元人民币汇率
        :return:
        '''
        path = OK_API['EXCHANGE_RATE'][0]
        params = {}
        return self.utils.api_key_get(params, path)

    def get_future_estimated_price(self,symbol):
        '''
        #获取交割预估价
        :param symbol:
        :return:
        '''
        path = OK_API['F_EST_PRICE'][0]
        params = {'symbol':symbol}
        return self.utils.api_key_get(params, path)

    def get_future_kline(self,symbol,period,size=60,contract_type='this_week'):
        '''
        #获取虚拟合约的K线数据
        :param symbol:
        :param period:
        1min : 1分钟, 3min : 3分钟, 5min : 5分钟,15min : 15分钟,30min : 30分钟
        1day : 1日,3day : 3日,1week : 1周
        1hour : 1小时,2hour : 2小时,4hour : 4小时,6hour : 6小时,12hour : 12小时
        :param contract_type:
        :return:
        '''
        path = OK_API['F_KLINE'][0]
        params = {'symbol': symbol,
                  'type': period,
                  'size':size,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_get(params, path)

    def get_future_hold_amount(self,symbol,contract_type='this_week'):
        '''
        #获取当前可用合约总持仓量
        :param symbol:
        :param contract_type:
        :return:
        '''
        path = OK_API['F_H_AMOUNT'][0]
        params = {'symbol': symbol,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_get(params, path)

    def get_future_price_limit(self,symbol,contract_type='this_week'):
        '''
        #获取合约最高限价和最低限价
        :param symbol:
        :param contract_type:
        :return:
        '''
        path = OK_API['F_PRICE_LIMIT'][0]
        params = {'symbol': symbol,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_get(params, path)

    #------------------------------币币交易部分------------------------#

    def get_userinfo(self):
        '''
        #获取用户信息
        :return:
        '''
        path = OK_API['USERINFO'][0]
        params = {}

        return self.utils.api_key_post(params,path)

    def send_order(self,symbol,type,amount,price):
        '''
        #发送订单
        :param symbol:
        :param type：买卖类型： 限价单（buy/sell） 市价单（buy_market/sell_market）
        :param amount:
        :param price:
        :return:
        '''
        path = OK_API['TRADE'][0]
        params = {'symbol':symbol,
                  'type':type,
                  'price':price,
                  'amount':amount
                  }
        return self.utils.api_key_post(params, path)

    def send_batch_orders(self,symbol,type,order_data):
        '''
        #币币交易批量下单
        :param symbol:
        :param type:买卖类型： 限价单（buy/sell）
        :param order_data:最大下单量为5， price和amount参数参考trade接口中的说明，最终买卖类型由orders_data 中type 为准，如orders_data不设定type 则由上面type设置为准。
        :return:
        '''

        path = OK_API['BATCH_TRADE'][0]
        params = {'symbol': symbol,
                  'type': type,
                  'order_data': order_data
                  }
        return self.utils.api_key_post(params, path)

    def cancel_order(self,symbol,order_id):
        '''
        #撤销订单
        :param symbol:
        :param order_id:订单ID(多个订单ID中间以","分隔,一次最多允许撤消3个订单)
        :return:
        '''
        path = OK_API['CANCEL_ORDER'][0]
        params = {'symbol': symbol,
                  'order_id': order_id
                  }
        return self.utils.api_key_post(params, path)

    def get_order_info(self,symbol,order_id):
        '''
        #获取用户的订单信息
        :param symbol:
        :param order_id:
        :return:
        '''
        path = OK_API['ORDER_INFO'][0]
        params = {'symbol': symbol,
                  'order_id': order_id
                  }
        return self.utils.api_key_post(params, path)

    def get_order_list(self,symbol,type,order_id):
        '''
        批量获取用户订单
        :param symbol:
        :param type:查询类型 0:未完成的订单 1:已经完成的订单
        :param order_id:订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
        :return:
        '''
        path = OK_API['ORDERS_INFO'][0]
        params = {'symbol': symbol,
                  'type':type,
                  'order_id': order_id
                  }
        return self.utils.api_key_post(params, path)

    def get_order_history(self,symbol,status=0,current_page=1,page_length=100):
        '''
        #获取历史订单信息，只返回最近两天的信息
        :param symbol:
        :param status:查询状态 0：未完成的订单 1：已经完成的订单 （最近两天的数据）
        :param current_page:当前页数
        :param page_length:每页数据条数，最多不超过200
        :return:
        '''
        path = OK_API['ORDER_HISTORY'][0]
        params = {'symbol': symbol,
                  'status': status,
                  'current_page': current_page,
                  'page_length':page_length
                  }
        return self.utils.api_key_post(params, path)

    def withdraw(self,symbol,withdraw_address,withdraw_amount,trade_pwd,chargefee,target):
        '''
        提币BTC/LTC/ETH/ETC/BCH
        :param symbol:btc_usd:比特币    ltc_usd :莱特币    eth_usd :以太坊     etc_usd :以太经典    bch_usd :比特现金
        :param withdraw_address:认证的地址、邮箱 或手机号码
        :param withdraw_amount:提币数量 BTC>=0.01 LTC>=0.1 ETH>=0.1 ETC>=0.1 BCH>=0.1
        :param trade_pwd:交易密码
        :param chargefee:网络手续费 >=0
                        BTC范围 [0.002，0.005]
                        LTC范围 [0.001，0.2]
                        ETH范围 [0.01]
                        ETC范围 [0.0001，0.2]
                        BCH范围 [0.0005，0.002]
                        手续费越高，网络确认越快，OKCoin内部提币设置0
        :param target:地址类型 okcn：国内站 okcom：国际站 okex：OKEX address：外部地址
        :return:
        '''
        path = OK_API['WITHDRAW'][0]
        params = {'symbol': symbol,
                  'withdraw_address': withdraw_address,
                  'withdraw_amount': withdraw_amount,
                  'trade_pwd': trade_pwd,
                  'chargefee':chargefee,
                  'target':target
                  }
        return self.utils.api_key_post(params, path)

    def cancel_withdraw(self,symbol,withdraw_id):
        '''
        取消提币BTC/LTC/ETH/ETC/BCH
        :param symbol:btc_usd:比特币    ltc_usd :莱特币    eth_usd :以太坊     etc_usd :以太经典    bch_usd :比特现金
        :param withdraw:提币申请Id
        :return:
        '''
        path = OK_API['CANCEL_WITHDRAW'][0]
        params = {'symbol': symbol,
                  'withdraw_id': withdraw_id
                  }
        return self.utils.api_key_post(params, path)

    def get_withdraw_info(self,symbol,withdraw_id):
        '''

        :param symbol:查询提币BTC/LTC/ETH/ETC/BCH信息
        :param withdraw_id:提币申请Id
        :return:
        result:true表示请求成功
        address:提现地址
        amount:提现金额
        created_date:提现时间
        chargefee:网络手续费
        status:提现状态（-3:撤销中;-2:已撤销;-1:失败;0:等待提现;1:提现中;2:已汇出;3:邮箱确认;4:人工审核中5:等待身份认证）
        withdraw_id:提币申请Id
        '''

        path = OK_API['WITHDRAW_INFO'][0]
        params = {'symbol': symbol,
                  'withdraw_id': withdraw_id
                  }
        return self.utils.api_key_post(params, path)

    def get_account_records(self,symbol,type,current_page=1,page_length=50):
        '''
        #获取用户提现/充值记录
        :param symbol:btc, ltc, eth, etc, bch, usdt
        :param type:0：充值 1 ：提现
        :param current_page:当前页数
        :param page_length:每页数据条数，最多不超过50条
        :return:
        '''
        path = OK_API['ACCOUNT_RECORDS'][0]
        params = {'symbol': symbol,
                  'type': type,
                  'current_page':current_page,
                  'page_length':page_length
                  }
        return self.utils.api_key_post(params, path)

    #-----------------------------合约交易部分-------------------------#

    def get_future_userinfo(self):
        '''
        获取OKex合约账户信息（全仓，所有仓位）
        :return:
        '''
        path = OK_API['F_USERINFO'][0]
        params = {}

        return self.utils.api_key_post(params, path)

    def get_future_position(self,symbol,contract_type='this_week'):
        '''
        #获取用户持仓获取OKex合约账户信息（全仓）
        :param symbol:btc_usd   ltc_usd    eth_usd    etc_usd    bch_usd
        :param contract_type:合约类型: this_week:当周   next_week:下周   quarter:季度
        :return:
        '''
        path = OK_API['F_POSITION'][0]
        params = {'symbol':symbol,
                  'contract_type':contract_type
                  }
        return self.utils.api_key_post(params, path)

    def send_future_order(self,symbol,type,price,amount,match_price=1,lever_rate=20,contract_type = 'this_week'):
        '''
        #合约下单
        :param symbol: btc_usdt   ltc_usdt    eth_usdt    etc_usdt    bch_usdt
        :param type:1:开多   2:开空   3:平多   4:平空
        :param price:
        :param amount:委托数量
        :param match_price:是否为对手价 0:不是    1:是   ,当取值为1时,price无效
        :param lever_rate:杠杆倍数 value:10\20 默认10
        :param contract_type:合约类型: this_week:当周   next_week:下周   quarter:季度
        :return:
        '''
        path = OK_API['F_TRADE'][0]
        params = {'symbol': symbol,
                  'type': type,
                  'price': price,
                  'amount': amount,
                  'match_price': match_price,
                  'lever_rate': lever_rate,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_post(params, path)

    def send_future_batch_orders(self, symbol, orders_data, lever_rate=20, contract_type='this_week'):
        '''
        #合约账户批量下单
        :param symbol:btc_usdt   ltc_usdt    eth_usdt   etc_usdt    bch_usdt
        :param order_data:
        JSON类型的字符串
        例：[{price:5,amount:2,type:1,match_price:0},{price:2,amount:3,type:1,match_price:0}]
        最大下单量为5，price,amount,type,match_price参数参考future_trade接口中的说明
        :param lever_rate:杠杆倍数 value:10\20 默认10
        :param contract_type:this_week:当周   next_week:下周   quarter:季度
        :return:
        '''

        path = OK_API['F_BATCH_TRADE'][0]
        params = {'symbol': symbol,
                  'orders_data': orders_data,
                  'lever_rate': lever_rate,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_post(params, path)

    def get_future_trades_history(self,symbol,date,since):
        '''
        获取Okex合约交易历史(非个人）
        :param symbol:btc_usdt   ltc_usdt    eth_usdt    etc_usdt    bch_usdt
        :param date:合约交割时间，格式yyyy-MM-dd
        :param since:交易Id起始位置
        :return:
        '''
        path = OK_API['F_TRADES_HISTORY'][0]
        params = {'symbol': symbol,
                  'date': date,
                  'since': since
                  }
        return self.utils.api_key_post(params, path)

    def cancel_future_order(self,symbol,order_id,contract_type='this_week'):
        '''
        #取消合约订单
        :param symbol:
        :param order_id:
        :param contract_type:
        :return:
        '''
        path = OK_API['F_CANCEL'][0]
        params = {'symbol': symbol,
                  'order_id': order_id,
                  'contract_type': contract_type
                  }
        return self.utils.api_key_post(params, path)

    def get_future_order(self,symbol,order_id,status=1,current_page=1,page_length=1,contract_type='this_week'):
        '''
        #获取合约订单信息
        :param symbol:
        :param order_id:
        :param status:查询状态 1:未完成的订单 2:已经完成的订单
        :param current_page:当前页数
        :param page_length:每页获取条数，最多不超过50
        :param contract_type:
        :return:
        '''
        path = OK_API['F_ORDER_INFO'][0]
        params = {'symbol': symbol,
                  'order_id': order_id,
                  'status': status,
                  'page_length': page_length,
                  'current_page': current_page,
                  'contract_type': contract_type
                  }

        return self.utils.api_key_post(params, path)

    def get_future_order_list(self,symbol,order_id,contract_type='this_week'):
        '''
        #批量获取合约订单信息
        :param symbol:
        :param order_id:订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
        :param contract_type:合约类型: this_week:当周   next_week:下周   quarter:季度
        :return:
        '''
        path = OK_API['F_ORDERS_INFO'][0]
        params = {'symbol': symbol,
                  'order_id': order_id,
                  'contract_type': contract_type
                  }

        return self.utils.api_key_post(params, path)

    def get_future_userinfo_4fix(self):
        '''#获取逐仓合约账户信息
        '''
        path = OK_API['F_USDERINFO_4FIX'][0]
        params = {}

        return self.utils.api_key_post(params, path)

    def get_future_position_4fix(self,symbol,type=0,contract_type='this_week'):
        '''
        #逐仓用户持仓查询
        :param symbol:
        :param type:默认返回10倍杠杆持仓 type=1 返回全部持仓数据
        :param contract_type:合约类型: this_week:当周   next_week:下周   quarter:季度   （如不传入参数，则返回全部合约）
        :return:
        '''
        path = OK_API['F_POSITION_4FIX'][0]
        params = {'symbol':symbol,
                  'type':type,
                  'contract_type':contract_type
        }

        return self.utils.api_key_post(params, path)

    def get_future_explosive(self,symbol,status=0,current_page=1,page_number=0,page_length=1,contract_type='this_week'):
        '''
        #获取合约爆仓单
        :param symbol:
        :param status:状态 0：最近7天未成交 1:最近7天已成交
        :param current_page:当前页数索引值
        :param page_number:当前页数(使用page_number时current_page失效，current_page无需传)
        :param page_length:每页获取条数，最多不超过50
        :param contract_type:合约类型。this_week：当周；next_week：下周；quarter：季度
        :return:
        '''
        path = OK_API['F_EXPLOSIVE'][0]
        params = {'symbol': symbol,
                  'status': status,
                  'current_page':current_page,
                  'page_number':page_number,
                  'page_length':page_length,
                  'contract_type': contract_type
                  }

        return self.utils.api_key_post(params, path)

    def transfer_future_deposit(self,symbol,type,amount):
        '''
        #个人账户资金划转
        :param symbol:
        :param type:划转类型。OK_TRANSFER_TYPE['E2F'] 1：币币转合约 OK_TRANSFER_TYPE['F2E'] 2：合约转币币
        :param amount:划转币的数量
        :return:
        '''
        path = OK_API['F_DEVOLVE'][0]
        params = {'symbol': symbol,
                  'type': type,
                  'amount': amount,
                  }

        return self.utils.api_key_post(params, path)



if __name__ == '__main__':

    ok = Ok_Services()

    '''#1 get_depth 获取币币市场深度
    result = ok.get_depth('xrp_usdt')
    print(result['asks'][-5:-1])
    print(result['bids'][0:5])
    '''#1 get_depth 获取币币市场深度

    '''#2 get_ticker 获取币币市场行情
    result = ok.get_ticker('eth_usdt')
    print(result)
    '''#2 get_ticker 获取币币市场行情

    '''#3 get_trade_detail 获取币币市场交易信息
    result = ok.get_trade_detail('eth_usdt')
    print(result)
    '''#3 get_trade_detail 获取币币市场交易信息

    '''#4 get_kline 获取币币交易K线数据 每个周期数据条数2000左右
    result = ok.get_kline('eth_usdt','1min')
    print(result)
    '''#4 get_kline 获取币币交易K线数据 每个周期数据条数2000左右

    '''#5 get_future_ticker获取OKex合约行情数据
    result = ok.get_future_ticker('eth_usdt')
    print(result)
    '''#5 get_future_ticker获取OKex合约行情数据

    '''#6 get_future_depth 获取OKex合约深度信息
    result = ok.get_future_depth('eth_usdt')
    print(result)
    '''#6 get_future_depth 获取OKex合约深度信息

    '''#7 get_future_trades 获取OKex合约成交信息
    result = ok.get_future_trades('eth_usdt')
    print(result)
    '''#7 get_future_trades 获取OKex合约成交信息


    '''#8 get_future_index 获取OKex合约指数信息
    result = ok.get_future_index('eth_usdt')
    print(result)
    '''#8 get_future_index 获取OKex合约指数信息

    '''#9  get_exchange_usdcnyrate 获取美元人民币汇率
    result = ok.get_exchange_usdcnyrate()
    print(result)
    '''#9  get_exchange_usdcnyrate 获取美元人民币汇率

    '''#10 get_future_estimated_price获取交割预付价
    result = ok.get_future_estimated_price('eth_usdt')
    print(result)
    '''#10 get_future_estimated_price获取交割预付价

    '''#11 get_future_kline 获取虚拟合约的K线数据
    result = ok.get_future_kline('eth_usdt','1min')
    print(result)
    '''#11 get_future_kline 获取虚拟合约的K线数据

    '''#12 get_future_hold_amount 获取当前合约总持仓量
    result = ok.get_future_hold_amount('eth_usdt')
    print(result)
    '''#12 get_future_hold_amount 获取当前合约总持仓量

    '''#13 get_future_price_limit 获取合约最高限价和最低限价
    result = ok.get_future_price_limit('eth_usdt')
    print(result)
    '''#13 get_future_price_limit 获取合约最高限价和最低限价

    '''#14 get_userinfo 获取币币用户信息
    result = ok.get_userinfo()
    print(result['info']['funds']['borrow'])
    print(type(result['info']['funds']['borrow']))
    '''#14 get_userinfo 获取币币用户信息

    '''#16 Get_future_userinfo 获取合约账户信息
    result = ok.get_future_userinfo()
    print(result)
    '''#16 Get_future_userinfo 获取合约账户信息

    '''#17 get_future_position获取用户持仓获取OKex合约帐户信息（全仓）
    result = ok.get_future_position('eth_usdt')
    print(result)
    '''#17 get_future_position 获取用户持仓获取OKex合约帐户信息（全仓）

    '''#18 send_future_order合约账户下单
    result = ok.send_future_order('eth_usdt',OK_ORDER_TYPE['KD'],1000.000,1)
    print(result)
    '''#18 send_future_order合约账户下单

    '''#19 send_future_batch_orders合约账户批量下单
    orders_data=[{'price':1000.000,'amount':1,'type':OK_ORDER_TYPE['KD'],'match_price':0},
                 {'price':1001.000,'amount':2,'type':OK_ORDER_TYPE['KD'],'match_price':0}]
    result = ok.send_future_batch_orders('eth_usdt',orders_data)
    print(result)
    '''#19 send_future_batch_orders合约账户批量下单

    '''#20 cancel_future_order 取消合约订单
    result = ok.cancel_future_order('eth_usdt',result['order_id'])
    print(result)
    '''#20 cancel_future_order 取消合约订单

    '''#21 get_future_order 获取合约订单信息
    result = ok.get_future_order('eth_ust',result['order_id'])
    print(result)
    '''#21 get_future_order 获取合约订单信息

    '''#22 get_future_order_list 批量获取合约订单用户
    result = ok.get_future_order_list('eth_usdt','')
    print(result)
    '''#22 get_future_order_list 批量获取合约订单用户

    '''#23 get_future_userinfo_4fix获取逐仓合约账户信息
    result = ok.get_future_userinfo_4fix()
    print(result)
    '''#23 get_future_userinfo_4fix获取逐仓合约账户信息

    '''#24 get_future_explosive 获取合约爆仓单
    result = ok.get_future_explosive('eth_usdt')
    print(result)
    '''#24 get_future_explosive 获取合约爆仓单

    '''#25 transfer_future_deposit #个人账户资金划转
    result = ok.transfer_future_deposit('eth_usdt',OK_TRANSFER_TYPE['F2E'],0.2)
    print(result)
    '''#25 transfer_future_deposit #个人账户资金划转

    '''#26 send_order #币币交易下订单
    result = ok.send_order('eth_usdt',OK_ORDER_TYPE['SL'],0.1,1500)
    print(result)
    '''#26 send_order #币币交易下订单

    '''#27 cancel_order 取消币币交易订单
    result = ok.cancel_order('eth_usdt', result['orders'][0]['order_id'])
    print(result)
    '''#27 cancel_order 取消币币交易订单

    '''#28 get_order_info 获取订单信息
    result = ok.get_order_info('eth_usdt','')
    print(result)
    '''#28 get_order_info 获取订单信息

    '''#29 获取历史订单信息，只返回最近两天的信息
    result = ok.get_order_history('eth_usdt')
    print(result['orders'][0]['order_id'])
    '''#29 获取历史订单信息，只返回最近两天的信息

    '''#30 get_account_records 获取账户充值提现记录数据
    result =ok.get_account_records('eth',0)
    print(result)
    '''#30 get_account_records 获取账户充值提现记录数据