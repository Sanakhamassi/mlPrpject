import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
AdaBoostRegressor,
GradientBoostingRegressor,
RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging 
from src.utils import evaluate_models, save_object
@dataclass
class ModelTrainerConfig: 
    trained_model_file_path=os.path.join("artifacts","model.pkl")
class ModelTrainer: 
    def __init__(self): 
        self.model_trainer_config=ModelTrainerConfig() 
    def initiate_model_trainer(self,train_arr,test_arr):
        try: 
            logging.info("splitting and test inut data")
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1], 
                test_arr[:,:-1],
                test_arr[:,-1]

            ) 
            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Classifier": KNeighborsRegressor(),
                "XGBClassifier": XGBRegressor(),
                "CatBoosting Classifier": CatBoostRegressor(verbose=False),
                "AdaBoost Classifier": AdaBoostRegressor(),
            } 
            model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys()) [
            list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f'Best found model on both training ad testing dataset')
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model) 
            predict=best_model.predict(x_test)
            r2=r2_score(y_test,predict)
            return r2

        except Exception as e:
            raise CustomException(e,sys)

