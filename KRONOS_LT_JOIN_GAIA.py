import pickle
from Default.KronosConfig import *
from Default.DefaultCommonConfig import *

@config_interface
class TagConfig():
    def __init__(self):
        self.configs = []
        self.acct_group = 'kronos_lt_join_gaia'
        self.tag = 'KRONOS_LT_JOIN_GAIA'
        

    def genFactors(self, factor_path):
        with open(factor_path , 'rb') as file:
            factors = pickle.load(file)
        return factors

    def generateParams(self, stra_params):
        config = KronosConfig("ok_join")
        config.num_of_book_levels = 500
        # predictor log
        config.predictorConfig.demeter_sample_num = stra_params["demeter_sample_size"]
        config.predictorConfig.factor_path = f"{stra_params["pred_dir"]}/factors.txt"
        config.predictorConfig.model_path = ""
        config.predictorConfig.demeter_sample_type = stra_params["demeter_sample_type"]
        config.predictor = 'Kronos'
        config.predictorConfig.model_type = 'lgb'
        if stra_params["to_generate_factors"]:
            config.predictorConfig.factors = self.genFactors(config.predictorConfig.factor_path)
            config.predictorConfig.model_path = f"{stra_params["pred_dir"]}/model.txt"
        else:
            config.predictorConfig.factors = []
        if len(config.predictorConfig.factors) >0 and config.predictorConfig.factors[0].__contains__('model_type'):
            config.predictorConfig.model_type = config.predictorConfig.factors[0]['model_type']
            config.predictorConfig.factors = config.predictorConfig.factors[1:].copy()

        config.commonConfig.use_warmup = True
        config.commonConfig.set_values(data_preprocessor_config=[{'name':'TradeFilterPreprocessor'}])

        # orderlogic log
        for key, value in stra_params.items():
            setattr(config.orderLogicConfig, key, value)
        config.orderLogicCommonConfig.max_pos_in_clips = stra_params["max_pos_in_clips"]
        config.orderLogicCommonConfig.notional_size = stra_params["notional_size"]
        config.orderLogicCommonConfig.stop_loss = stra_params["stop_loss"]
        config.orderLogicCommonConfig.use_reduce_only_mode = stra_params["use_reduce_only_mode"]
        config.commonConfig.set_values(use_orderbook=True,
                                                use_bestquote=True,
                                                use_trade=True,
                                                use_liquidation=False,
                                                use_fundingrate=False,
                                                use_batch_mode = stra_params['batch_mode'])
        # real trade
        config.acct_group = self.acct_group
        config.tag = self.tag
        config.sub_tag = f"{self.tag}_{stra_params["idx"]}"
        config.acct_id = stra_params["acct_id"]

        # 
        config.setSymbol(stra_params["target_instrument"])
        self.configs.append(config)
    
    def getConfig(self):
        stra_params = {
            "to_generate_factors": True,
            "to_output_factors": False,
            "to_output_gob": False,
            "demeter_sample_type": "tick",
            "demeter_sample_size": 0,
            "output_sample_size": 0,
            "pred_dir": "/mnt/share/lxy/config/prod/ok_btc/linear_7",#
            "stop_loss": -100,
            "use_reduce_only_mode": False,
            "mkt_timeout_ns": 3000000000,
            "quoty_size": 0.01,
            "notional_size": 200,
            "max_pos_in_clips": 1,
            "custom_min_notional": 10,
            "use_debug_msg":0,
            "theo_alpha": 0,
            "theo_gamma": 1,
            "std_ewma_interval": 0.5,
            "std_ewma_exp_base": 60,
            "sigma_threshold": 0,
            "sigma_dis_cap": 1000,
            "sigma_alpha": 0.0,
            "sigma_beta": 1.0,
            "use_pred": True,
            "pred_beta": 0,
            "entry_bps": 2,
            "exit_bps": 2,
            "cancel_entry_bps": 0.2,
            "cancel_exit_bps": 0.2,
            "pos_entry_dis_bps": 0,
            "pos_exit_dis_bps": 0,
            "theo_level": 50,
            "pred_edge_entry_threshold": -100,
            "pred_edge_exit_threshold": -100,
            "pred_edge_entry_cancel_threshold": -100,
            "pred_edge_exit_cancel_threshold": -100,
            "sigma_entry_threshold": -100,
            "mid_buffer_len1": 30,#20
            "mid_buffer_len2": 60,
            "mid_buffer_len3": 120,
        }

        for symbol in ["BTC"]:
            for idx in [1]:
                stra_params["idx"] = str(idx)
                stra_params["acct_id"] = f"{symbol.lower()}_{idx}"
                stra_params["target_instrument"] = f"Lighter_LinearSwap_{symbol}USD"
                stra_params["notional_size"] = 200
                stra_params["batch_mode"] = True
                stra_params["stop_loss"] = -500

                if symbol == "BTC":
                    stra_params["to_generate_factors"] = True
                    stra_params["use_pred"] = True
                    stra_params["pred_dir"] = "/mnt/share/lxy/config/prod/ok_btc/trade_model_120_notrade"
                    stra_params["notional_size"] = 500
                    stra_params["std_ewma_exp_base"] = 60
                    stra_params["sigma_threshold"] = 10
                    stra_params["sigma_alpha"] = 0.02
                    stra_params["sigma_beta"] = 1
                    stra_params["entry_bps"] = 2
                    stra_params["exit_bps"] = 2
                    stra_params["cancel_entry_bps"] = 0.2
                    stra_params["cancel_exit_bps"] = 0.2
                    stra_params["pred_edge_entry_threshold"] = -100
                    stra_params["pred_edge_entry_cancel_threshold"] = -100
                    stra_params["pred_edge_exit_threshold"] = -100
                    stra_params["pred_edge_exit_cancel_threshold"] = -100
                    if idx == 1:
                        stra_params["entry_bps"] = 2
                        stra_params["exit_bps"] = 2
                        stra_params["pred_edge_entry_threshold"] = 0.4
                        stra_params["pred_edge_entry_cancel_threshold"] = 0.4

                self.generateParams(stra_params)
                    
        return self.configs
