import tensorflow as tf
import numpy as np
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from nltk.tag import StanfordPOSTagger
from basic.clustering import do_cluster

def norm_vis(T, which_words, data_type, summaries):
    """
    To visualize norm of fillers and roles vectors.
    This function is aimed to be used under "evaluator.py"
    """
    for word in which_words:
        # question side
        name = "{}/norm/fw_u_aF/[0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["fw_u_aF"][0][word])))]) )
        name = "{}/norm/fw_u_aR/[0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["fw_u_aR"][0][word])))]) )
        name = "{}/norm/bw_u_aF/[0][" + str(word) + "]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["bw_u_aF"][0][word])))]) )
        name = "{}/norm/bw_u_aR/[0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["bw_u_aR"][0][word])))]) )
        # context side
        name = "{}/norm/fw_h_aF/[0][0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["fw_h_aF"][0][0][word])))]) )
        name = "{}/norm/fw_h_aR/[0][0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["fw_h_aR"][0][0][word])))]) )
        name = "{}/norm/bw_h_aF/[0][0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["bw_h_aF"][0][0][word])))]) )
        name = "{}/norm/bw_h_aR/[0][0]["+str(word)+"]"
        summaries.append( tf.Summary(
            value=[tf.Summary.Value(tag=name.format(data_type),
                                    simple_value=float(np.linalg.norm(T["bw_h_aR"][0][0][word])))]) )
    return summaries

def norm_vis2(T, which_words):
    """
    To visualize norm of fillers and roles vectors.
    This function is aimed to be used under "model.py" and called in "main.py" through "trainer.py".
    """
    for word in which_words:
        # question side
        name = "{}/norm/fw_u_aF/[0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["fw_u_aF"][0][word]))
        name = "{}/norm/fw_u_aR/[0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["fw_u_aR"][0][word]))
        name = "{}/norm/bw_u_aF/[0][" + str(word) + "]"
        tf.summary.scalar(name, euclidean_norm(T["bw_u_aF"][0][word]))
        name = "{}/norm/bw_u_aR/[0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["bw_u_aR"][0][word]))
        # context side
        name = "{}/norm/fw_h_aF/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["fw_h_aF"][0][0][word]))
        name = "{}/norm/fw_h_aR/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["fw_h_aR"][0][0][word]))
        name = "{}/norm/bw_h_aF/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["bw_h_aF"][0][0][word]))
        name = "{}/norm/bw_h_aR/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, euclidean_norm(T["bw_h_aR"][0][0][word]))

def sparsity_vis(T, which_words):
    """
    To visualize sparsity of fillers and roles vectors.
    """
    for word in which_words:
        # question side
        name = "{}/sparsity/fw_u_aF/[0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["fw_u_aF"][0][word]))
        name = "{}/sparsity/fw_u_aR/[0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["fw_u_aR"][0][word]))
        name = "{}/sparsity/bw_u_aF/[0][" + str(word) + "]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["bw_u_aF"][0][word]))
        name = "{}/sparsity/bw_u_aR/[0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["bw_u_aR"][0][word]))
        # context side
        name = "{}/sparsity/fw_h_aF/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["fw_h_aF"][0][0][word]))
        name = "{}/sparsity/fw_h_aR/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["fw_h_aR"][0][0][word]))
        name = "{}/sparsity/bw_h_aF/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["bw_h_aF"][0][0][word]))
        name = "{}/sparsity/bw_h_aR/[0][0]["+str(word)+"]"
        tf.summary.scalar(name, tf.nn.zero_fraction(T["bw_h_aR"][0][0][word]))

def tensorHist(T, which_words):
    """
    To visualize distribution of units activations of fillers and roles vectors.
    """
    for word in which_words:
        # question side
        name = "fw_u_aF/[0][" + str(word) + "]"
        tf.summary.histogram(name, T["fw_u_aF"][0][word])
        name = "fw_u_aR/[0][" + str(word) + "]"
        tf.summary.histogram(name, T["fw_u_aR"][0][word])
        name = "bw_u_aF/[0][" + str(word) + "]"
        tf.summary.histogram(name, T["bw_u_aF"][0][word])
        name = "bw_u_aR/[0][" + str(word) + "]"
        tf.summary.histogram(name, T["bw_u_aR"][0][word])
        # context side
        name = "fw_h_aF/[0][0][" + str(word) + "]"
        tf.summary.histogram(name, T["fw_h_aF"][0][0][word])
        name = "fw_h_aR/[0][0][" + str(word) + "]"
        tf.summary.histogram(name, T["fw_h_aR"][0][0][word])
        name = "bw_h_aF/[0][0][" + str(word) + "]"
        tf.summary.histogram(name, T["bw_h_aF"][0][0][word])
        name = "bw_h_aR/[0][0][" + str(word) + "]"
        tf.summary.histogram(name, T["bw_h_aR"][0][0][word])

