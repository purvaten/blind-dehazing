"""Transmission map estimation functions."""
import numpy as np

import math

from decimal import Decimal

import torch

from torch.autograd import Variable

import torch.nn.functional as F

import tools


def sigmoid(y):
    """Returns sigmoid value of pixel x
    """
    l2_norm = math.sqrt(sum(map(lambda x: x * x, y)))
    res = 1 / (1 + Decimal(48 * (l2_norm - 0.1)).exp())
    return res


def get_norm(x):
    height, width = x.size(0), x.size(1)

    log = torch.log(x)
    log = log.view(1, 1, height, width)
    diff1 = torch.Tensor([-1, 0, 1])
    diff1 = Variable(diff1.view(1, 1, 1, 3), requires_grad=False)
    diff2 = torch.Tensor([1, 0, -1])
    diff2 = Variable(diff2.view(1, 1, 3, 1), requires_grad=False)

    # conv1 and conv2 should contain the x and y components resp, of grad(log)
    conv1 = F.conv2d(log, diff1, padding=(0, 1))
    conv2 = F.conv2d(log, diff2, padding=(1, 0))

    l2_norm = torch.mul(conv1, conv1) + torch.mul(conv2, conv2)
    l2_norm.view(height * width)
    return l2_norm


def loss_fun(w, sig):
    """Equation (26)"""
    l2_norm = get_norm(w)
    s = l2_norm * sig
    ret = torch.sum(s)
    return ret


def minimization(sig, tlb):
    """Returns new t-map
    Initialize tmap with tlb
    sig is a constant for the optimization step
    """
    t_height, t_width = len(tlb), len(tlb[0])
    tlb = torch.FloatTensor(np.reshape(tlb, [t_height, t_width]))
    for i in range(t_height):
        for j in range(t_width):
            if tlb[i][j] <= 0:
                tlb[i][j] = 10 ** -7

    weight = Variable(tlb, requires_grad=True)
    sig = Variable(sig, requires_grad=False)

    optimizer = torch.optim.SGD([weight], lr=10)
    optimizer.zero_grad()
    loss = loss_fun(weight, sig)
    print "Loss is ", loss
    loss.backward()
    optimizer.step()
    t = weight.data
    return t


def estimate_tmap(img, patches, airlight, constants):
    """Estimates t-map and returns dehazed output image after 20 iterations
    """
    patch_size = constants.PATCH_SIZE
    h, w = img.shape[0], img.shape[1]

    # Initializing lower bounded transmission map tlb
    tlb = np.empty([len(patches)])
    for index, patch in enumerate(patches):
        raw = np.reshape(patch.raw_patch, [-1, 3])
        tlb_patch = 1 - raw / airlight
        tlb[index] = max(tlb_patch[patch_size ** 2 // 2])
    tlb = np.reshape(tlb, [h - patch_size, w - patch_size, 1])
    img = np.reshape(img[0:h - patch_size, 0:w - patch_size], [h - patch_size, w - patch_size, 3])
    l_img = (img - airlight) / tlb + airlight

    tools.show_img([img, l_img])

    # Initial Sigmoid calculation
    grad = np.empty([3, l_img.shape[0] * l_img.shape[1]])
    l_img = np.reshape(l_img, [3, -1])
    grad = [np.gradient(l_img[i]) for i in range(3)]
    grad = np.reshape(grad, [-1, 3])
    l_img = np.reshape(l_img, [-1, 3])
    sig = torch.Tensor([float(sigmoid(grad[i])) for i in range(len(l_img))])
    sig = sig.view(h - patch_size, w - patch_size)

    # Run through 10 iterations
    t_prev = tlb
    new_grad = np.empty([3, l_img.shape[0] * l_img.shape[1]])
    for i in range(10):
        t_curr = minimization(sig, t_prev)
        t_curr = t_curr.numpy()
        t_curr = np.reshape(t_curr, [h - patch_size, w - patch_size, 1])
        l_img = (img - airlight) / t_curr + airlight
        t_prev = t_curr
        tools.show_img([img, l_img])

        # Recalculation of sigmoid
        l_img = np.reshape(l_img, [3, -1])
        new_grad = [np.gradient(l_img[i]) for i in range(3)]
        grad = np.reshape(new_grad, [-1, 3])
        l_img = np.reshape(l_img, [-1, 3])
        sig = torch.Tensor([float(sigmoid(grad[i])) for i in range(len(l_img))])
        sig = sig.view(h - patch_size, w - patch_size)

    l_img = np.reshape(l_img, [h - patch_size, w - patch_size, 3])
    return l_img