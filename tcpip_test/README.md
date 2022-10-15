# TCP Cubic 測試

[![hackmd-github-sync-badge](https://hackmd.io/2NaU5jDpSy6IYzPYJuEiIw/badge)](https://hackmd.io/2NaU5jDpSy6IYzPYJuEiIw)

## Topology
  > B is switch  
  > others are hosts  
  > C is receiver  
  > A & A' are senders  
  > > $~$A--B--C  
  > > $~~~~$/$~$\\  
  > > $~$  A'  sink

  > Scenario 1:
  > 1. A-B-C  
  > 2. A'-B-C  
  >    two TCP flows

  > Scenario 2:
  > 1. A-B-C  
  > 2. A'-B-sink  
  >    (link B - sink is unlimited)  
  >    two TCP flows  

  > Scenario 3:  
  > 1. (TCP) A-B-C  
  > 2. (UDP) A'-B -C 

  注意要點：
  > 要在意的點有 throughput, bandwidth, congestion window  
  > 應該需要 parse 出封包來看才會比較準確  
  > (也可以試著看 congestion control 中不同 phase 的狀況, e.g.  slow start)  
  > link 需要有 bandwidth 的限制，調整 bandwidth  來做測試  
  > 看能不能跑滿 bottleneck

## 實驗
### 環境建置
* 作業系統版本：Ubuntu 20.04 LTS  
  ![environment](https://i.imgur.com/vZmdfbC.png)
* 網路環境：
  * 用***Mininet+python***建置custom topology
  * (原本用docker container，但發現太花時間，且Mininet可以簡單快速滿足上述需求，也**可使用Wireshark圖形化界面截取封包**)
  * *A*, *A'*(在mininet中以***APr***表示), *C*, *sink*為host，*B*為switch
  * 拓撲建置：[topo.py](https://github.com/teogi/RDMA-project/blob/main/tcpip_test/topo.py)  
    * *pingall*: 測試連接性  
      ![ping reachability](https://i.imgur.com/OOGmnAk.png)  
      皆有成功連綫
* 流量：使用**iperf發送，wireshark監控**
  * 接收端**C (server side)** :![Node C](https://i.imgur.com/knvPSLA.png)
  * IP位置(皆爲CIDR/8)：
    * A: 10.0.0.1
    * C: 10.0.0.2
    * A': 10.0.0.3
    * sink: 10.0.0.4

### Scenario 1: A,A'送tcp flow給C
  * 初步測試：無bandwidth限制,個別發送10秒，A先發送，C延後5秒發送
    * 使用**xterm**分別打開每個node CLI,再手動發iperf指令，不知道有沒有更好的做法……
    * Node **A**:
      * iperf:![](https://i.imgur.com/wA1fFGk.png)
      * wireshark graph:![](https://i.imgur.com/nlKhcR5.png)
    * Node **A'**:
      * iperf:![](https://i.imgur.com/lQt4Vf5.png)
      * wireshark graph:![](https://i.imgur.com/SmanfVZ.png)


## Reference
### [什麽是Cubic TCP？（Wikipedia解釋）](https://zh.wikipedia.org/zh-tw/CUBIC_TCP)
> CUBIC是一個為具有高頻寬和高延遲的長胖網路（[LFN](https://zh.wikipedia.org/zh-tw/%E5%B8%A6%E5%AE%BD%E6%97%B6%E5%BB%B6%E4%B9%98%E7%A7%AF)）最佳化的TCP擁塞控制實現。

> CUBIC與標準的TCP流的另一個主要區別是，它不依賴於ACK的接收來增加窗口大小，CUBIC的窗口大小隻依賴於最後的擁塞事件。在標準的TCP中，極短的RTT將更快的收到ACK，它們的擁塞窗口將比其他較長RTT的流更快增長。CUBIC使資料流之間更加公平，因為窗口的增長與RTT（往返時延）無關。

> CUBIC TCP在Linux核心2.6.19及更高版本中被實現並預設使用。

### [TCP congestion control(fundamental)](https://notfalse.net/28/tcp-congestion-control#-Congestion-Window-cwnd)
> TCP 流量控制 (Flow Control)，是為避免 高速傳送端 癱瘓 低速接收端。  
> 而 TCP 壅塞控制 (Congestion Control)，則是用於避免 高速傳送端 癱瘓 網路。

> 任何 壅塞控制 演算法，必須解決的問題是:  
> 
> > 網絡，沒有獲取「給定連線的可用頻寬」之機制  
>
> 因此 TCP 壅塞控制 (Congestion Control) 必須以某種方式，得出關於「在任何給定時間內，可以發送多少資料」的結論，
以調整傳送速率至最佳效能，而不癱瘓 網路。