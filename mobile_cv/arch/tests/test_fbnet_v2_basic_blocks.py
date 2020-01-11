#!/usr/bin/env python3

import unittest

import mobile_cv.arch.fbnet_v2.basic_blocks as bb
import numpy as np
import torch


def _create_input(input_dims):
    assert isinstance(input_dims, (tuple, list))
    nchw = np.prod(input_dims)
    ret = (torch.arange(nchw, dtype=torch.float32) - (nchw / 2.0)) / (nchw)
    ret = ret.reshape(*input_dims)
    return ret


class TestFBNetV2BasicBlocks(unittest.TestCase):
    def test_hsigmoid(self):
        input = _create_input([1, 2, 2, 2])
        op = bb.HSigmoid()
        output = op(input)
        gt_output = torch.tensor(
            [0.416667, 0.4375, 0.458333, 0.479167, 0.5000, 0.5208, 0.5417, 0.5625]
        ).reshape([1, 2, 2, 2])
        np.testing.assert_allclose(output, gt_output, rtol=0, atol=1e-4)

    def test_hswish(self):
        input = _create_input([1, 2, 2, 2])
        op = bb.HSwish()
        output = op(input)
        gt_output = torch.tensor(
            [-0.2083, -0.1641, -0.1146, -0.0599, 0.0000, 0.0651, 0.1354, 0.2109]
        ).reshape([1, 2, 2, 2])
        np.testing.assert_allclose(output, gt_output, rtol=0, atol=1e-4)


class TestFBNetV2BasicBlocksEmptyInput(unittest.TestCase):
    def test_conv_bn_relu_empty_input(self):
        input_size = [0, 3, 4, 4]
        inputs = torch.rand(input_size)
        op = bb.ConvBNRelu(3, 4, stride=2, kernel_size=3, padding=1)
        output = op(inputs)
        self.assertEqual(output.shape, torch.Size([0, 4, 2, 2]))


if __name__ == "__main__":
    unittest.main()
