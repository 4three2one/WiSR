from torch import nn
import torch
try:
    from attention import Seq_Transformer
except:
    from .attention import Seq_Transformer



class ChannelAttention(nn.Module):
    def __init__(self, channels, reduction=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.avg_pool(x).squeeze(-1)
        channel_att = self.fc(avg_out).unsqueeze(2)
        channel_att = self.sigmoid(channel_att)
        return x * channel_att

class SelfAttention(nn.Module):
    def __init__(self, in_channels):
        super(SelfAttention, self).__init__()
        self.query = nn.Conv1d(in_channels, in_channels // 8, kernel_size=1)
        self.key = nn.Conv1d(in_channels, in_channels // 8, kernel_size=1)
        self.value = nn.Conv1d(in_channels, in_channels, kernel_size=1)
        self.gamma = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        batch_size, channels, seq_len = x.size()
        query = self.query(x).view(batch_size, -1, seq_len)
        key = self.key(x).view(batch_size, -1, seq_len)
        value = self.value(x).view(batch_size, -1, seq_len)

        attention_weights = F.softmax(torch.bmm(query.transpose(1, 2), key), dim=2)
        attention_output = torch.bmm(value, attention_weights.transpose(1, 2))
        attention_output = attention_output.view(batch_size, channels, seq_len)

        out = self.gamma * attention_output + x
        return out


class base_Model(nn.Module):
    def __init__(self, configs,ts_mixer):
        super(base_Model, self).__init__()
        self.ts_mixer_f=ts_mixer
        self.conv_block1 = nn.Sequential(
            nn.Conv1d(configs.input_channels, 128, kernel_size=configs.kernel_size,
                      stride=configs.stride, bias=False, padding=(configs.kernel_size//2)),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=1),
            # nn.Dropout(configs.dropout)
        )

        self.channel_attention1 = ChannelAttention(128)

        self.conv_block2 = nn.Sequential(
            nn.Conv1d(128, 256, kernel_size=8, stride=1, bias=False, padding=4),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            # nn.MaxPool1d(kernel_size=2, stride=2, padding=1),
        )

        self.channel_attention2 = ChannelAttention(256)
        self.conv_block3 = nn.Sequential(
            nn.Conv1d(256, configs.final_out_channels, kernel_size=8, stride=1, bias=False, padding=4),
            nn.BatchNorm1d(configs.final_out_channels),
            nn.ReLU(),
            # nn.MaxPool1d(kernel_size=2, stride=2, padding=1),
        )
        self.channel_attention3 = ChannelAttention(512)

        # self.seq_transformer = Seq_Transformer(patch_size=configs.final_out_channels, dim=configs.TC.hidden_dim, depth=6,
        #                                        heads=4, mlp_dim=256)
        self.n_outputs = configs.final_out_channels

        self.l1 = nn.Conv1d(512 , 512 , kernel_size=3, stride=1, padding=0,
                            bias=False)
        self.l2 = nn.BatchNorm1d(512)
        self.l3 = nn.ReLU(inplace=True)
        self.l4 = nn.AdaptiveAvgPool1d(1)
        self.classifier = nn.Sequential(self.l1, self.l2, self.l3, self.l4)

        self.lstm = nn.LSTM(315, 512, num_layers=2)
        self.BiLstm = nn.LSTM(315, 512, num_layers=2, bidirectional=True)

        self.gru = nn.GRU(315, 512, num_layers=2)

        self.attention1 = SelfAttention(128)
        self.attention2 = SelfAttention(256)
        self.attention3 = SelfAttention(512)

    def forward(self, x_in):
        # print("x_in shape",x_in.shape)
        # if not x_in.shape==(128,342,500):
        #     x_in=x_in.reshape(x_in.shape[0],342,-1)
        #     pass

        # if self.ts_mixer_f:
        #     # print("ts_mixer_f....")
        #     x_in=self.tsmixer(x_in)
        ###
        x = self.conv_block1(x_in)  #2 90 250
        x = self.channel_attention1(x)
        x = self.conv_block2(x)
        x = self.channel_attention2(x)
        x = self.conv_block3(x)
        x = self.channel_attention3(x)
        # c_t=self.seq_transformer(x.transpose(1, 2))
        choose="none"
        if choose == "lstm":
            x = x.permute(1, 0, 2)
            _, (ht, ct) = self.lstm(x)
            x=ht[-1]
        elif choose == "bilstm":
            x = x.permute(1, 0, 2)
            _, (ht, ct) = self.BiLstm(x)
            x = ht[-1]
        elif choose == "gru":
            x = x.permute(1, 0, 2)
            _, ht= self.gru(x)
            x = ht[-1]
        else:
            x = self.classifier(x)  # torch.Size([8, 512, 1])

        x = x.view(x.size(0), -1)  # torch.Size([8, 512])
        return x

if __name__ == '__main__':
    # from config_files.HAR_Configs import Config as Configs
    # from config_files.HE_Configs import Config as Configs
    from own_Configs import Config as Configs

    configs = Configs()
    # x=torch.randn(1,180,400)
    model=base_Model(configs,False)
    # y=model(x)
    # for i in range(len(model.conv_block1)):
    #     x=model.conv_block1[i](x)
    #
    # for i in range(len(model.conv_block2)):
    #     x=model.conv_block2[i](x)
    #
    # for i in range(len(model.conv_block3)):
    #     x=model.conv_block3[i](x)
    # y=model(x)
    pass