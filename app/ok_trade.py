#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from app.OK_Services import *
except Exception as e:
    from OK_Services import *


class OK_MAKER:

    def __init__(self,params):
        self._params = params
        self._OKServices = Ok_Services()

    def get_price_depth(self,symbol):
        '''
        #获取市场行情深度
        :param symbol:
        :return:
        '''
        sell=0.0000
        buy = 0.0000
        try:
            result = self._OKServices.get_future_depth(symbol)
            sell = result['asks'][-1][0]  #获取卖二价
            buy = result['bids'][0][0]   #获取买二价
            #print(result['asks'][-5:-1])
            #print(result['bids'][0:5])
        except Exception as e:
            print('error:%s'%e)
            return buy,sell
        finally:
            return buy,sell

    def send_price(self,symbol,buy,sell):

        if sell - buy > 1:
            buy_order = self._OKServices.send_future_order(symbol, OK_ORDER_TYPE['KD'], buy + 0.001, 0.001)
            sell_order = self._OKServices.send_future_order(symbol, OK_ORDER_TYPE['KK'], sell - 0.001, 0.001)
        else:
            buy_order,sell_order=[]

        return buy_order,sell_order

    def deal_net_pot(self):
        print('test')

    def get_user_pot(self,symbol):
        '''
        获取用户仓位信息
        :param symbol:
        :return:
        '''
        result = self._OKServices.get_future_userinfo()

        return result['info'][symbol]

    def check_risk(self,symbol):
        '''
        检查系统风险，实现仓位控制
        :param symbol:
        :return:
        '''
        risk = self.get_net_pot(symbol)
        if risk['keep_deposit']/risk['account_rights'] <= self._params['risk_rate']:
            print('now risk is :%s,limit risk:%s'%(risk['keep_deposit']/risk['account_rights'],self._params['risk_rate']))
            return True
        else:
            print('now risk is :%s,limit risk:%s' % (risk['keep_deposit'] / risk['account_rights'], self._params['risk_rate']))
            return False

    def get_user_position(self,symbol,contract_type='this_week'):
        '''
        #获取仓位信息
        :param symbol:btc_usdt   ltc_usdt    eth_usdt    etc_usdt    bch_usdt
        :param contract_type:
        :return:
        '''
        result={}
        result['status']=False
        hold = self._OKServices.get_future_position(symbol,contract_type)
        if hold:
            result['buy_amount'] = hold['holding'][0]['buy_amount']
            result['buy_available']=hold['holding'][0]['buy_available']
            result['buy_cost'] = hold['holding'][0]['buy_price_cost']
            result['sell_amount'] = hold['holding'][0]['sell_amount']
            result['sell_available'] = hold['holding'][0]['sell_available']
            result['sell_cost'] = hold['holding'][0]['sell_price_cost']
            result['status'] = True
        else:
            result['status'] = False

        return result

    def get_ma_data(self,symbol,period='1min',size = 60,contract_type='this_week'):

        data={}
        data['status']=False
        ma={}
        sum_5=0.0000
        sum_10=0.0000
        sum_15=0.0000
        sum_30=0.0000
        sum_60=0.0000
        try:
            result = self._OKServices.get_future_kline(symbol,period,size,contract_type)
            if result:
                for i in range(0,size):
                    if i<5:
                        sum_5 = sum_5 + result[-1 - i][4]
                    if i<10:
                        sum_10 = sum_10 + result[-1 - i][4]
                    if i<15:
                        sum_15 = sum_15 + result[-1 - i][4]
                    if i<30:
                        sum_30 = sum_30+ result[-1 - i][4]
                    if i<60:
                        sum_60 = sum_60 + result[-1 - i][4]

                ma['price'] = round(result[-1][4],4)
                ma['ma5'] = round(sum_5/5,4)
                ma['ma10'] = round(sum_10/10,4)
                ma['ma15'] = round(sum_15/15,4)
                ma['ma30'] = round(sum_15 / 30, 4)
                ma['ma60'] = round(sum_15 / 60, 4)
                data['status'] = True
                data['data'] = ma
        except Exception as e:
            data['status']=False

        return data

    def get_trade_signal(self,symbol,period='1min',size = 60,contract_type='this_week'):

        result = ok_maker.get_ma_data(symbol, period,size) #获取均线数据
        if result['status']:

            if result['data']['price']>result['data']['ma10']:
                result['signal'] = 1

            if result['data']['price']<result['data']['ma10']:
                result['signal'] = -1

            '''
            if  result['data']['price']>result['data']['ma5'] and result['data']['ma5'] < result['data']['ma10']<result['data']['ma15']:#价格上出现变盘信号
                # print('当前趋势price,ma5:%s,ma10:%s,ma15:%s'%(result['data']['price'],result['data']['ma5'],result['data']['ma10'],result['data']['ma15']))
                result['signal'] = 1

            if result['data']['ma5']> result['data']['ma10'] and result['data']['ma10'] < result['data']['ma15']:
                # print('当前趋势price,ma5:%s,ma10:%s,ma15:%s'%(result['data']['price'],result['data']['ma5'],result['data']['ma10'],result['data']['ma15']))
                result['signal'] = 2
            if result['data']['price']>result['data']['ma5']> result['data']['ma10']>result['data']['ma15']:#当前趋势为上涨行情
                # print('当前趋势price,ma5:%s,ma10:%s,ma15:%s'%(result['data']['price'],result['data']['ma5'],result['data']['ma10'],result['data']['ma15']))
                result['signal'] = 3

            if result['data']['price']<result['data']['ma5'] and result['data']['ma5'] > result['data']['ma10']>result['data']['ma15']:#价格上出现变盘信号
                # print('当前趋势price,ma5:%s,ma10:%s,ma15:%s'%(result['data']['price'],result['data']['ma5'],result['data']['ma10'],result['data']['ma15']))
                result['signal'] = -1
            if result['data']['ma5']< result['data']['ma10'] and result['data']['ma10'] > result['data']['ma15']:
                # print('当前趋势price,ma5:%s,ma10:%s,ma15:%s'%(result['data']['price'],result['data']['ma5'],result['data']['ma10'],result['data']['ma15']))
                result['signal'] = -2
            if result['data']['price']<result['data']['ma5'] < result['data']['ma10'] < result['data']['ma15']:#当前趋势为下跌行情
                # print('当前趋势price,ma5:%s,ma10:%s,ma15:%s'%(result['data']['price'],result['data']['ma5'],result['data']['ma10'],result['data']['ma15']))
                result['signal'] = -3
            '''
        else:
            result['status'] = False

        return result

    def send_slower_order(self,symbol,type,price,amount,match_price=0,lever_rate=20,contract_type = 'this_week'):
        '''
        #发送平仓订单
        :param symbol:
        :param type:
        :param price:
        :param amount:
        :param match_price:
        :param lever_rate:
        :param contract_type:
        :return:
        '''

        price = ok_maker.get_price_depth(symbol)
        if price[1] > 1018.500:
            amount = random.randrange(4000, 6000) / 10000
            result = ok_maker.send_pc_order('eth_usdt', OK_ORDER_TYPE['PD'], price[1] - 0.001, amount)
            print(result)


        result = ok_maker._OKServices.send_future_order(symbol, type, price, amount,match_price,lever_rate,contract_type)

        return result

    def get_wt_orders(self,symbol):
        '''
        #获取用户委托订单类型
        :param symbol:
        :return:
        '''
        return_data={}
        wt_type = []
        wt_orders = self._OKServices.get_future_order(symbol=symbol, order_id=-1)
        if wt_orders:
            for order in wt_orders['orders']:
                wt_type.append(order['type'])

            return_data['orders']=wt_orders['orders']
        return_data['type_list']=wt_type

        return return_data  # 返回用户委托订单类型

    def send_pc_orders(self,symbol,signal):
        #print('用户持仓数据： %s' % position)
        #print('signal数据：%s'%signal_data)
        order_info = {}
        user_pos = self.get_user_position(symbol)
        if user_pos['status']:
            #print('交易信号:%s'%signal['signal'])
            wt_orders = self.get_wt_orders(symbol)
            if signal['signal'] == 1:
                if user_pos['sell_available']>0:
                    pk_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PK'],
                                                                  match_price=0, price=signal['data']['ma10']-0.5,
                                                                  amount=user_pos['sell_available'])
                    print(pk_order)
                    if pk_order:
                        order_info = pk_order
                        print('执行空头止损(市价)：%s' % pk_order)
            elif signal['signal'] == 2:#表示行情开始上涨,处理空头
                if user_pos['sell_amount']>0 and OK_ORDER_TYPE['PK'] not in wt_orders['type_list']:#表示持有空头持仓，并且没有平空的委托订单
                    if user_pos['sell_available']>0:#可平空数量不为0
                        pk_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PK'],
                                                                       match_price=0, price=signal['ma10'],
                                                                       amount=user_pos['sell_available'])
                        if pk_order:
                            order_info = pk_order
                            print('执行空头止损(挂单)：%s' % pk_order)
            elif signal['signal'] == 3:#表示行情开始上涨,处理空头  #
                if user_pos['sell_amount'] > 0:
                    if user_pos['sell_available']>0:#可平空数量不为0
                        pk_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PK'],
                                                                       match_price=1, price=signal['ma5'],
                                                                       amount=user_pos['sell_available'])
                        if pk_order:
                            order_info = pk_order
                            print('执行空头止损(挂单)：%s' % pk_order)

                if OK_ORDER_TYPE['PK'] in wt_orders['type_list']:#存在平空委托订单，将平空委托订单撤销
                    for order in wt_orders['orders']:
                        if order['type'] == OK_ORDER_TYPE['PK']:  # 表示平多未成交，摊销未成交订单，执行市价成交
                            cancel_order = self._OKServices.cancel_future_order(symbol, order['order_id'])
                            if cancel_order:  # 撤销订单成功
                                pk_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PD'],
                                                                              match_price=1, price=signal['ma5'],
                                                                              amount=user_pos['sell_available'])
                                if pk_order:
                                    order_info = pk_order
                                    print('执行空头止损(市平)：%s' % pk_order)
            #------------------------------------处理多头 头寸-----------------#
            elif signal['signal'] == -1:
                if user_pos['buy_available']>0:
                    pd_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PD'],
                                                                  match_price=0, price=signal['data']['ma10']+0.5,
                                                                  amount=user_pos['buy_available'])
                    print(pd_order)
                    if pd_order:
                        order_info = pd_order
                        print('执行多头止损(市价)：%s' % pd_order)
            elif signal['signal'] == -2:#表示行情开始下跌,处理多头
                if user_pos['buy_amount']>0 and OK_ORDER_TYPE['PK'] not in wt_orders['type_list']:#表示持有多头持仓，并且没有平多的委托订单
                    if user_pos['buy_available']>0:#可平多数量不为0
                        pd_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PD'],
                                                                        match_price=0, price=signal['ma10'],
                                                                        amount=user_pos['buy_available'])
                        print(pd_order)
                        if pd_order:
                            order_info = pd_order
                            print('执行多头止损(挂单)：%s' % pd_order)
            elif signal['signal'] == -3:#表示行情开始下跌,处理多头
                if user_pos['buy_amount']>0:#表示持有多头持仓
                    if user_pos['buy_available']>0:#可平多数量不为0
                        pd_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['PD'],
                                                                        match_price=1, price=signal['ma5'],
                                                                        amount=user_pos['buy_available'])
                        if pd_order:
                            order_info = pd_order
                            print('执行多头止损(挂单)：%s' % pd_order)
                    if OK_ORDER_TYPE['PD'] in wt_orders['type_list']:#表示存在多头平仓委托订单，撤销多头平仓委托订单
                        for order in wt_orders['orders']:
                            if order['type'] == OK_ORDER_TYPE['PD']:  # 表示平多未成交，摊销未成交订单，执行市价成交
                                cancel_order = self._OKServices.cancel_future_order(symbol, order['order_id'])
                                if cancel_order:  # 撤销订单成功
                                    pd_order = self._OKServices.send_future_order(symbol=symbol,
                                                                                  type=OK_ORDER_TYPE['PD'],
                                                                                  match_price=1,
                                                                                  price=signal['ma5'],
                                                                                  amount=user_pos['buy_available'])
                                    if pd_order:
                                        order_info = pd_order
                                        print('执行多头止损(市平)：%s' % pd_order)

        return order_info
    def send_kc_orders(self,symbol,signal):

        order_info={}
        user_pos = self.get_user_position(symbol)
        if user_pos['status']:
            print('交易信号:%s' % signal['signal'])
            wt_orders=self.get_wt_orders(symbol)
            if signal['signal'] == 1:#买入
                if user_pos['buy_amount'] == 0 and OK_ORDER_TYPE['KD'] not in wt_orders['type_list']:
                    buy_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['KD'],
                                                                   match_price=0, price=signal['data']['ma10']-0.5,
                                                                   amount=self._params['amount'])  # 挂单在10日均线上
                    if buy_order:
                        order_info = buy_order
                        print('多头已下单(市价):%s' % buy_order)
            elif signal['signal'] == 2:  # 表示做多信号
                if user_pos['buy_amount'] == 0 and OK_ORDER_TYPE['KD'] not in wt_orders['type_list']:  # 表示当前没有持仓,并且没有买入委托订单
                    buy_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['KD'],
                                                                   match_price=0, price=signal['ma10'],
                                                                   amount=self._params['amount'])  # 挂单在10日均线上
                    if buy_order:
                        order_info = buy_order
                        print('多头已下单(挂单):%s' % buy_order)
            elif signal['signal'] == 3:  # 表示上涨趋势已形成，不需要撤销未成交的委托订单，万一捡个漏呢
                if user_pos['buy_amount'] == 0:#表示当前没有买入持仓，执行市价买入
                    buy_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['KD'],
                                                                   match_price=1, price=signal['ma5'],
                                                                   amount=self._params['amount'])  # 挂单在5日均线上
                    if buy_order:
                        order_info = buy_order
                        print('多头已下单(市价):%s' % buy_order)
            # --------------------------------------处理做空订单-----------------------------------
            elif signal['signal'] == -1:
                if user_pos['sell_amount'] == 0 and OK_ORDER_TYPE['KK'] not in wt_orders['type_list']:
                    sell_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['KK'],
                                                                    match_price=0, price=signal['data']['ma10']+0.5,
                                                                    amount=self._params['amount'])  # 挂单在5日均线上
                    if sell_order:
                        order_info = sell_order
                        print('空头已下单(市价):%s' % sell_order)
            elif signal['signal'] == -2:  # 表示做空信号
                if user_pos['sell_amount'] == 0 and OK_ORDER_TYPE['KK'] not in wt_orders['type_list']:  # 表示没有空头持仓，执行做空操作
                    sell_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['KK'],
                                                                    match_price=0,price=signal['ma10'],
                                                                    amount=self._params['amount'])  # 挂单在10日均线上
                    if sell_order:
                        order_info = sell_order
                        print('空头已下单(挂单):%s' % sell_order)
            elif signal['signal'] == -3:  # 表示下跌趋势已形成，执行市价买入
                if user_pos['sell_amount'] == 0:
                    sell_order = self._OKServices.send_future_order(symbol=symbol, type=OK_ORDER_TYPE['KK'],
                                                                    match_price=1, price=signal['ma5'],
                                                                    amount=self._params['amount'])  # 挂单在5日均线上
                    if sell_order:
                        order_info = sell_order
                        print('空头已下单(市价):%s' % sell_order)

        return order_info
    def trade_system(self,symbol,period='1min',size = 60,contract_type='this_week'):

        return_data = {}
        signal = self.get_trade_signal(symbol, period, size, contract_type)  # 获取行情交易信号
        if signal['status']:#获取到交易信号
            pc_order = self.send_pc_orders(symbol, signal)  #处理平仓

            if pc_order:
                print("平仓订单:%s"%pc_order)

            kc_order = self.send_kc_orders(symbol, signal)  #处理开仓#
            if kc_order:
                print("平仓订单:%s"%kc_order)

        return return_data

if __name__ == '__main__':
    params ={'dif':1.5}
    params ={'m5m10':0.2}
    params ={'risk_rate':0.5}
    params ={'amount':2}

    ok_maker = OK_MAKER(params)
    symbol = 'eth_usdt'
    while True:
        ok_maker.trade_system(symbol,'5min')




