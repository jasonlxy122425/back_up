import pickle
from Default.KronosConfig import *
from Default.DefaultCommonConfig import *

@config_interface
class TagConfig():
    def __init__(self):
        self.configs = []
        self.tag = 'KRONOS_LT_GAIA_2'
        self.acct_group = 'kronos_lt_gaia_2'
        

    def genFactors(self, factor_path):
        with open(factor_path , 'rb') as file:
            factors = pickle.load(file)
        return factors

    def generateParams(self, stra_params):
        config = KronosConfig("lt_gaia")
        #self.tag = stra_params['tag']
        #self.acct_group = stra_params['acct_group']
        config.num_of_book_levels = 300
        config.max_qry_order_count = 2
        # predictor log
        config.predictorConfig.demeter_sample_num = stra_params["demeter_sample_size"]
        config.predictorConfig.factor_path = stra_params["factor_path"]
        config.predictorConfig.model_path = ""
        config.predictorConfig.demeter_sample_type = stra_params["demeter_sample_type"]
        config.predictor = 'Kronos'
        config.predictorConfig.model_type = 'lgb'
        if stra_params["to_generate_factors"]:
            config.predictorConfig.factors = self.genFactors(config.predictorConfig.factor_path)
            config.predictorConfig.model_path = stra_params['model_path']
        else:
            config.predictorConfig.factors = []
        if len(config.predictorConfig.factors) >0 and config.predictorConfig.factors[0].__contains__('model_type'):
            config.predictorConfig.model_type = config.predictorConfig.factors[0]['model_type']
            config.predictorConfig.factors = config.predictorConfig.factors[1:].copy()


        # orderlogic log
        for key, value in stra_params.items():
            setattr(config.orderLogicConfig, key, value)

        config.orderLogicCommonConfig.set_values(max_pos_in_clips = stra_params["max_pos_in_clips"],
                                                    notional_size = stra_params["notional_size"],
                                                    stop_loss = stra_params["stop_loss"],
                                                    cancel_interval_ms = 1000)

        config.commonConfig.set_values(use_orderbook=True,
                                                use_bestquote=False,
                                                use_trade=True,
                                                use_liquidation=False,
                                                use_fundingrate=False,
                                                use_batch_mode = stra_params['batch_mode'],
                                                data_preprocessor_config=[{'name':'TradeFilterPreprocessor'}]
                                                )
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
            "factor_path":  "/mnt/share/jsc/config/pred/[Lighter_LinearSwap_BTCUSD][lt_bn_btc]/factors.txt",
            "model_path": "/mnt/share/jsc/config/pred/[Lighter_LinearSwap_BTCUSD][lt_bn_btc]/model.txt",
            "mkt_timeout_ns": 3000000000,
            "notional_size": 1000,
            "max_pos_in_clips": 1,
            "quote_qty": 0.001,
            "theo_alpha": 0.0,
            "theo_gamma": 1.0,
            'theo_gamma2': 1.0,
            'theo_alpha2':0,
            "init_var":0.0,
            "var_ewma":0.95,
            "theo_buffer_len": 30,
            "sigma_alpha": 0.0,
            "sigma_beta": 1.0,
            "sigma_base": 0.0,
            "pos_pen_intercept": 1.0,
            "pos_pen_coef": 1000,
            "pos_pen_lowerbound": 0.0,
            "quote_range":100,
            "queue_front_cancel":100000,
            "min_edge_cancel":0.0,
            "min_edge_bps":0.2,
            "min_edge":0.0,
            "signal_floor":0.0,
            "improve_tick_num":0,
            "improve_spread_ratio": 0.1,
            "is_tif_po": 1,
            'use_sigma_adj':0,
            'sigma_alpha_take':0,
            'sigma_beta_take':0,
            'sigma_base_take':0,
            'sigma_alpha_join':0,
            'sigma_beta_join':0,
            'sigma_base_join':0,
            'sigma_alpha_improve':0,
            'sigma_beta_improve':0,
            'sigma_base_improve':0,
            'pred_beta':1.0,
            'pred_alpha':0,
            'pred_base':0,
            'frac_cut':1.0,
            'frac_cut_for_improve':1.0,
            'frac_cut_for_join':1.0,
            'frac_cut_for_take':1.0,
            'use_sep_improve_frac_cut':0,
            'use_sep_take_frac_cut':1.0,
            'use_sep_join_frac_cut':1.0,
            'minimum_edge_bps':1.2,
            'minimum_edge':0,
            'pos_pen_lower_bound_cancel':0,
            'pos_pen_upper_bound_cancel':0,
            'use_queue_cancel':0,
            'cancel_threshold_in_volume':0,
            'frac_den_const':0,
            'queue_edge_alpha':0,
            'queue_edge_beta':0,
            'queue_edge_base':0,
            'pos_pen_lower_bound':0,
            'pos_pen_upper_bound':0,
            'pos_pen_one_side_target':0,
            'use_spread_filter':0,
            'spread_filter_cut':0,
            'min_volume_for_taking':0,
            'min_standized_signal_for_taking':0,
            'improve_queue_beta':0,
            'frac_den_const_for_improve':0,

            'join_queue_beta':0,
            'frac_den_const_for_join':0,

            'take_queue_beta':0,
            'frac_den_const_for_take':0,
            'take_queue_beta':0,
            'take_queue_base':0,
            'improve_tick':1,
            "spread_offset_bps":0.5,
            "cancel_range_bps":0.25,
            "cancel_range_ticks":1000,
            "edge_lower_bound":-1,
            "inventory_bias_beta":0.5,
            "improve_spread_ratio": 0.1,
            "cancel_queue_front": 1000,
            'to_output_logs':0,
        }

        for symbol in ["BTC"]:
            for idx in [1]:
                stra_params["idx"] = str(idx)
                stra_params["acct_id"] = f"{symbol.lower()}_{idx}"
                stra_params["target_instrument"] = f"Lighter_LinearSwap_{symbol}USD"
                stra_params["notional_size"] = 120
                stra_params["batch_mode"] = False
                stra_params["stop_loss"] = -1000
                if idx == 1:
                    stra_params["signal_floor"] = 0.0
                    stra_params["minimum_edge_bps"] = 1.2
                    stra_params["improve_spread_ratio"] = 0.1
                    stra_params["queue_front_cancel"] = 1
                elif idx == 2:
                    stra_params["signal_floor"] = 1.5
                    stra_params["minimum_edge_bps"] = 0.0
                    stra_params["improve_spread_ratio"] = 1.0

                self.generateParams(stra_params)
                    
        return self.configs
