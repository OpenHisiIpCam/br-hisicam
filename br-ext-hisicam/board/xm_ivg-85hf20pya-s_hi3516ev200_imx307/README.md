## /proc/umap/mipi

```
Module: [MIPI_RX], Build Time[Oct 18 2019, 18:21:00]

-----MIPI LANE DIVIDE MODE---------------------------------------------------------------------------------------------
  MODE         LANE DIVIDE
     0                   4

-----MIPI DEV ATTR-----------------------------------------------------------------------------------------------------
   Devno  WorkMode  DataRate            DataType   WDRMode    ImgX    ImgY    ImgW    ImgH
       0      MIPI        X1               RAW12      None       0       0    1920    1080

-----MIPI LANE INFO-----------------------------------------------------------------------------------------------------
   Devno                  LaneID
       0         0,  2, -1, -1

-----MIPI PHY DATA INFO------------------------------------------------------
   PhyId         LaneId            PhyData                MipiData              LvdsData
       0       0, 1, 2, 3    0x00,0x00,0x00,0x00    0xff,0x00,0xff,0x00    0x00,0x00,0x00,0x00

-----MIPI DETECT INFO----------------------------------------------------
 Devno VC   width  height
     0  0    1920    1080
     0  1       0       0

-----PHY CIL ERR INT INFO---------------------------------------------
   PhyId  Clk2TmOut  ClkTmOut  Lane0TmOut  Lane1TmOut  Lane2TmOut  Lane3TmOut  Clk2Esc  ClkEsc  Lane0Esc  Lane1Esc  Lane2Esc  Lane3Esc
       0          0         0           0           0           0           0        0       0         0         0         0         0

-----MIPI ERROR INT INFO 1-----------------------------------------------------------
   Devno  Ecc2  Vc0CRC  Vc1CRC  Vc2CRC  Vc3CRC  Vc0EccCorrct  Vc1EccCorrct  Vc2EccCorrct  Vc3EccCorrct
       0     0       0       0       0       0             0             0             0             0

-----MIPI ERROR INT INFO 2-----------------------------------------------------------
   Devno  Vc0Dt  Vc1Dt  Vc2Dt  Vc3Dt  Vc0FrmCrc  Vc1FrmCrc  Vc2FrmCrc  Vc3FrmCrc
       0      0      0      0      0          0          0          0          0

-----MIPI ERROR INT INFO 3-----------------------------------------------------------
   Devno  Vc0FrmSeq  Vc1FrmSeq  Vc2FrmSeq  Vc3FrmSeq  Vc0BndryMt  Vc1BndryMt  Vc2BndryMt  Vc3BndryMt
       0          0          0          0          0           0           0           0           0

-----MIPI ERROR INT INFO 4-----------------------------------------------------------
   Devno  DataFifoRdErr  CmdFifoRdErr  CmdFifoWrErr  DataFifoWrErr
       0              0             0             0              0

-----ALIGN ERROR INT INFO--------------------------------------
   Devno  FIFO_FullErr  Lane0Err  Lane1Err  Lane2Err  Lane3Err
       0             0         0         0         0         0
```

## /proc/umap/vi

