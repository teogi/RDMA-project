# TCP Cubic 測試
* TOPO:
  > B is switch
  > others are hosts
  > C is receiver
  > A & A' are senders
  > $~$A--B--C
  > $~~~~$/$~$\\
  > $~$  A'  sink

  > Scenario 1:
  > 1. A-B-C
  > 2. A'-B-C
  >    two TCP flows
  > 
  > Scenario 2:
  > 1. A-B-C
  > 2. A'-B-sink
  >    (link B - sink is unlimited)
  >    two TCP flows
  > 
  > Scenario 3:
  > 1. (TCP) A-B-C
  > 2. (UDP) A'-B -C (edited) 

  注意要點：
  > 要在意的點有 throughput, bandwidth, congestion window
  > 應該需要 parse 出封包來看才會比較準確
  > (也可以試著看 congestion control 中不同 phase 的狀況, e.g.  slow start)
  > link 需要有 bandwidth 的限制，調整 bandwidth  來做測試
  > 看能不能跑滿 bottleneck

* 實驗環境：Ubuntu 20.04 LTS
  ![environment](https://i.imgur.com/vZmdfbC.png)
  * 網路環境：用***Mininet+python***建置custom topology，流量利用***iperf***由A，APr發送給C
    * (原本用docker container，但發現太花時間，且Mininet可以簡單快速滿足上述需求，也**可使用Wireshark圖形化界面截取封包**)
    * *A,C,sink*為host，*B*為switch
