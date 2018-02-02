import model.model_add_aligned as model_add_aligned
from  ultize.parameter import args
from ultize.reader import *
from ultize.functions import *
#logging.basicConfig(level=logging.NOTSET)

# Read cha_vectors.bin
if args.use_pretrain_vector is False:
    vocab = loadvocab(args.vocab_path)
    vocab_size = len(vocab)
    embedding_dim = args.input_embedding_size 
    print("load vocab")
else:
    if args.pretrain_vector_split is False:
        vocab,embd = loadWord2Vec(args.vector_path)
        vocab_size = len(vocab)
        embedding_dim = len(embd[0])
        print("load vector")
    else:
        vocab,trainable_embd = loadWord2Vec(args.vector_path+'-trainable')
        vocab2, fixed_embd = loadWord2Vec(args.vector_path + '-fixed')
        # adding vocab size parameter
        args.fixed_vocab_size =len(vocab2)
        args.trainable_vocab_size = len(vocab)
        vocab.extend(vocab2) # because vocab is the big vocab
        embedding_dim = len(fixed_embd[0])
        vocab_size = len(vocab)
        print("load spliting vector")


# specific vocab size
vocab = dict(zip(vocab,range(len(vocab)))) # vocab
id_vocab = {v:k for k, v in vocab.items() }

# Define reader
reader  = Reader(args,vocab)
args.src_vocab_size = vocab_size
args.pre_trained_embedding_length = len(vocab) # fix the trained embedding size
args.input_embedding_size = embedding_dim
args.pos_vocab_size =  len(reader.pos_vocab)  # size of vocab


trainModel = model_add_aligned.model(args)
trainModel.build_model()


sess = tf.Session()#config=para_config)
saver = tf.train.Saver()
ckpt_state = tf.train.get_checkpoint_state(args.restore_path)


graph=  tf.get_default_graph()
writer = tf.summary.FileWriter(args.restore_path,graph=graph)


if ckpt_state == None:
    print("Cant't load model,starting initial")
    sess.run(tf.global_variables_initializer())
    # load embedding
    if args.use_pretrain_vector:
        if args.pretrain_vector_split is False:
            sess.run(trainModel.embedding_init, feed_dict={trainModel.embedding_placeholder: embd})
        else:
            sess.run(trainModel.embedding_init, feed_dict={trainModel.trainable_embed_placeholder: trainable_embd,trainModel.fixed_embed_placeholder: fixed_embd})
else:
    try:
        saver.restore(sess, ckpt_state.model_checkpoint_path)
        print("restor model successed")
    except:
        print("loading error.")
        exit(0)
# start to inference
print("model path:".format(args.restore_path))
reader.reset()
for m_epoch in range(args.epoch):

    per_loss_start = 0
    
    per_loss_end = 0
    
    for step in  range(reader.num_examples // args.batch_size):

        query_ls , passage_ls, answer_ls, answer_p_s, answer_p_e,passage_pos_ls = reader.get_batch()
        
        feed = set_dict(trainModel,query_ls , passage_ls, answer_p_s, answer_p_e,passage_pos_ls,add_token_feature = args.add_token_feature)
        
        toSee = [trainModel.cross_entropy_start,trainModel.cross_entropy_end,trainModel.start_loss_matrix,trainModel.summary_op,trainModel.train_op]
        
        loss_start,loss_end, loss_nartix,summary_re, _ = sess.run(toSee,feed_dict=feed)
        
        per_loss_start  += loss_start
        
        per_loss_end    += loss_end
        
        # save summary
        if step*args.batch_size % 100 ==0 and step!=0:
            print("iterator: {} ，loss_start is :{} , loss_end is:{}".format(reader.question_index, per_loss_start /100,per_loss_end/100 ))
            writer.add_summary(summary_re,global_step = trainModel.global_step.eval(session = sess))
            per_loss_start = 0
            per_loss_end = 0
            # inference
            pre_s ,pre_e =sess.run([trainModel.p_W_q,trainModel.p_We_q],feed_dict=feed)
            s_p = np.argmax(pre_s[0])
            e_p = np.argmax(pre_e[0])
            if  s_p <= e_p:
                #print("answer_ls[0]:{},len id_vocab:{},len vocab:{}".format(answer_ls[0] , len(id_vocab) ,len(vocab)))
                print("question:{},passage:{},answer:{},answer_p:{},answer_e:{},pre:{},start:{},end:{},sequence_len:{}".format(
                    id2word(query_ls[0],id_vocab),
                    id2word(passage_ls[0],id_vocab),
                    answer_ls[0],
                    answer_p_s[0],
                    answer_p_e[0],
                    id2word(passage_ls[0][s_p:e_p],id_vocab), # because in slicing list is [)
                    s_p,
                    e_p,
                    len(passage_ls[0])))
                #print("start_martix:{},end_martix:{}".format(pre_s[0],pre_e[0]))
        if step*args.batch_size %1000 == 0:
            saver.save(sess,args.restore_path,global_step = trainModel.global_step.eval(session = sess))
    reader.reset()

print("finished")