```
[VI] Version: [Hi3516EV200_MPP_V1.0.1.2 B030 Release], Build Time[Oct 18 2019, 18:21:00]


-------------------------------MODULE PARAM ---------------------------------------------------------------------------
      DetectErrFrame        DropErrFrame            VbSource
                   0                   0              Common

-------------------------------VI MODE -------------------------------------------------------------
  Pipe0Mode   Pipe1Mode
     online     offline
-------------------------------VPSS MODE -------------------------------------------------------------
  Pipe0Mode   Pipe1Mode
     online     offline

-------------------------------VI DEV ATTR1----------------------------------------------------------------------------
  DevID   DevEn  BindPipe     Width    Height               IntfM     WkM     ComMsk0     ComMsk1   ScanM
      0       Y         Y      1920      1080                MIPI    1Mux    fff00000           0       P

-------------------------------VI DEV ATTR2----------------------------------------------------------------------------
  DevID   AD0   AD1   AD2   AD3     Seq  DataType   DataRev    BasW    BasH   HReph   VReph   WDRMode  CacheLine  DataRate
      0    -1    -1    -1    -1     N/A       RGB         N    1920    1080    NONE    NONE      None       1080        X1

-------------------------------VI BIND ATTR----------------------------------------------------------------------------
   DevID PipeNum              PipeId
       0       1                   0

-------------------------------VI DEV TIMING ATTR----------------------------------------------------------------------
  DevID DevTimingEn  DevFrmRate  DevWidth   DevHeight

-------------------------------VI PIPE ATTR1---------------------------------------------------------------------------
  PipeID  BypassMode YuvSkip IspBypass     Width    Height    PixFmt  BitWidth    NrEn SharpenEn  CompressMode
       0  BypassNone       N         N      1920      1080     RAW12        12       N         N          None

-------------------------------VI PIPE ATTR2---------------------------------------------------------------------------
  DiscProPic    SrcFRate    DstFRate FrameSource  RepeatMode   VCNum           IntType EarlyLine  VbPoolId
           N          -1          -1         DEV        NONE       0         EARLY_END       128        -1

-------------------------------VI INTERRUPT ONEBUF INFO----------------------------------------------------------------
      ProcCostTime    CapturedCostTime LowerLine UpperLine WdrExposureInterval

-------------------------------VI PIPE CROP ATTR-----------------------------------------------------------------------
  PipeID CropEn    CoorX   CoorY   Width  Height

-------------------------------VI PIPE USER PIC ATTR-------------------------------------------------------------------
  PipeID  Enable   ChnID    Mode BgColor   PicID   Width  Height  Stride  PixFmt  PoolID         PhyAddr

-------------------------------VI PIPE DUMP ATTR-----------------------------------------------------------------------
  PipeID    Enable     Depth  DumpType

-------------------------------VI CHN ATTR1----------------------------------------------------------------------------
  PipeID   ChnID   Width    Height    Mirror    Flip    SrcFRate    DstFRate    PixFmt      VideoFmt  DynamicRange

-------------------------------VI CHN ATTR2----------------------------------------------------------------------------
  CompressMode     Depth     Align  VbPoolId

-------------------------------VI EXTCHN ATTR1-------------------------------------------------------------------------
  PipeID   ChnID  Source  SrcChn   Width    Height    SrcFRate    DstFRate    PixFmt  DynamicRange  CompressMode     Depth

-------------------------------VI EXTCHN ATTR2-------------------------------------------------------------------------
  Align  VbPoolId

-------------------------------VI CHN CROP INFO------------------------------------------------------------------------
PipeID   ChnID  CropEn  CoorType   CoorX   CoorY   Width  Height   TrimX   TrimY TrimWid TrimHgt

-------------------------------VI CHN ROTATION INFO--------------------------------------------------------------------
  PipeID   ChnID    Rotation

-------------------------------VI CHN LDCV3 INFO-------------------------------------------------------------------------

-------------------------------ISP 2DofDIS INFO------------------------------------------------------------------------
  PipeID  Enable
       0       N

-------------------------------VI CHN OUTPUT RESOLUTION----------------------------------------------------------------
  PipeID   ChnID  Enable  Mirror    Flip   Width  Height  PixFmt  VideoFmt  DynamicRange  CompressMode FrameRate

-------------------------------VI PIPE STATUS--------------------------------------------------------------------------
  PipeID  Enable    IntCnt FrameRate LostFrame  VbFail   Width  Height
       0       Y     46882         0         0       0    1920    1080

-------------------------------VI CHN STATUS---------------------------------------------------------------------------
  PipeID   ChnID  Enable FrameRate LostFrame  VbFail   Width  Height

-------------------------------VI PIPE Statistic-----------------------------------------------------------------------
  PipeID     RecvPic     LostCnt      BufCnt   CurSoftTm   MaxSoftTm   CurTaskTm   MaxTaskTm   LowBandWidth  BeBufNum
       0           0           0           0           0           0           0           0              0         0

-------------------------------VI HW STATISTIC-------------------------------------------------------------------------
  ProcIdx    HWCostTm MaxHWCostTm    CycleCnt MaxCycleCnt
        0           0           0           0           0

-------------------------------VI PROC OFFLINE IRQ STATISTIC----------------------------------------------------------
 ProcIdx       SubmitCnt          IntCnt         ListCnt  TmOutCnt BusErrCnt  DcmpErrCnt StartErrCnt  NodeIdErrCnt
       0               0               0               0         0         0           0           0             0

-------------------------------VI PROC ONLINE IRQ STATISTIC-----------------------------------------------------------
 ProcIdx          IntCnt     FrmStartCnt FrmErrCnt  FrmFlowCnt BusErrCnt    DcmpErrCnt  CfgLossCnt   FirstIntPts
       0           23441           23441         0           0         0             0           0   16844427835

-------------------------------VI PROC COST TIME STATISTIC-----------------------------------------------------------
 ProcIdx    IntCntPerSec MaxIntCntPerSec  CurIntCostTm  MaxIntCostTm  TotalIntCostTm   IntTmPerSec  MaxIntTmPerSec
       0              12              25            39            43          914599           466             990

-------------------------------VI DEV DETECT INFO----------------------------------------------------------------------
   DevID  ValidWidth ValidHeight  TotalWidth
       0        1920        1080        7619

-------------------------------VI BAS DETECT INFO----------------------------------------------------------------------
   DevID  ValidWidth ValidHeight  TotalWidth

-------------------------------VI ISP DETECT INFO----------------------------------------------------------------------
   ISPID  ValidWidth ValidHeight  TotalWidth
       0        1920        1080        7619
```

