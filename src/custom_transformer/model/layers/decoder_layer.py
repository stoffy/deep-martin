from typing import Tuple
import torch.nn as nn
import torch

from src.custom_transformer.model.layers.feed_forward_layer import FeedForward


class DecoderLayer(nn.Module):
    def __init__(self, d_model: int, heads: int, max_length: int, dropout: float = 0.1):
        super(DecoderLayer, self).__init__()

        self.d_model = d_model
        self.max_length = max_length
        self.norm_1 = nn.LayerNorm(d_model)
        self.norm_2 = nn.LayerNorm(d_model)
        self.norm_3 = nn.LayerNorm(d_model)

        self.dropout_1 = nn.Dropout(dropout)
        self.dropout_2 = nn.Dropout(dropout)
        self.dropout_3 = nn.Dropout(dropout)

        self.attn_1 = nn.MultiheadAttention(d_model, heads, dropout=dropout)
        self.attn_2 = nn.MultiheadAttention(d_model, heads, dropout=dropout)
        self.ff = FeedForward(d_model, dropout=dropout)

    def forward(self, x: torch.Tensor, e_outputs: torch.Tensor, src_mask: torch.Tensor,
                trg_masks: Tuple[torch.Tensor, torch.Tensor]) -> torch.Tensor:
        x = x.reshape(self.max_length-1, -1, self.d_model)
        x2 = self.norm_1(x)
        attention_1 = self.attn_2(x2, x2, x2, key_padding_mask=trg_masks[0], attn_mask=trg_masks[1])
        x = x + self.dropout_1(attention_1[0])
        x2 = self.norm_2(x)
        attention_2 = self.attn_2(x2, e_outputs, e_outputs, key_padding_mask=src_mask)
        x = x + self.dropout_2(attention_2[0])
        x2 = self.norm_3(x)
        x = x + self.dropout_3(self.ff(x2))
        return x
