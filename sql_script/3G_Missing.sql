SELECT
a.oss,a.xdate,a.SITE_ID,a.name,a.RNC,a.WBTS,a.WCEL,a.IPNBId,a.PtxCellMax,a.MBLBStateTransEnabled, "Missing" AS Remark
from  isat_tmp.susy3G_yesterday a
left Join isat_tmp.susy3G_today b 
ON a.oss = b.oss and a.rnc = b.rnc and a.wbts = b.wbts and a.WCEL = b.WCEL
WHERE b.WCEL IS null
group BY a.oss, a.RNC,a.WBTS,a.WCEL
;