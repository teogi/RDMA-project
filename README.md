# RDMA專題

## Simulation 環境建置（SoftRoCE）
由於手邊沒有RDMA的實體網卡，因此利用兩個VM建立SoftRoCE 的Environment，好編譯與執行RDMA程式（參考[reference：SoftRoCE Environment Setup](https://ksld154.github.io/2020/12/06/SoftRoCE-Setup.html)）

### 環境相關資訊
* kernel distro version: ```Ubuntu 20.04 LTS```

### 測試
#### 1 Install VM
分別爲```csproj_rdma```(作爲server)和```csproj_rdma_cli```（作爲client）
![VMs information](https://i.imgur.com/XyCQP21.png)
設定在同一個NAT network（同一subnet底下）：![](https://i.imgur.com/n6oRNcv.png)


#### 2 Install required library
ibverb and RDMA library
```
sudo apt install libibverbs-dev librdmacm-dev
```
rdma-core
```
# Download the libary and install prerequisites
git clone https://github.com/linux-rdma/rdma-core.git
sudo apt install build-essential cmake gcc libudev-dev libnl-3-dev libnl-route-3-dev 
sudo apt install ninja-build pkg-config valgrind python3-dev cython3 python3-docutils pandoc
```
```
# Complie the library
cd rdma-core
bash build.sh
```
#### 3 Add Virtual RDMA NIC
command:
```
rdma link add <RDMA_NIC_NAME> type <TYPE> netdev <DEVICE>
```
* TYPE: rxe (for RoCE)
* DEVICE: 實體網卡名稱

實際VM操作：
* csproj_rdma: ```rxe_srv``` 綁 ```enp0s3``` ![](https://i.imgur.com/h3czt6I.png)

* csproj_rdma_client:```rxe_cli``` 綁 ```enp0s3```![](https://i.imgur.com/DI6pjOA.png)

#### 4 測試雙方互通情況
* **rping**
  ![](https://i.imgur.com/QdrjwV5.png)

* **ib_rc_pingpong**
  server side:![](https://i.imgur.com/mkJ3ZCp.png)
  client side:![](https://i.imgur.com/k246H3k.png)

* **perftest**:
  server side:![](https://i.imgur.com/L2B0beq.png)
  client side:![](https://i.imgur.com/ERapkB4.png)

## 第二學期

### FreeFlow

### 相關實驗 
#### TCP Cubic 測試
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
      
    

## reference
[RDMA tutorial sample code: The geek in the corner](https://github.com/tarickb/the-geek-in-the-corner)
[SoftRoCE Setup（中）](https://ksld154.github.io/2020/12/06/SoftRoCE-Setup.html)
[RDMA (Remote Directly Memory Access)](https://ithelp.ithome.com.tw/articles/10226640)
[Building an RDMA-capable application with IB verbs, part 1: basics](https://thegeekinthecorner.wordpress.com/2010/08/13/building-an-rdma-capable-application-with-ib-verbs-part-1-basics/)
### Papers
[Congestion Control for Large-Scale RDMA Deployments](https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p523.pdf)
[Introducing RDMA into computer networks course: design and experience](https://dl.acm.org/doi/pdf/10.5555/3280489.3280501)