## /proc/umap/isp

```


```


# cat /proc/umap/vi

[VI] Version: [Hi3516EV200_MPP_V1.0.1.2 B030 Release], Build Time[Oct 18 2019, 18:21:00]


-------------------------------MODULE PARAM ---------------------------------------------------------------------------
      DetectErrFrame        DropErrFrame            VbSource
                   0                   0              Common

-------------------------------VI MODE -------------------------------------------------------------
  Pipe0Mode   Pipe1Mode
     online     offline
-------------------------------VPSS MODE -------------------------------------------------------------
  Pipe0Mode   Pipe1Mode
     online     offline

-------------------------------VI DEV ATTR1----------------------------------------------------------------------------
  DevID   DevEn  BindPipe     Width    Height               IntfM     WkM     ComMsk0     ComMsk1   ScanM
      0       Y         Y      1920      1080                MIPI    1Mux    fff00000           0       P

-------------------------------VI DEV ATTR2----------------------------------------------------------------------------
  DevID   AD0   AD1   AD2   AD3     Seq  DataType   DataRev    BasW    BasH   HReph   VReph   WDRMode  CacheLine  DataRate
      0    -1    -1    -1    -1     N/A       RGB         N    1920    1080    NONE    NONE      None       1080        X1

-------------------------------VI BIND ATTR----------------------------------------------------------------------------
   DevID PipeNum              PipeId
       0       1                   0

-------------------------------VI DEV TIMING ATTR----------------------------------------------------------------------
  DevID DevTimingEn  DevFrmRate  DevWidth   DevHeight

-------------------------------VI PIPE ATTR1---------------------------------------------------------------------------
  PipeID  BypassMode YuvSkip IspBypass     Width    Height    PixFmt  BitWidth    NrEn SharpenEn  CompressMode
       0  BypassNone       N         N      1920      1080     RAW12        12       N         N          None

