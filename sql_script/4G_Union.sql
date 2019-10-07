(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName, a.cellname, a.MRBTS,a.lnbts,a.LNCEL,a.earfcnDL,a.dlchbw, a.pMax,"newXXX" AS remark
from isat_tmp.susy4G_today a 
Join isat_tmp.susy4G_yesterday b 
On a.oss = b.oss and a.LNBTS = b.LNBTS and a.MRBTS = b.MRBTS and a.LNCEL = b.LNCEL
WHERE (a.NAME  LIKE '%XXX%' ) AND (b.NAME NOT LIKE '%XXX%') 
group by a.oss, a.MRBTS,b.mrbts,a.lnbts,b.lnbts,a.LNCEL,b.lncel
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName, a.cellname, a.MRBTS,a.lnbts,a.LNCEL,a.earfcnDL,a.dlchbw, a.pMax,"newXYX" AS remark
from isat_tmp.susy4G_today a 
Join isat_tmp.susy4G_yesterday b 
On a.oss = b.oss and a.LNBTS = b.LNBTS and a.MRBTS = b.MRBTS and a.LNCEL = b.LNCEL
WHERE (a.NAME  LIKE '%XYX%') AND (b.NAME NOT LIKE '%XYX%')
group by a.oss, a.MRBTS,b.mrbts,a.lnbts,b.lnbts,a.LNCEL,b.lncel
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName, a.cellname, a.MRBTS,a.lnbts,a.LNCEL,a.earfcnDL,a.dlchbw, a.pMax,"removalXXX" AS remark
from isat_tmp.susy4G_today a 
Join isat_tmp.susy4G_yesterday b 
On a.oss = b.oss and a.LNBTS = b.LNBTS and a.MRBTS = b.MRBTS and a.LNCEL = b.LNCEL
WHERE (b.NAME LIKE '%XXX%') AND (a.NAME NOT LIKE '%XYX%' ) AND (a.NAME NOT LIKE '%XXX%') 
group by a.oss, a.MRBTS,b.mrbts,a.lnbts,b.lnbts,a.LNCEL,b.lncel
)
UNION
(SELECT
a.oss,a.xdate,a.SITE_ID,b.NAME AS yesterdayName,a.NAME AS todayName, a.cellname, a.MRBTS,a.lnbts,a.LNCEL,a.earfcnDL,a.dlchbw, a.pMax,"removalXYX" AS remark
from isat_tmp.susy4G_today a 
Join isat_tmp.susy4G_yesterday b 
On a.oss = b.oss and a.LNBTS = b.LNBTS and a.MRBTS = b.MRBTS and a.LNCEL = b.LNCEL
WHERE (b.NAME LIKE '%XYX%') AND (a.NAME NOT LIKE '%XYX%' ) AND (a.NAME NOT LIKE '%XXX%') 
group by a.oss, a.MRBTS,b.mrbts,a.lnbts,b.lnbts,a.LNCEL,b.lncel
)