(select
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.BSC,a.BCF,a.BTS,a.TRX,a.frequencyBandInUse,"newXXX" AS Remark
from isat_tmp.susy2G_today a 
Join isat_tmp.susy2G_yesterday b 
On a.oss = b.oss and a.bsc = b.bsc and a.bcf = b.bcf and a.bts = b.bts AND a.TRX = b.TRX
WHERE (a.NAME  LIKE '%XXX%' ) AND (b.NAME NOT LIKE '%XXX%') 
group by a.oss, a.bsc, b.bsc, a.bcf, b.bcf, a.bts, b.bts
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.BSC,a.BCF,a.BTS,a.TRX,a.frequencyBandInUse,"newXYX" AS Remark
from isat_tmp.susy2G_today a 
Join isat_tmp.susy2G_yesterday b 
On a.oss = b.oss and a.bsc = b.bsc and a.bcf = b.bcf and a.bts = b.bts AND a.TRX = b.TRX
WHERE (a.NAME  LIKE '%XYX%' ) AND (b.NAME NOT LIKE '%XYX%') 
group by a.oss, a.bsc, b.bsc, a.bcf, b.bcf, a.bts, b.bts
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.BSC,a.BCF,a.BTS,a.TRX,a.frequencyBandInUse,"removalXXX" AS Remark
from isat_tmp.susy2G_today a 
Join isat_tmp.susy2G_yesterday b 
On a.oss = b.oss and a.bsc = b.bsc and a.bcf = b.bcf and a.bts = b.bts
WHERE (b.NAME LIKE '%XXX%') AND (a.NAME NOT LIKE '%XYX%' ) AND (a.NAME NOT LIKE '%XXX%') 
group by a.oss, a.bsc, b.bsc, a.bcf, b.bcf, a.bts, b.bts
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName,a.BSC,a.BCF,a.BTS,a.TRX,a.frequencyBandInUse,"removalXYX" AS Remark
from isat_tmp.susy2G_today a 
Join isat_tmp.susy2G_yesterday b 
On a.oss = b.oss and a.bsc = b.bsc and a.bcf = b.bcf and a.bts = b.bts
WHERE (b.NAME LIKE '%XYX%') AND (a.NAME NOT LIKE '%XYX%' ) AND (a.NAME NOT LIKE '%XXX%') 
group by a.oss, a.bsc, b.bsc, a.bcf, b.bcf, a.bts, b.bts
)