-------------------------------VI PIPE ATTR2---------------------------------------------------------------------------
  DiscProPic    SrcFRate    DstFRate FrameSource  RepeatMode   VCNum           IntType EarlyLine  VbPoolId
           N          -1          -1         DEV        NONE       0         EARLY_END       128        -1

-------------------------------VI INTERRUPT ONEBUF INFO----------------------------------------------------------------
      ProcCostTime    CapturedCostTime LowerLine UpperLine WdrExposureInterval

-------------------------------VI PIPE CROP ATTR-----------------------------------------------------------------------
  PipeID CropEn    CoorX   CoorY   Width  Height

-------------------------------VI PIPE USER PIC ATTR-------------------------------------------------------------------
  PipeID  Enable   ChnID    Mode BgColor   PicID   Width  Height  Stride  PixFmt  PoolID         PhyAddr

-------------------------------VI PIPE DUMP ATTR-----------------------------------------------------------------------
  PipeID    Enable     Depth  DumpType

-------------------------------VI CHN ATTR1----------------------------------------------------------------------------
  PipeID   ChnID   Width    Height    Mirror    Flip    SrcFRate    DstFRate    PixFmt      VideoFmt  DynamicRange

-------------------------------VI CHN ATTR2----------------------------------------------------------------------------
  CompressMode     Depth     Align  VbPoolId

-------------------------------VI EXTCHN ATTR1-------------------------------------------------------------------------
  PipeID   ChnID  Source  SrcChn   Width    Height    SrcFRate    DstFRate    PixFmt  DynamicRange  CompressMode     Depth

-------------------------------VI EXTCHN ATTR2-------------------------------------------------------------------------
  Align  VbPoolId

-------------------------------VI CHN CROP INFO------------------------------------------------------------------------
  PipeID   ChnID  CropEn  CoorType   CoorX   CoorY   Width  Height   TrimX   TrimY TrimWid TrimHgt

-------------------------------VI CHN ROTATION INFO--------------------------------------------------------------------
  PipeID   ChnID    Rotation

-------------------------------VI CHN LDCV3 INFO-------------------------------------------------------------------------

-------------------------------ISP 2DofDIS INFO------------------------------------------------------------------------
  PipeID  Enable
       0       N

-------------------------------VI CHN OUTPUT RESOLUTION----------------------------------------------------------------
  PipeID   ChnID  Enable  Mirror    Flip   Width  Height  PixFmt  VideoFmt  DynamicRange  CompressMode FrameRate

-------------------------------VI PIPE STATUS--------------------------------------------------------------------------
  PipeID  Enable    IntCnt FrameRate LostFrame  VbFail   Width  Height
       0       Y     46882         0         0       0    1920    1080

-------------------------------VI CHN STATUS---------------------------------------------------------------------------
  PipeID   ChnID  Enable FrameRate LostFrame  VbFail   Width  Height

-------------------------------VI PIPE Statistic-----------------------------------------------------------------------
  PipeID     RecvPic     LostCnt      BufCnt   CurSoftTm   MaxSoftTm   CurTaskTm   MaxTaskTm   LowBandWidth  BeBufNum
       0           0           0           0           0           0           0           0              0         0

-------------------------------VI HW STATISTIC-------------------------------------------------------------------------
  ProcIdx    HWCostTm MaxHWCostTm    CycleCnt MaxCycleCnt
        0           0           0           0           0

-------------------------------VI PROC OFFLINE IRQ STATISTIC----------------------------------------------------------
 ProcIdx       SubmitCnt          IntCnt         ListCnt  TmOutCnt BusErrCnt  DcmpErrCnt StartErrCnt  NodeIdErrCnt
       0               0               0               0         0         0           0           0             0

-------------------------------VI PROC ONLINE IRQ STATISTIC-----------------------------------------------------------
 ProcIdx          IntCnt     FrmStartCnt FrmErrCnt  FrmFlowCnt BusErrCnt    DcmpErrCnt  CfgLossCnt   FirstIntPts
       0           23441           23441         0           0         0             0           0   16844427835

