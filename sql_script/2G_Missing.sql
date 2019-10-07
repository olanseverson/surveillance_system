SELECT
a.oss,a.xdate,a.SITE_ID,a.name,a.BSC,a.BCF,a.BTS,a.TRX,a.frequencyBandInUse, "Missing" AS Remark
from  isat_tmp.susy2G_yesterday a
left Join isat_tmp.susy2G_today b
On a.oss = b.oss AND a.bsc = b.bsc and a.bcf = b.bcf and a.bts = b.bts 
WHERE b.BTS IS null 
group by a.oss, a.BSC,a.BCF,a.BTS,a.TRX
;