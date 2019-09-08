SELECT
a.oss,a.xdate,a.SITE_ID,a.name, a.cellname, a.MRBTS,a.lnbts,a.LNCEL,a.earfcnDL,a.dlchbw, a.pMax,"Missing" AS remark
from  isat_tmp.susy4G_yesterday a
left Join isat_tmp.susy4G_today b
On a.oss = b.oss and a.LNBTS = b.LNBTS and a.MRBTS = b.MRBTS and a.LNCEL = b.LNCEL
WHERE b.lncel IS null
group by a.oss, a.MRBTS,a.lnbts,a.LNCEL