-------------------------------VI PROC COST TIME STATISTIC-----------------------------------------------------------
 ProcIdx    IntCntPerSec MaxIntCntPerSec  CurIntCostTm  MaxIntCostTm  TotalIntCostTm   IntTmPerSec  MaxIntTmPerSec
       0              12              25            39            43          914599           466             990

-------------------------------VI DEV DETECT INFO----------------------------------------------------------------------
   DevID  ValidWidth ValidHeight  TotalWidth
       0        1920        1080        7619

-------------------------------VI BAS DETECT INFO----------------------------------------------------------------------
   DevID  ValidWidth ValidHeight  TotalWidth

-------------------------------VI ISP DETECT INFO----------------------------------------------------------------------
   ISPID  ValidWidth ValidHeight  TotalWidth
       0        1920        1080        7619


# cat /proc/umap/isp

[ISP] Version: [Hi3516EV200_ISP_V1.0.1.2 B030 Release], Build Time[Oct 18 2019, 18:21:00]


------------------------------------------------------------------------------
------------------------------ ISP PROC PIPE[0] -----------------------------
------------------------------------------------------------------------------

-----MODULE/CONTROL PARAM-----------------------------------------------------
    ProcParam    StatIntvl    UpdatePos   IntBothalf   IntTimeout    PwmNumber   PortIntDelay   QuickStart LdciTprFltEn LongFrmIntEn
           30            1            0            0          200            3              0            0            0            0

-----ISP Mode------------------------------------------------------------------
      StitchMode     RunningMode
          NORMAL          ONLINE

-----DRV INFO-------------------------------------------------------------------
     ViPipe     IntCnt       IntT    MaxIntT    IntGapT    MaxGapT   IntRat IspResetCnt  IspBeStaLost
          0      24587        255       3112      83398-1456372400       12           2             0

    IntTpye   PtIntCnt     PtIntT  PtMaxIntT  PtIntGapT  PtMaxGapT PtIntRat SensorCfgT  SensorMaxT
      Other          0          0          0          0          0        0          5        2899


-----PubAttr INFO--------------------------------------------------------------
        WndX        WndY        WndW        WndH        SnsW        SnsH       Bayer
           0           0        1920        1080        1920        1080        RGGB


-----SNAPATTR INFO-----------------------------------------------------------------
    SnapType    PipeMode      OPType   ProFrmNum
      NORMAL        NONE        Auto           3


[AE] Version: [Hi3516EV200_ISP_V1.0.1.2 B030 Release], Build Time[Oct 18 2019, 18:21:02]
-----AE INFO-------------------------------------------------------------------
      Again      Dgain      IspDg    SysGain        Iso       Line   AEInter   Incrmnt                 Exp   1stTime
      22924      11489       1108     262224      27177       2813         1       350           737413885    920000

       Comp     EVbias     OriAve     Offset      Speed       Tole     Error       Fps   RealFps    BDelay    WDelay
         66       1024          3          0        100          3        63     25.00      1199         2         0

    MaxLine   MaxLineT     MaxAgT     MaxDgT    MaxIDgT     MaxSgT    ManuEn    MaLine      MaAg      MaDg   MaIspDg
       2813       2813      22924     128914       2048     262144         0         0         0         0         0

    WdrMode  ExpRatio0  ExpRatio1  ExpRatio2    AnFlick    SlowMod     GainTh
       LINE         64         64         64          0          0       1024

     NodeId    IntTime    SysGain    IrisApe     UpStgy     DwStgy              Mltply
          0          1       1024          1          0          4                1024
          1       2813       1024          1          1          0             2880512
          2       2813     262144          1          4          1           737411072

   NodeIdSF  IntTimeSF  SysGainSF  IrisApeSF   UpStgySF   DwStgySF            MltplySF
          0          1       1024          1          0          4                1024
          1       1369       1024          1          1          0             1401856
          2       1369    5771923          1          4          1          7901762587

     AuIrEn     IrType     MaIrEn    DbgIrSt
          0     DCIris          0          0



