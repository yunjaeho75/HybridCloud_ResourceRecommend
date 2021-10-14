import argparse
import os
import sys as _sys
from cmp.ml import learner
from cmp.ml import estimator
from cmp.pso import estimator as cost_estimator
from cmp.api import ml as mlestimator
from cmp.api import pso as posestimator

# create command parser
parser = argparse.ArgumentParser(prog="CMP", description='cmp conntrols the cmp-ai echo system.')

# add sub-command parser
subparsers = parser.add_subparsers(help='Usual sub-command help')

# add ml learner parser
learner_parser = subparsers.add_parser('learner', help='Run the generate a predictive model.')
learner_parser.add_argument('-n', '--name', type=str, help='Specifies the name of the model to be created.')
learner_parser.add_argument('-i', '--input', type=str, help='Specify the dataset to be used for the model to be created.')
learner_parser.add_argument('-o', '--output', type=str, help='Specify the location of the model to be created.')
learner_parser.add_argument('-bm', '--base-model', type=str, help='Specifies the default model to be used in the model to be generated.')
learner_parser.add_argument('-dh', '--data-helper', type=str, help='Specifies the data helper.')
learner_parser.add_argument('-l', '--log', type=str, default='learner-ml.log', help='Specify the location where the log will be saved.')
learner_parser.add_argument('-v', '--verbose', type=int, default='1', help='Specifies the level of log generation.')
learner_parser.set_defaults(func=learner.main)

# add ml estimator parser
estimator_parser = subparsers.add_parser('estimator', help='Run the predictive model and return predicted values.')
estimator_parser.add_argument('-m', '--model', type=str, help='Specify the predictive model to use.')
estimator_parser.add_argument('-i', '--input', type=str, help='Specify the dataset to be used for prediction.')
estimator_parser.add_argument('-o', '--output', type=str, default='predict.json', help='Output the prediction results to a file.')
estimator_parser.add_argument('-dh', '--data-helper', type=str, help='Specifies the data helper.')
estimator_parser.add_argument('-l', '--log', type=str, default='estimator-ml.log', help='Specify the location where the log will be saved.')
estimator_parser.add_argument('-v', '--verbose', type=int, default='1', help='Specifies the level of log generation.')
estimator_parser.set_defaults(func=estimator.main)

# add ml estimator api parser
estimator_parser = subparsers.add_parser('ml-api', help='Run the predictive model and return predicted values.')
estimator_parser.add_argument('-m', '--model', type=str, help='Specify the predictive model to use.')
estimator_parser.add_argument('-dh', '--data-helper', type=str, default='spamfilter', help='Specifies the data helper.')
estimator_parser.add_argument('-l', '--log', type=str, default='estimator-ml-api.log', help='Specify the location where the log will be saved.')
estimator_parser.add_argument('-v', '--verbose', type=int, default='1', help='Specifies the level of log generation.')
estimator_parser.set_defaults(func=mlestimator.main)

# add pso clound item recommender parser
estimator_parser = subparsers.add_parser('cost-consol', help='Run the resource usage cost optimization in cloud computing.')
estimator_parser.add_argument('-m', '--model', type=str, help='Specify the predictive model to use.')
estimator_parser.add_argument('-i', '--input', type=str, help='Specify the dataset to be used for prediction.')
estimator_parser.add_argument('-o', '--output', type=str, default='predict.json', help='Output the prediction results to a file.')
estimator_parser.add_argument('-op', '--optimizer', type=str, default='pso', help='Specify the agorithm of optimizer.')
estimator_parser.add_argument('-dh', '--data-helper', type=str, default='azure-vm', help='Specifies the data helper.')
estimator_parser.add_argument('-l', '--log', type=str, default='estimator-pso-cost.log', help='Specify the location where the log will be saved.')
estimator_parser.add_argument('-v', '--verbose', type=int, default='1', help='Specifies the level of log generation.')
estimator_parser.set_defaults(func=cost_estimator.main)

# add ml estimator api parser
estimator_parser = subparsers.add_parser('cost-api', help='Run the predictive model and return predicted values.')
estimator_parser.add_argument('-m', '--model', type=str, help='Specify the predictive model to use.')
estimator_parser.add_argument('-op', '--optimizer', type=str, default='pso', help='Specify the agorithm of optimizer.')
estimator_parser.add_argument('-dh', '--data-helper', type=str, default='azure-vm', help='Specifies the data helper.')
estimator_parser.add_argument('-l', '--log', type=str, default='estimator-pso-api.log', help='Specify the location where the log will be saved.')
estimator_parser.add_argument('-v', '--verbose', type=int, default='1', help='Specifies the level of log generation.')
estimator_parser.set_defaults(func=posestimator.main)


def main(*args):
    args = parser.parse_args(*args)
    args.func(args)

if __name__ == "__main__":
    main(_sys.argv[1:])