"""
THis file is for train.py and inference.py
"""
import codecs
import argparse

parser = argparse.ArgumentParser(description='parameters.')

parser.add_argument('--batch_size',type= int ,default = 20,
                    help='the origin data path')
parser.add_argument('--num_units', type= int, default = 200,
                    help='the path of processed data ')
parser.add_argument('--is_training', type=lambda s: s.lower() in ['true', 't', 'yes', '1'] ,default= False,
                    help='Ture means inference')
parser.add_argument('--restore_path', type= str, default = "../modelRestor/word-level/",
                    help='the path of retore path ')

parser.add_argument('--input_embedding_size', type= int, default = 200,
                    help='the size of embedding size ')
parser.add_argument('--data_path', type= str, default = "../input/data",
                    help='the path of data')
# check to use vocab or pre-train vector
parser.add_argument('--use_pretrain_vector',type=lambda s: s.lower() in ['true', 't', 'yes', '1'] ,default= False,
                    help='a switch to use pre-trained vector ')
parser.add_argument('--pretrain_vector_split',type=lambda s: s.lower() in ['true', 't', 'yes', '1'] ,default= False,
                    help='whether to split vector into fixed and trainable')

parser.add_argument('--vocab_path', type= str, default = None,
                    help='the size of vocab size ')
parser.add_argument('--vector_path', type= str, default = "../cha_vectors.bin",
                    help='the path of vector and vocab')

parser.add_argument('--result_path', type= str, default = "../output/result",
                    help='the path of result')
# used in inference
parser.add_argument('--test_inference', type=lambda s: s.lower() in ['true', 't', 'yes', '1'] ,default= False,
                    help='whether to check inference run ok')
parser.add_argument('--infer_vocab_path', type= str, default = None,
                    help='the path of infer_vocab')

parser.add_argument('--num_layer', type= int, default =3,
                    help='layers in biRNN')
parser.add_argument('--epoch', type= int, default =10,
                    help='the training epochs')
# pos 
parser.add_argument('--pos_vocab_path', type= str, default ="../others/pos_vocab",
                    help='the pos vocab')
parser.add_argument('--pos_vocab_size', type= int, default = 30,
                    help='the pos vocab size')
# this need to be set in inference.py
parser.add_argument('--add_token_feature', type=lambda s: s.lower() in ['true', 't', 'yes', '1'] ,default= False,
                    help='add_token_feature to be Ture of False')
# model version 
parser.add_argument('--version', action='version', version='%(prog)s 1.17')

# drop_out_pro
parser.add_argument('--keep_pro', type= float, default = 0.7,
                    help='drop out probality')
# Used in self-define data 
parser.add_argument('--show_self_define',type=lambda s: s.lower() in ['true', 't', 'yes', '1'] ,default= False,
                    help='a switch to show inference information')
args = parser.parse_args()

# TODO : this two flag are also set in make_vocab.py
# I need to modify this
args.EN_TAG  = 'EN'
args.NUM_TAG = 'NUM'
print("load paramaters")
