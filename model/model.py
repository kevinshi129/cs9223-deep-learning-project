import torch
import torch.nn as nn
import torchvision.models as models

class NIMA(nn.Module):

    def __init__(self, base_model, num_classes=10):
        super(NIMA, self).__init__()
        self.features = base_model.features
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.75),
            nn.Linear(in_features=25088, out_features=num_classes),
            nn.Softmax())

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return out


class NIMAResNet(nn.Module):
    
    def __init__(self, base_model, num_classes=10):
        super(NIMAResNet, self).__init__()
        self.features = nn.Sequential(*list(base_model.children())[:-1])
        self.classifier = nn.Sequential(
                nn.Linear(2048, num_classes), # change to 512 for resnet 18
                nn.Softmax())

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size()[0], -1)
        out = self.classifier(out)
        return out


class NIMAMobileNetV2(nn.Module):
    def __init__(self, base_model, num_classes=10):
        super(NIMAMobileNetV2, self).__init__()
        self.features = base_model.features
        self.classifier = nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(62720, num_classes),
                nn.Softmax())

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size()[0], -1)
        out = self.classifier(out)
        return out


def single_emd_loss(p, q, r=2):
    """
    Earth Mover's Distance of one sample

    Args:
        p: true distribution of shape num_classes × 1
        q: estimated distribution of shape num_classes × 1
        r: norm parameter
    """
    length = p.shape[0]
    emd_loss = 0.0
    for i in range(1, length + 1):
        emd_loss += torch.abs(sum(p[:i] - q[:i])) ** r
    return (emd_loss / length) ** (1. / r)


def emd_loss(p, q, r=2):
    """
    Earth Mover's Distance on a batch

    Args:
        p: true distribution of shape mini_batch_size × num_classes × 1
        q: estimated distribution of shape mini_batch_size × num_classes × 1
        r: norm parameters
    """
    mini_batch_size = p.shape[0]
    loss_vector = []
    for i in range(mini_batch_size):
        loss_vector.append(single_emd_loss(p[i], q[i], r=r))
    return sum(loss_vector) / mini_batch_size
