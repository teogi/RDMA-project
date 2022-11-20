# 對TCP CUBIC 的網路測試

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

  ### 注意要點：
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

* 初步測試：使用**xterm**分別打開每個node CLI,再手動發iperf指令，不知道有沒有更好的做法……
  * 個別測試
    * A:(由於A' to C完全是同樣的條件，因此不另作A' to C)
    * ![](https://i.imgur.com/OqZb6iw.png)

  * 無bandwidth限制,個別發送10秒，A先發送，A'延後5秒發送
    * **A**:
      * iperf:![](https://i.imgur.com/wA1fFGk.png)
      * wireshark graph:![](https://i.imgur.com/nlKhcR5.png)
    * **A'**:
      * iperf:![](https://i.imgur.com/lQt4Vf5.png)
      * wireshark graph:![](https://i.imgur.com/SmanfVZ.png)
* bandwidth 100M:
  * A:  
    * iperf![](https://i.imgur.com/2REFR4w.png)
    * wireshark![](https://i.imgur.com/gxBDefq.png)
  * A':
    * iperf![](https://i.imgur.com/QbofVNJ.png)
    * wireshark![](https://i.imgur.com/MFhC7vf.png)
* bandwidth 10M:
    * A:![](https://i.imgur.com/sSTuMr9.png)
    * A':![](https://i.imgur.com/RXIeRdj.png)



### Scenario 2：tcp flow,A to C, A' to sink
* bandwidth 100M：同Scenario 1 作法  
  * 個別測試：
    * A to C:  
      
    * A' to sink:  
  * 第一次：
    * A to C:  
      ![](https://i.imgur.com/Mp0O4pV.png)
    * A' to sink:  
      ![](https://i.imgur.com/pO2WpWG.png)
  * 第二次：  
    * A to C:  
      ![](https://i.imgur.com/6L5MGnU.png)
    * A' to sink: 
      ![](https://i.imgur.com/DEbzn4L.png)
  * N次后發現使用這個bandwidth測試似乎不穩定，單試host A throughput也無法穩定……![](https://i.imgur.com/Q1QtZ3B.png)throughput不斷浮動


* bandwidth 10M:
    * A to C: ![](https://i.imgur.com/aZtWSN2.png)
    * A' to sink:![](https://i.imgur.com/YIyLlKc.png)



### Scenario 3:A to C(TCP), A' to sink(UDP)
* bandwidth 100M: 個別10秒，A'先送5秒，之後A送10秒，兩者重叠時間約5秒
    * A to C：**反復測試，結果有誤差**
        1. 約第7~9秒**有明顯下降**![](https://i.imgur.com/rvnpdP7.png)
        2. 5秒後**後期平順**![](https://i.imgur.com/TqDfxHG.png)
        3. 反面處理：A先送，A'後送：![](https://i.imgur.com/BW9s3v3.png)似乎看不出對throughput的影響
* bandwidth 10M: 
    * A to C
    * 第一次![](https://i.imgur.com/pCTZbuP.png)
    * 第二次![](https://i.imgur.com/pUAOMBi.png)
    * 基本上**影響甚微**



## 結果分析
### 在TCP Cubic的網路中對Throughput的影響
1. 從Scenario 1看出，對於不同senders對相同receiver的TCP流，**會對throughput有一定的影響**
2. 在Scenario 2，對於不同senders對不同receivers的TCP流，看不出TCP流重叠時期與個別傳輸時期的througput有什麽太明顯的不同，**對throughput的影響并不顯著**
3. 在Scenario 3，對於不同senders對不同receivers的TCP流和UDP流，看不出TCP流重叠時期與個別傳輸時期的througput有什麽太明顯的不同，**對throughput的影響并不顯著**
### cwnd的狀態
1. 除了 Scenario 1以外，cwnd的size**到達threshold之後都不變**
## Reference

### [TCP congestion control(fundamental)](https://notfalse.net/28/tcp-congestion-control#-Congestion-Window-cwnd)
> TCP 流量控制 (Flow Control)，是為避免 高速傳送端 癱瘓 低速接收端。  
> 而 TCP 壅塞控制 (Congestion Control)，則是用於避免 高速傳送端 癱瘓 網路。

> 任何 壅塞控制 演算法，必須解決的問題是:  
> 
> > 網絡，沒有獲取「給定連線的可用頻寬」之機制  
>
> 因此 TCP 壅塞控制 (Congestion Control) 必須以某種方式，得出關於「在任何給定時間內，可以發送多少資料」的結論，以調整傳送速率至最佳效能，而不癱瘓網路。

### [什麽是CUBIC TCP？（Wikipedia解釋）](https://zh.wikipedia.org/zh-tw/CUBIC_TCP)
> CUBIC是一個為具有高頻寬和高延遲的長胖網路（[LFN](https://zh.wikipedia.org/zh-tw/%E5%B8%A6%E5%AE%BD%E6%97%B6%E5%BB%B6%E4%B9%98%E7%A7%AF)）最佳化的TCP擁塞控制實現。

> CUBIC與標準的TCP流的另一個主要區別是，它不依賴於ACK的接收來增加窗口大小，CUBIC的窗口大小隻依賴於最後的擁塞事件。在標準的TCP中，極短的RTT將更快的收到ACK，它們的擁塞窗口將比其他較長RTT的流更快增長。CUBIC使資料流之間更加公平，因為窗口的增長與RTT（往返時延）無關。

> CUBIC TCP在Linux核心2.6.19及更高版本中被實現並預設使用。 

在[英文版的Algorithm](https://en.wikipedia.org/wiki/CUBIC_TCP#Algorithm)中：
> cwnd運算模型：  
> ![model](https://i.imgur.com/4AeztCA.png)  
> Define the following variables:  
> > β: Multiplicative decrease factor  
> > w_max: Window size just before the last reduction  
> > T: Time elapsed since the last window reduction  
> > C: A scaling constant  
> > cwnd: The congestion window at the current time

from [Pandora FMS](https://pandorafms.com/blog/tcp-congestion-control/):
> ![](https://i.imgur.com/eQn6GDo.png)
> 1. At the time of experiencing congestion event the window size for that instant will be recorded as Wmax or the maximum window size.
> 2. The Wmax value will be set as the inflection point of the cubic function that will govern the growth of the congestion window.
> 3. The transmission will then be restarted with a smaller window value and, if no congestion is experienced, this value will increase according to the concave portion of the cubic function.
> 4. As the window approaches Wmax the increments will slow down.
> 5. Once the tipping point has been reached, i.e. Wmax, the value of the window will continue to increase discreetly.
> 6. Finally, if the network is still not experiencing any congestion, the window size will continue to increase according to the convex portion of the function  

> As we can see, CUBIC implements schemes of **large increments at first**, which ***decrease** around the window size that **caused the last congestion***, and then **continue to increase** with large increments.