[AWB] Version: [Hi3516EV200_ISP_V1.0.1.2 B030 Release], Build Time[Oct 18 2019, 18:21:04]
-----AWB INFO------------------------------------------------------------------
   Gain0   Gain1   Gain2   Gain3  CoTemp
   0x1c4   0x100   0x100   0x1c9    5255

 Color00 Color01 Color02 Color10 Color11 Color12 Color20 Color21 Color22
  0x 137  0x8040  0x   9  0x8027  0x 161  0x803a  0x  21  0x8048  0x 127

  ManuEn     Sat   Zones   Speed
       0      86      32     256

-----DEFECT INFO-----------------------------------
      Enable    Strength  BlendRatio
           1         220           0

-----GE INFO-------------------------------------------------------------
      Enable    NpOffset   Threshold    Strength
           1       32768        5120         130

-----FrameWDR INFO------------------------------------------------------------------
       MdtEn   LongThr  ShortThr  MdThrLow  MdThrHig
           1      3008      4032         0         0

-----Black Level Actual INFO--------------------------------------------------------------
            BlcR           BlcGr           BlcGb            BlcB
             240             240             240             240

-----BAYERNR INFO----------------------------------------------------------------------------
          Enable     NrLscEnable      CoarseStr0      CoarseStr1      CoarseStr2      CoarseStr3
               1               0             160             160             160             160

-----DRC INFO------------------------------------------------------------------
              En          ManuEn        Strength
               1               1             200

-----Lcac INFO-----------------------------------
      Enable       CrCtr       CbCtr
           1           3           3

-----DEMOSAIC INFO-------------------------------------------------------------
      Enable  NoDirStr  NoDirMFStr  NoDirHFStr DeSmthRng
           1        64          20           7         1

-----AntiFalseColor INFO-------------------------------------------------------------
      Enable   Threshold    Strength
           1           6           6

-----CA INFO-----------------------------------
      Enable    isoRatio
           1        1360

-----FPN CORRECT INFO------------------------------------------------------------
      En OpType Strength Offset
       0  --       --      --

-----SHARPEN INFO--------------------------------------------------------------
      bSharpenEn
               1
LumaWgt 0--7:
      31      31      31      31      31      31      31      31

LumaWgt 8--15:
      31      31      31      31      31      31      31      31

LumaWgt 16--23:
      31      31      31      31      31      31      31      31

LumaWgt 24--31:
      31      31      31      31      31      31      31      31

TextureStr 0--7:
     161     171     183     195     206     217     228     237

TextureStr 8--15:
     245     251     257     261     265     268     270     271

TextureStr 16--23:
     271     268     264     258     251     243     235     229

TextureStr 24--31:
     223     217     211     204     198     192     186     180

EdgeStr 0--7:
     161     171     183     195     206     217     228     237

EdgeStr 8--15:
     245     251     257     261     265     268     270     271

EdgeStr 16--23:
     271     268     264     258     251     243     235     229

EdgeStr 24--31:
     223     217     211     204     198     192     186     180

 TextureFreq    EdgeFreq   OverShoot  UnderShoot ShootSupStr  DetailCtrl EdgeFiltStrEdgeFiltMaxCap       RGain       GGain       BGain    SkinGain 
         317         272           1          37           4         164          31          18           8          45          31          31

 ShootSupAdj DetailCtrlThr  MaxSharpGain    SkinUmax    SkinUmin    SkinVmax    SkinVmin  WeakDetailGain
           0           176            46         128         110         149         128               4


-----LDCI INFO------------------------------------------------------------------------------
      Enable      Manual   GaussLPFSigma    HePosWgt  HePosSigma   HePosMean    HeNegWgt  HeNegSigma   HeNegMean     BlcCtrl
           1           0              58           0         145         143           3          80          36          30

