import torch.nn as nn
import torch
from torch.nn.modules.module import Module
from torch_hyperbolic import manifolds


class HyperbolicEncoder(Module):
    def __init__(self, manifold: str = "PoincareBall", curvature=None):
        """ The encode() method of the HGCN and HNN from https://github.com/HazyResearch/hgcn/edit/master/models/encoders.py as an explicit class """
        super(HyperbolicEncoder, self).__init__()
        self.curvature = nn.Parameter(torch.Tensor([1.])) if curvature is None else curvature
        self.manifold = getattr(manifolds, manifold)()

    def forward(self, x):
        """ Projects x into hyperbolic space """
        if isinstance(self.manifold, manifolds.Hyperboloid):
            x = torch.cat((torch.zeros_like(x)[:, 0:1], x), dim=-1)

        x_tan = self.manifold.proj_tan0(x, self.curvature)

        x_hyp = self.manifold.expmap0(x_tan, c=self.curvature)
 
        x_hyp = self.manifold.proj(x_hyp, c=self.curvature)

        return x_hyp

    def extra_repr(self):
        return 'c={}'.format(self.curvature)