def euclidean_norm(a):
    a = tf.square(a)
    a = tf.reduce_sum(a)
    return tf.sqrt(a)


def forceAspect(ax, aspect=1):
    im = ax.get_images()
    extent = im[0].get_extent()
    ax.set_aspect(abs((extent[1] - extent[0]) / (extent[3] - extent[2])) / aspect)

def sentence2role_filler_vis(data_set, idxs, tensor_dict, config, tensor2vis, spans):
    if tensor2vis in ["fw_u_aR", "bw_u_aR", "fw_u_aF", "bw_u_aF"]: # Question side
        question = data_set.data["q"][config.which_q]
        q_len = len(question)
        T = tensor_dict[tensor2vis][config.which_q][:q_len]
        # Visualize each question
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel(tensor2vis)
        ax.set_ylabel("QUESTION")
    else: # Context side
        if config.Just_Answer_vis:
            ans_start = spans[config.which_q][0][1]
            ans_end = spans[config.which_q][1][1]
            q_len = ans_end - ans_start
            question = data_set.data["x"][config.which_q][0][ans_start:ans_end]
            T = tensor_dict[tensor2vis][config.which_q][0][ans_start:ans_end]
            # Visualize each answer
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel(tensor2vis + "\n Question: " + str(data_set.data["q"][config.which_q]), fontsize=8)
            ax.set_ylabel("PREDICTED ANSWER BY TRAINED MODEL")
        else:
            question = data_set.data["x"][config.which_q][0]
            q_len = len(question)
            if q_len > 15:
                q_len = 15
            T = tensor_dict[tensor2vis][config.which_q][0][:q_len]
            # Visualize each question
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel(tensor2vis + "\n Question: " + str(data_set.data["q"][config.which_q]), fontsize=8)
            ax.set_ylabel("FIRST 15 WORDS OF THE PASSAGE.")


    cax = ax.matshow(T, interpolation='none', cmap=plt.cm.ocean_r)
    fig.colorbar(cax)
    ax.set_yticklabels([""] + question, fontsize=8)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
    # Minor ticks
    if tensor2vis in ["fw_u_aR", "bw_u_aR", "fw_h_aR", "bw_h_aR"]:
        width = config.nRoles
    else:
        width = config.nSymbols
    ax.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-.5, q_len, 1), minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=2)
    plt.show()
    forceAspect(ax, aspect=1)
    plt.savefig(config.TPRvis_dir + "/dataID_" + str(idxs[config.which_q]) + "_" + tensor2vis + ".png")

def write2csv(data_set, idxs, tensor_dict, config, tensor2vis):
    fl = open(config.TPRvis_dir + "/" + tensor2vis + "_nRoles_" + str(config.nRoles) + "_test_set.csv", "a")
    nQuestions = len(data_set.data["q"])
    for which_q in range(nQuestions):
        if tensor2vis in ["fw_u_aR", "bw_u_aR", "fw_u_aF", "bw_u_aF"]: # Question side
            question = data_set.data["q"][which_q]
            q_len = len(question)
            T = tensor_dict[tensor2vis][which_q][:q_len]
        out = [[]]*q_len
        for i in range(q_len):
            out[i] = [idxs[which_q]] + [question[i]] + T[i].tolist()
        writer = csv.writer(fl)
        for row in out:
            writer.writerow(row)
    fl.close()

def write2csv_withPOS(data_set, idxs, tensor_dict, config, tensor2vis, posBatch):
    fl = open(config.TPRvis_dir + "/" + tensor2vis + "_nRoles_" + str(config.nRoles) + "_test_set.csv", "a")
    nQuestions = len(data_set.data["q"])
    for which_q in range(nQuestions):
        if tensor2vis in ["fw_u_aR", "bw_u_aR", "fw_u_aF", "bw_u_aF"]: # Question side
            question = data_set.data["q"][which_q]
            q_len = len(question)
            T = tensor_dict[tensor2vis][which_q][:q_len]
        out = [[]]*q_len
        pos = posBatch[which_q]
        for i in range(q_len):
            out[i] = [idxs[which_q]] + [question[i]] + [pos[i][1]] + T[i].tolist()
        writer = csv.writer(fl)
        for row in out:
            writer.writerow(row)
    fl.close()

def getPOS_fromBatch(data_set, config):
    nQuestions = len(data_set.data["q"])
    out = [[]] * nQuestions
    pos_tagger = StanfordPOSTagger(config.stanford_model, config.stanford_jar, encoding='utf8')
    for which_q in range(nQuestions):
        if config.QuestionSideVis: # Question side
            question = data_set.data["q"][which_q]
        pos = pos_tagger.tag(question)
        out[which_q] = pos
    return out

def cluster(n, X):
    do_cluster(n, X)