-----PreGamma INFO--------------------------------------------------------------
          Enable
               0

-----------------------------------------------------------------------------
----------------------------------- ISP PROC END[0] ------------------------
-----------------------------------------------------------------------------


# cat /proc/umap/sys

[SYS] Version: [Hi3516EV200_MPP_V1.0.1.2 B030 Release], Build Time[Oct 18 2019, 18:21:00]


-----MODULE STATUS--------------------------------------------------------------
  Status
     run

-----SCALE COEFF INFO-----------------------------------------------------------
            RangeLevel   RangeValue    HorLum    HorChr    VerLum    VerChr
           RANGE_0   (    0,  8/64)   LEVEL_0   LEVEL_0   LEVEL_0   LEVEL_0
           RANGE_1   [ 8/64, 10/64)   LEVEL_1   LEVEL_1   LEVEL_1   LEVEL_1
           RANGE_2   [10/64, 15/64)   LEVEL_2   LEVEL_2   LEVEL_2   LEVEL_2
           RANGE_3   [15/64, 19/64)   LEVEL_3   LEVEL_3   LEVEL_3   LEVEL_3
           RANGE_4   [19/64, 24/64)   LEVEL_4   LEVEL_4   LEVEL_4   LEVEL_4
           RANGE_5   [24/64, 29/64)   LEVEL_5   LEVEL_5   LEVEL_5   LEVEL_5
           RANGE_6   [29/64, 33/64)   LEVEL_6   LEVEL_6   LEVEL_6   LEVEL_6
           RANGE_7   [33/64, 35/64)   LEVEL_7   LEVEL_7   LEVEL_7   LEVEL_7
           RANGE_8   [35/64, 38/64)   LEVEL_8   LEVEL_8   LEVEL_8   LEVEL_8
           RANGE_9   [38/64, 42/64)   LEVEL_9   LEVEL_9   LEVEL_9   LEVEL_9
           RANGE_10  [42/64, 45/64)  LEVEL_10  LEVEL_10  LEVEL_10  LEVEL_10
           RANGE_11  [45/64, 48/64)  LEVEL_11  LEVEL_11  LEVEL_11  LEVEL_11
           RANGE_12  [48/64, 51/64)  LEVEL_12  LEVEL_12  LEVEL_12  LEVEL_12
           RANGE_13  [51/64, 53/64)  LEVEL_13  LEVEL_13  LEVEL_13  LEVEL_13
           RANGE_14  [53/64, 55/64)  LEVEL_14  LEVEL_14  LEVEL_14  LEVEL_14
           RANGE_15  [55/64, 57/64)  LEVEL_15  LEVEL_15  LEVEL_15  LEVEL_15
           RANGE_16  [57/64, 60/64)  LEVEL_16  LEVEL_16  LEVEL_16  LEVEL_16
           RANGE_17  [60/64,     1]  LEVEL_17  LEVEL_17  LEVEL_17  LEVEL_17
           RANGE_18  (    1,   MAX)  LEVEL_18  LEVEL_18  LEVEL_18  LEVEL_18

-----MEM TABLE------------------------------------------------------------------
     Mod         ModName     Dev     Chn         MmzName

-----BIND RELATION TABLE--------------------------------------------------------
  FirMod  FirDev  FirChn  SecMod  SecDev  SecChn  TirMod  TirDev  TirChn    SendCnt     rstCnt
    vpss       0       1    venc       0       0    null       0       0      24915          0
    vpss       0       2    venc       0       2    null       0       0          0          0
    vpss       0       2    venc       0       1    null       0       0          0          0
      vi       0       0    vpss       0       1    venc       0       0          0          0
      vi       0       0    vpss       0       2    venc       0       2          0          0
      vi       0       0    vpss       0       2    venc       0       1          0          0
      ai       0       0    aenc       0       0    null       0       0      51798          0
