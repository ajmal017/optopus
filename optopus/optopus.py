#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 16:30:25 2018

@author: ilia
"""
from optopus.account import Account, AccountItem
from optopus.data_manager import DataManager, DataSource
from optopus.data_objects import Asset, BarDataType
from optopus.portfolio_manager import PortfolioManager


class Optopus():
    """Class implementing automated trading system"""

    def __init__(self, broker) -> None:
        self._broker = broker
        self._account = Account()
       
        
        
        self._data_manager = DataManager()
        self._data_manager.add_data_adapter(self._broker._data_adapter,
                                            DataSource.IB)
        self._portfolio_manager = PortfolioManager(self._data_manager)
        
         # Events
        self._broker.emit_account_item_event = self._change_account_item
        self._broker.emit_position_event = self._data_manager._change_position
        self._broker.emit_execution_details = self._data_manager._execution
        

        

    def start(self) -> None:
        self._broker.connect()
        
    def stop(self) -> None:
        self._broker.disconnect()

    def pause(self, time: float) -> None:
        self._broker.sleep(time)

    def _start_strategies(self) -> None:
        self.dummy = DummyStrategy(self._data_manager)

    def _change_account_item(self, item: AccountItem) -> None:
        try:
            self._account.update_item_value(item)
        except Exception as e:
            print('Error updating account item', e)

    def beat(self) -> None:
        print('.')
        self._data_manager.update_assets()
        self.dummy.calculate_signals()
        
    def positions(self) -> object:
        return self._portfolio_manager.positions()

    def current(self, assets: Asset, fields: list) -> object:
        return self._data_manager.current(assets, fields)

    def update_assets(self) -> None:
        self._data_manager.update_assets()

    def historical(self, assets: list, fields: list) -> object:
        return self._data_manager.historical(assets, fields, BarDataType.Trades)
    
    def historical_IV(self, assets: list, fields: list) -> object:
        return self._data_manager.historical(assets, fields, BarDataType.IV)
    
    def IV_rank(self, asset: Asset, IV_value: float) -> float:
        return self._data_manager.IV_rank(asset, IV_value)
    
    def IV_percentile(self, asset: Asset, IV_value: float) -> float:
        return self._data_manager.IV_percentile(asset, IV_value)
        
